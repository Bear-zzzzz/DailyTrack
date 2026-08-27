# Android 电量优化 — 知识复盘

---

## 知识体系速查

### 耗电来源

| 耗电源 | 占比 | 说明 |
|--------|------|------|
| 屏幕 | 20%~40% | 亮度、刷新率、常亮时间 |
| CPU/GPU | 15%~30% | 计算、渲染、唤醒 |
| 网络（Radio） | 10%~25% | 蜂窝、Wi-Fi、蓝牙 |
| GPS/定位 | 5%~15% | 高精度定位极耗电 |
| 传感器 | 2%~8% | 加速度、陀螺仪等 |
| 后台唤醒 | 5%~15% | AlarmManager、JobScheduler、FCM |

### 网络无线电状态机（核心）

```
IDLE(休眠,~0mA) ──数据传输──→ DCH(全功率,~300mA) ──5~10s无数据──→ FACH(中功率,~100mA)
     ▲                                                                    │
     └──────────────────── 10~15s 无数据 ──────────────────────────────────┘
```

- 每次请求即使只传 1 字节也消耗全功率电量
- DCH 回到 IDLE 需要 **~30 秒尾部时间**（DCH 10s + FACH 15s）
- **频繁请求 = Radio 反复唤醒 = 电量浪费**

### 后台任务调度对比

| 方式 | 特点 | 耗电 | 推荐度 |
|------|------|------|--------|
| AlarmManager | 精确定时唤醒，强制唤醒 | 高 | ⚠️ 谨慎 |
| JobScheduler | 条件触发，系统批量调度 | 低 | ✅ |
| WorkManager | JobScheduler 封装，兼容旧版 | 低 | ✅✅ 推荐 |
| FCM | 推送唤醒，被动接收 | 最低 | ✅✅ |

WorkManager 三核心：**条件触发**（充电+WiFi+空闲）、**批量调度**（系统合并多 App 任务）、**持久化**（重启不丢）。

### Doze 模式（Android 6.0+）

设备静止+未充电+屏幕关闭一段时间后进入低功耗模式。对 App 的限制：
- **延迟网络访问**：请求排队等到维护窗口
- **暂停 JobScheduler/WorkManager 任务**：延迟到维护窗口
- **忽略非精确闹钟**：AlarmManager.set() 被延迟
- **停止 GPS 扫描**：定位请求挂起
- **暂停同步**：账户同步暂停

适配方式：
1. 后台任务用 WorkManager 替代 AlarmManager
2. 紧急消息用 FCM high priority 推送（可绕过 Doze）
3. 闹钟等必须准时场景用 `setExactAndAllowWhileIdle()`（需权限）

### WakeLock

| 类型 | 效果 | CPU | 屏幕 | 耗电 |
|------|------|-----|------|------|
| PARTIAL_WAKE_LOCK | 保持 CPU 运行 | ✅ | ❌ | 中 |
| SCREEN_DIM_WAKE_LOCK | 屏幕变暗 | ✅ | ✅(暗) | 高 |
| SCREEN_BRIGHT_WAKE_LOCK | 屏幕保持亮 | ✅ | ✅(亮) | 高 |
| FULL_WAKE_LOCK | 屏幕+键盘亮 | ✅ | ✅(亮) | 最高 |

- WakeLock = **保持唤醒**（hold），不是**唤醒**（wake up）
- AlarmManager = 唤醒设备
- 正确姿势：带超时 acquire + finally release

### 定位优化策略

| 策略 | 说明 |
|------|------|
| 分级定位 | 导航用 HIGH_ACCURACY，轨迹记录用 BALANCED，后台用 LOW_POWER |
| 被动定位 | PRIORITY_NO_POWER，复用其他 App 定位结果，零额外耗电 |
| 静止检测 | 加速度传感器检测静止时降低 GPS 频率 |
| 先粗后精 | 先基站/Wi-Fi 快速粗定位，需要精度时再开 GPS |
| 后台限制 | 后台定位必须前台 Service，Android 10+ 需单独权限，12+ 精度降到 ~1km |

### 工具速查

| 工具 | 用途 |
|------|------|
| Battery Historian | 电量消耗时间线可视化（官方） |
| `dumpsys batterystats` | 按 App 查耗电统计 |
| Energy Profiler | Android Studio 实时 CPU/Network/GPS 耗电 |

---

## 问答复盘

### Q1: 蜂窝网络 Radio 状态机有哪些状态？为什么频繁小请求更耗电？

**我的回答：**

有 IDLE、全功率、中功率 3 个状态。每 30s 发一次就会进入全功率状态，电量消耗大。可以把小请求汇集一起来，一次性发完所有数据，这样只唤醒一次。

**点评：** ⭐⭐⭐⭐ 基本正确

补关键数字：DCH 回到 IDLE 需要 **~30 秒尾部时间**（DCH 10s + FACH 15s），所以每次请求实际消耗的不是"传数据那几毫秒"，而是 30 秒的 Radio 全功率电量。

**优化点：** 面试中说出"30 秒尾部时间"这个数字，体现对 Radio 状态机的量化理解。

---

### Q2: WakeLock 有什么作用？使用不当会导致什么问题？正确使用姿势？

**我的回答：**

WakeLock 是唤醒设备做定时任务，使用不当会造成电量消耗过快。正确的使用方式应该避免用 Alarm WakeLock，尽量使用 WorkManager。另外使用后要设置超时，主动释放。

**点评：** ⭐⭐⭐ 概念偏差

**WakeLock 的定义答错了**。WakeLock 不是"唤醒设备做定时任务"，而是**保持设备/CPU 不进入休眠**，让任务能在屏幕关闭后继续执行。唤醒设备用的是 AlarmManager。

✅ 正确的部分：使用不当会持续耗电、要设置超时+主动释放、推荐用 WorkManager 替代。

正确理解：
- WakeLock = **保持唤醒**（hold），不是**唤醒**（wake up）
- AlarmManager = 唤醒设备
- 两者常配合使用：AlarmManager 唤醒 → WakeLock 保持 CPU 运行直到任务完成

**优化点：** 面试中要分清"唤醒"和"保持唤醒"两个动作。WakeLock 的核心风险是 acquire 后不 release，导致 CPU 一直不睡。

---

### Q3: AlarmManager、JobScheduler、WorkManager 三者的区别？为什么 6.0 后不建议用 AlarmManager？

**我的回答：**

AlarmManager 是直接唤醒设备执行任务，会导致电量消耗过多。JobScheduler 是通过系统调度任务，尽量在空闲时执行。WorkManager 是 JobScheduler 的升级版，更加推荐使用。

**点评：** ⭐⭐⭐ 方向对，缺关键差异

缺的关键点：
- **AlarmManager 为什么被限制**：Android 6.0 Doze 模式下，**非精确闹钟会被延迟**，精确闹钟需要权限（Android 12+），强制唤醒打断系统批量调度。
- **WorkManager 不只是"升级版"**：核心价值是**条件触发**（充电+WiFi+空闲时才执行）+ **系统批量合并**（多个 App 的任务攒到一起批量唤醒）+ **持久化**（重启不丢）。
- **JobScheduler 已被 WorkManager 封装**，API 21+ WorkManager 底层自动选 JobScheduler 或 AlarmManager。

**优化点：** 面试中强调 WorkManager 的三个核心能力：条件触发、批量调度、持久化。

---

### Q4: 什么是 Doze 模式？对 App 产生什么限制？如何适配？

**我的回答：**

是系统长时间无操作待机后，系统会进入低功耗模式，减少电量消耗。App 的限制不清楚。

**点评：** ⭐⭐ 知道概念，不知道限制

Doze 对 App 的限制（必须记住）：
- **延迟网络访问**：网络请求被排队，等到维护窗口才放行
- **暂停 JobScheduler/WorkManager 任务**：延迟到维护窗口
- **忽略非精确闹钟**：AlarmManager.set() 被延迟
- **停止 GPS 扫描**：定位请求被挂起
- **暂停同步**：账户同步被暂停
- 只有**维护窗口**（每几小时短暂开放）才能执行被延迟的任务

适配方式：
1. 后台任务全部用 WorkManager 替代 AlarmManager
2. 紧急消息用 FCM high priority 推送（可绕过 Doze）
3. 闹钟等必须准时的场景用 `setExactAndAllowWhileIdle()`（需权限）

**优化点：** 这题是面试高频，至少记住"延迟网络、暂停任务、忽略闹钟"三个限制 + WorkManager 适配。

---

### Q5: GPS 定位耗电的主要原因？如何根据不同场景做定位优化？

**我的回答：**

GPS 芯片冷启动耗时长，定位精度高、频率高，因此耗电多。优化：1. 前台时才运行 GPS 定位；2. 尽量采用融合定位方式，减少 GPS 频率。

**点评：** ⭐⭐⭐ 方向对，缺关键策略

补的关键策略：

| 策略 | 说明 |
|------|------|
| **分级定位** | 导航用 HIGH_ACCURACY，轨迹记录用 BALANCED，后台用 LOW_POWER |
| **被动定位** | 用 `PRIORITY_NO_POWER`，复用其他 App 的定位结果，零额外耗电 |
| **静止检测** | 加速度传感器检测静止时降低 GPS 频率 |
| **后台限制** | 后台定位必须前台 Service，Android 10+ 需单独权限，12+ 精度降到 ~1km |
| **先粗后精** | 先基站/Wi-Fi 快速粗定位，需要精度时再开 GPS |

**优化点：** 面试中说出"分级定位 + 被动定位 + 静止检测"三个策略，体现对定位耗电的系统理解。

---

## 评估总结

| 题 | 评价 | 待补强 |
|----|------|--------|
| 1 | ⭐⭐⭐⭐ 基本正确 | 补 Radio 尾部 30s 耗电 |
| 2 | ⭐⭐⭐ 概念偏差 | WakeLock 是"保持唤醒"不是"唤醒" |
| 3 | ⭐⭐⭐ 方向对 | 补 WorkManager 三核心：条件触发/批量/持久化 |
| 4 | ⭐⭐ 知概念不知限制 | 必须记住 Doze 的三个限制 + 适配方式 |
| 5 | ⭐⭐⭐ 方向对 | 补分级定位/被动定位/静止检测 |

**整体：耗电优化经验较少，概念方向基本正确，但系统机制细节（Doze 限制、WakeLock 定义）需要补强。**

重点记三个：
1. **Doze 限制**：延迟网络、暂停任务、忽略闹钟
2. **WakeLock**：保持唤醒（不是唤醒），acquire 必须 release
3. **WorkManager 三核心**：条件触发、批量调度、持久化
