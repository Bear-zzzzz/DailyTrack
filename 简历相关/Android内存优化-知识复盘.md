# Android 内存优化 — 知识复盘

---

## 知识体系速查

### Java 堆 vs Native 堆

| 堆 | 管理者 | 存储内容 | 回收方式 | 限制 |
|----|--------|----------|----------|------|
| **Java Heap** | ART/Dalvik GC | Java/Kotlin 对象 | GC 自动回收 | 有堆大小限制（128~512MB） |
| **Native Heap** | Linux malloc | C/C++ 对象、Bitmap 像素数据 | 手动 free 或 mmap | 无明确限制（受物理内存约束） |

**Android 8.0 关键变化**：Bitmap 像素数据通过 `NativeAllocationRegistry` 关联到 Java 对象，GC 能感知并回收 → **不再需要手动 `recycle()`**，但仍需及时断开 Java 引用。

### 进程优先级（LMK 回收顺序）

| 优先级 | 状态 | 被杀可能性 |
|--------|------|------------|
| **前台进程 Foreground** | Activity onResume | 几乎不杀 |
| **可见进程 Visible** | Activity onPause | 低 |
| **服务进程 Service** | 后台运行 Service | 中 |
| **后台进程 Cached** | Activity onStop | 高 |
| **空进程 Empty** | 无活跃组件 | 最高 |

LMK 按 `oom_adj` 从高到低依次杀，不是"先杀完低的再杀某一级"。

### GC 机制

- **代际假说**：① 绝大多数对象朝生夕灭；② 熬过越多次 GC 的对象越可能继续存活
- **Young GC**：只扫描新生代，速度快（<10ms），频繁触发
- **Full GC**：扫描全堆，速度慢（50~200ms），低频触发
- **ART CC（Concurrent Copying）**：部分并发，短暂 STW，不是全程暂停
- 卡顿原因：短暂 STW 恰好卡在渲染帧节点上

### GC Root 类型

| 类型 | 泄漏场景 |
|------|----------|
| 静态变量 | 静态持有 Activity/View |
| 活动线程 | 线程持有外部引用 |
| JNI 引用 | Native 层全局引用 |
| 栈帧局部变量 | 长生命周期方法持有引用 |
| System Class | 系统类持有引用 |
| 监视器锁 | synchronized 持有对象 |

### 核心优化手段速查

| 优化手段 | 核心思路 | 优先级 |
|----------|----------|--------|
| Bitmap 采样压缩 | inSampleSize 按需加载 | P0 |
| 修复内存泄漏 | 断开引用链 | P0 |
| LruCache + onTrimMemory | 缓存上限 + 级别响应 | P1 |
| 对象池复用 | 减少内存抖动 | P1 |
| SparseArray 替代 HashMap | 无装箱开销 | P2 |
| @IntDef 替代枚举 | 常量替代对象 | P2 |
| Native 内存管理 | JNI malloc/free 配对 | P3 |

### 工具速查

| 工具 | 用途 |
|------|------|
| `dumpsys meminfo` | PSS/Java/Native 内存概览 |
| Memory Profiler | Heap Dump + Allocation Tracking |
| LeakCanary | Debug 自动检测 Activity/Fragment/ViewModel 泄漏 |
| MAT | hprof 深入分析，Dominator Tree + Path to GC Roots |
| ASan | Native 内存问题检测 |

---

## 问答复盘

### Q1: Java 堆和 Native 堆的区别？Android 8.0 前后 Bitmap 像素数据存储位置变化？对开发者意味着什么？

**我的回答：**

Java 堆中存储的是 Java Kotlin 对象，Native 堆存的是 C++、C 对象，也包括 Bitmap。8.0 前 Bitmap 存 Native 堆，8.0 后通过一个 registry 关联到了 Java 对象，也可以被 GC 回收。

**点评：** ⭐⭐⭐⭐ 核心正确

缺的关键结论：8.0 后通过 `NativeAllocationRegistry` 关联到 Java 对象，意味着 **Bitmap 不再需要手动 `recycle()`**，GC 能自动感知并回收 Native 内存。但**仍需及时断开 Java 引用**，否则照样泄漏。

**优化点：** 面试中明确说出"不再需要手动 recycle，但仍需断开引用"这个结论，体现对 API 变化的工程理解。

---

### Q2: Android 进程优先级回收机制？onStop 时处于什么优先级？内存紧张时怎样处理？

**我的回答：**

分为前台进程、后台进程、服务进程、空闲进程，优先级从高到低。处于 onStop 时位于后台，内存紧张时如果低优先级进程 kill 后仍然紧张就会 kill 后台进程。

**点评：** ⭐⭐⭐ 分类不完整，细节有误

问题：
- **优先级分类不完整**，漏了**可见进程（Visible）**。完整 5 级：前台 > 可见 > 服务 > 后台 > 空进程。
- onStop 状态更准确说是**后台进程（Cached）**，不是"后台进程"和"空闲进程"混淆。空进程是指无任何活跃组件的进程。
- "先杀完低的再杀后台"——表述有误。LMK 是**按 oom_adj 从高到低依次杀**，后台进程本身就是低优先级。

**优化点：** 面试中完整说出 5 级优先级，强调 LMK 按 oom_adj 值从高到低依次杀，不是分级逐级杀。

---

### Q3: 什么是代际假说？Young GC 和 Full GC 的区别？为什么频繁 GC 会导致卡顿？

**我的回答：**

GC 过程中会把对象分为新生代和老年代，每一次 GC 时存活下来的年龄+1，年龄超过阈值就是老年代。Young GC 就是只 GC 新生代，Full GC 是全量 GC。因为 GC 时会暂停全量的进程，标记复制清除，完成 GC 后再恢复。如果频繁 GC 且页面渲染数据同步工作恰好被暂停，体感上就会卡顿。

**点评：** ⭐⭐⭐ 基本正确，机制描述需精确

需精确化：
- 代际假说完整表述是两条：① 绝大多数对象朝生夕灭；② 熬过越多次 GC 的对象越可能继续存活。只答了第一条的变体。
- "GC 时会暂停全量的进程"——不准确。ART 的 **CC（Concurrent Copying）** 是**部分并发**的，只有短暂 STW，不是全程暂停。卡顿是因为**短暂 STW 恰好卡在渲染帧的节点上**。

**优化点：** 强调 ART CC 是部分并发 + 短暂 STW，不是全程暂停。代际假说要说出两条。

---

### Q4: 列举至少 4 种常见内存泄漏场景及修复方案。

**我的回答：**

1. 静态变量持有了 Activity — 用弱引用替代
2. 线程持有了 Activity — 线程结束时释放 Activity
3. 页面动画未终止 — onPause 时停止动画
4. Handler 发送了延迟消息 — onDestroy 时移除消息
5. 注册了广播 — onDestroy 时注销广播

**点评：** ⭐⭐⭐⭐ 场景丰富

需修正：
- **静态变量持有 Activity**：弱引用可以，但更优先的方案是**及时置 null**。弱引用是备选。
- **线程持有 Activity**："线程结束时释放"——如果线程一直不结束呢？正确修复是：改为**静态内部类 + WeakReference**，或线程内部检查 Activity 是否已销毁。

**优化点：** 静态变量泄漏首选"及时置 null"而非弱引用；线程泄漏核心修复是"静态内部类 + WeakReference"。

---

### Q5: 什么是 GC Root？非静态内部类为什么会导致内存泄漏？

**我的回答：**

GC Root 就是 GC 引用链的根部，常见的有静态变量、Thread、Native 引用、正在执行方法的临时变量。非静态内部类导致泄漏，比如一个方法正在执行，引用了 Activity，但方法一直没有终止，Activity 就会回收失败造成泄漏。

**点评：** ⭐⭐⭐ GC Root 对，引用链解释有偏差

问题：引用链解释的是**方法栈帧**场景，但**非静态内部类泄漏的核心机制没答到**。

**正确解释**：非静态内部类**隐式持有外部类引用**（`Outer.this`）。当内部类对象被长生命周期引用（如线程池、静态变量）持有时，引用链是：

```
GC Root（Thread/静态变量）
  → 内部类实例（持有 Outer.this）
    → 外部 Activity
      → 无法回收 → 泄漏
```

关键点：**隐式持有 `Outer.this`** 是根因，不是"方法没终止"。

**优化点：** 面试中必须说出"隐式持有 Outer.this"这个关键词，并画出完整引用链：GC Root → 内部类实例 → 外部 Activity。

---

### Q6: 线上某页面 OOM 率偏高，描述完整排查路径。

**我的回答：**

首先用 `adb shell dumpsys memory info` 查看内存占用情况，看 PSS、Java、Native 占用。对比稳定基线，查看哪部分占比偏高。抓取堆快照，用 LeakCanary 工具查看是否有内存泄漏、大体积/高数量对象分布。

**点评：** ⭐⭐⭐ 思路对，工具链不完整

问题：
- **命令写错了**：是 `dumpsys meminfo`，不是 `dumpsys memory info`。
- **缺 Heap Dump 分析**：应该用 Profiler 或 MAT 抓 Heap Dump，按对象数量/大小排序找异常对象，再查 References 引用链。
- **缺 Allocation Tracking**：如果泄漏不是静态持有而是持续分配，需要记录分配轨迹定位高频分配源。
- **缺对比策略**：应该**进出页面前后各 Dump 一次**，对比差异，才能确认是这个页面的问题。

**优化点：** 完整路径应为：
```
dumpsys meminfo（PSS/Java/Native 分布）
→ 进出页面前后各 Dump Heap 对比差异
→ Profiler/MAT 按对象数量/大小排序找异常
→ 查 References 引用链定位泄漏源
→ Allocation Tracking 定位高频分配
```

---

### Q7: 什么是内存抖动？为什么引起卡顿？如何检测和解决？

**我的回答：**

反复创建和销毁对象，导致频繁 GC 卡顿。Memory Profiler 中可以看到锯齿状波形，火焰图里可以看到 malloc 调用。解决方式：对象池复用，循环内不能创建对象。

**点评：** ⭐⭐⭐⭐ 答得好

可补充：
- 火焰图中看的是 **`alloc` 相关调用**，不是 `malloc`（malloc 是 Native 层的）。
- 可补充**预分配缓冲区**作为第三种解决方案，如循环外创建 StringBuilder，循环内 `setLength(0)` 复用。

**优化点：** 火焰图看 alloc 调用（Java 层），非 malloc。补充预分配缓冲区方案。

---

### Q8: PSS 持续增长不回落，但 LeakCanary 没报泄漏，可能的原因？

**我的回答：**

1. Bitmap 占用空间很大，创建对象过多、对象过大。可以查看 Bitmap 的大小，是否有重复创建 Bitmap、是否有未回收的 Bitmap。查看 Memory Profiler 里对象的 top 数量和占用空间 top 大小。

**点评：** ⭐⭐⭐ 方向对，排查面不够宽

LeakCanary 没报泄漏 + PSS 持续增长，可能的原因远不止 Bitmap：

| 可能原因 | 排查方式 |
|----------|----------|
| **Native 内存泄漏**（JNI malloc 未 free） | 看 Native Heap 是否持续增长；用 ASan 检测 |
| **内存缓存无上限**（LruCache 配置过大或未设上限） | 检查缓存策略，onTrimMemory 是否响应 |
| **Bitmap 未回收但引用已断**（8.0 前 Native 堆不感知 GC） | 看 Graphics/Native Heap |
| **线程/连接池累积**（线程池未复用，不断新建线程） | Profiler 看线程数 |
| **LeakCanary 检测盲区**（只检测 Activity/Fragment/ViewModel，不检测 Service/View） | 手动 Dump Heap，用 MAT 查 Service/单例引用链 |

**优化点：** 面试中应体现"分层排查"思维——先看 Java Heap 还是 Native Heap 增长，再分别用不同工具下钻。**LeakCanary 只覆盖 Activity/Fragment/ViewModel，Native 泄漏和 Service 泄漏是盲区**。

---

## 评估总结

| 题 | 评价 | 待补强 |
|----|------|--------|
| 1 | ⭐⭐⭐⭐ 核心正确 | 补"不再需要 recycle"的结论 |
| 2 | ⭐⭐⭐ 分类不完整 | 补可见进程，精确 LMK 机制 |
| 3 | ⭐⭐⭐ 基本正确 | 精确 CC 并发机制，补代际假说第二条 |
| 4 | ⭐⭐⭐⭐ 场景丰富 | 修复方案需更精确（静态置 null 优先，线程用静态内部类） |
| 5 | ⭐⭐⭐ GC Root 对 | 引用链解释偏差，核心是"隐式持有 Outer.this" |
| 6 | ⭐⭐⭐ 思路对 | 命令写错，缺 Heap Dump + Allocation Tracking + 对比策略 |
| 7 | ⭐⭐⭐⭐ 答得好 | 补预分配缓冲区，火焰图看 alloc 不是 malloc |
| 8 | ⭐⭐⭐ 方向对 | 排查面不够宽，缺 Native 泄漏/缓存无上限/LeakCanary 盲区 |

**整体：概念理解扎实，但细节精确度和工具链操作熟练度需提升。**

重点补强方向：
1. **非静态内部类泄漏机制**：隐式持有 `Outer.this` 的引用链
2. **LeakCanary 盲区**：Native 泄漏、Service 泄漏
3. **分层排查思维**：Java Heap vs Native Heap 分别下钻
4. **GC 机制精确化**：CC 并发复制，非全程 STW
