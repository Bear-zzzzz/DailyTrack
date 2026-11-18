# 牛客赛文X社招面经：采集说明与目录

采集日期：2026-11-16。

来源：[赛文Xの社招面经汇总](https://www.nowcoder.com/discuss/921546202062000128?sourceSSR=users)。严格按原目录顺序，包含从「互动影游小厂 AI全栈开发 一面」到「商汤 全栈开发 一面」的两端。

## 采集结果

- 目录条目：**110**。
- 唯一帖子正文：**109**；无法获取：**0**。
- 提取面试问项：**1581** 次；同一主分类下仅合并文字相同（忽略大小写、空白、标点）的问项后：**1572** 条。
- 主分类：**16** 类；排除结果、评价、公司介绍及页面控件等非问题行：**83** 行。
- 不把原汇总标题里的「200+」当作本次范围的篇数；不擅自寻找目录之外的面经。

## 文件导航

1. [逐篇面经与问题](01_逐篇面经与问题.md)：逐篇保留主体、抽出问项、分离其他信息。
2. [分类题库](02_分类题库.md)：按主分类浏览全部问项，重复文字合并但保留所有来源。
3. [高频主题与复习索引](03_高频主题与复习索引.md)：跨篇主题覆盖统计及原题示例。
4. [全部问项 JSON](questions.json)：每次出现独立保存，含 ID、原文、分类、标签、来源行与 URL。
5. [帖子主体 JSON](posts.json)：109 篇主体及原目录别名。
6. [原目录 JSON](directory.json)：110 条原始顺序及直达链接。
7. [统计与校验](summary.json)、[校验记录](verification.json)。
8. [高频主题参考答案](04_高频主题参考答案.md)：21 个高频主题、80 组代表性问答，包含口述结论、工程取舍、追问与错误边界；不是对全部 1,581 次问项逐条作答。
9. [参考来源与版本说明](05_参考来源与版本说明.md)：官方规范、文档、源码与公开标准草案；[来源核对记录](answer_sources.json)、[答案校验](answers_verification.json)。

## 口径与重要限制

- **问项不是补写的逐字面试实录**：作者有时只写「GMP模型」「项目深挖」等简写考点；照原文保留，不扩写成未记载的问题。自我介绍、项目介绍、HR 谈话要求和候选人反问也纳入，并可在逐篇记录中辨认。
- 原文一行包含多个相关追问时，作为一条问项完整保留；不声称上述数量是拆到最小子问的数量。算法题仅采集作者写出的题目/要求，不猜测未记载的题干、约束或答案。
- 跨公司重复问题不从逐篇记录或 questions.json 删除；分类题库仅做文字层面的合并，**未做语义去重**，相似题仍保留。
- 每条只有一个主分类，跨领域内容另外打主题标签；高频主题允许重叠，覆盖篇数与主分类问项数不是同一指标。
- 只取帖子主体，排除评论区、推荐帖、导航、点赞、登录提示。主体内的表情图片在问项中移除；主体快照保留原标记。
- 原文错别字、非标准术语、残缺表述不擅自纠正或解释。例如「langgragh」「AI 主流还发场景」「Red set nx 错误释放所有什么场景」「RAG 的原理你」「NFS 和 VPC 区别」「scale 和 workflow」等，须结合语境自行核实；采集不等于认可其中技术前提。
- 原目录与实际帖名不一致时，两者都保留。P013「wxg」与目录第 14 条「远志」链接相同：保留别名，但正文/题目只算一次；不推断哪个公司名正确。
- 日期只标本次采集日期；源页「已编辑」「已过」「下周」等是作者发表时的叙述，**不代表 2026-11-16 的招聘状态**。
- 原始采集文件只保留问项，未补造原题；后续参考答案独立保存在 04 文档，明确区分原题、扩展解释、规范事实与工程建议。

## 主分类统计

| 分类 | 问项出现次数 | 文字合并后 |
|---|---:|---:|
| Agent 架构、运行时、记忆与多 Agent 编排 | 288 | 287 |
| MCP、Tool、Skill 与 A2A 协议 | 91 | 89 |
| RAG、知识库、向量检索与数据维护 | 49 | 49 |
| 大模型、Prompt、模型选型与效果评测 | 96 | 96 |
| AI 编程、Harness、SDD 与研发效能 | 176 | 176 |
| Go 语言与运行时 | 40 | 40 |
| Python 语言与并发 | 13 | 13 |
| C++、Java 与其他语言基础 | 33 | 33 |
| 前端、浏览器与 Web 开发 | 18 | 18 |
| 操作系统、网络与通用并发基础 | 65 | 65 |
| 数据库、Redis、缓存与查询优化 | 49 | 49 |
| 分布式系统、中间件与软件架构 | 113 | 113 |
| 云原生、部署运维、故障排查与安全 | 98 | 98 |
| 算法、手写代码与数学概率 | 44 | 44 |
| 项目深挖、业务理解与系统设计 | 232 | 226 |
| 职业规划、行为面试、HR 与反问 | 176 | 176 |

## 完整采集目录（原顺序）

| 序号 | 原目录标题 | 状态 | 问项数 | 原帖 |
|---:|---|---|---:|---|
| 1 | [互动影游小厂 AI全栈开发 一面](01_逐篇面经与问题.md#p001) | 已采集 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/24e01f1d510a486b92efa795b4835669) |
| 2 | [互动影游 全栈开发 二面](01_逐篇面经与问题.md#p002) | 已采集 | 8 | [直达](https://www.nowcoder.com/feed/main/detail/1665fbb876aa4da6aa68fd21a576c549) |
| 3 | [长城证券 AI全栈开发 一面](01_逐篇面经与问题.md#p003) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/aa720c49cec348fea797bf0731b06930) |
| 4 | [广发证券 AI研发 一面](01_逐篇面经与问题.md#p004) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/be11801cff834c7f8731c210e7d15483) |
| 5 | [广发证券 AI研发 二面](01_逐篇面经与问题.md#p005) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/f3fd1598004b4121b51927908c107a34) |
| 6 | [广发证券 AI研发 三面](01_逐篇面经与问题.md#p006) | 已采集 | 8 | [直达](https://www.nowcoder.com/feed/main/detail/85b45754b5a64eeea54384378275a7ce) |
| 7 | [广发证券 AI研发 四面](01_逐篇面经与问题.md#p007) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/6715d77233254a73b7d6b369b17927f4) |
| 8 | [九坤 量化开发 一面](01_逐篇面经与问题.md#p008) | 已采集 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/8ff64597c11e4272b742d0d1ec12647c) |
| 9 | [平安证券 全栈开发 一面](01_逐篇面经与问题.md#p009) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/2d99a5b5c27c4d55ba87869790f8a5de) |
| 10 | [360 ai agent 一面](01_逐篇面经与问题.md#p010) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/b1903a3fe061470694dd3e7d1c33bfab) |
| 11 | [360 agent开发 二面](01_逐篇面经与问题.md#p011) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/c72671706e314ce08d3c371685d7f70b) |
| 12 | [360 agent开发 hr面](01_逐篇面经与问题.md#p012) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/ba377c517a50478fbde8a1077970f9d6) |
| 13 | [wxg 全栈开发 一面](01_逐篇面经与问题.md#p013) | 已采集 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/513a8a3fa27f4fa889ed5fbd61d1a0bc) |
| 14 | [远志 全栈开发 一面](01_逐篇面经与问题.md#p013) | 与 P013 同链接，不重复计数 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/513a8a3fa27f4fa889ed5fbd61d1a0bc) |
| 15 | [snapmaker web 全栈 一面](01_逐篇面经与问题.md#p015) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/bf68837197fe433d83989f74a506e832) |
| 16 | [卓驭 agent开发 一面](01_逐篇面经与问题.md#p016) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/f9be60e7b3c54750a57b37d5d200d1e5) |
| 17 | [自变量 agent平台开发 一面](01_逐篇面经与问题.md#p017) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/1d05dbe48b314a81804c2ffdd51ab569) |
| 18 | [平安银行 AI开发 一面](01_逐篇面经与问题.md#p018) | 已采集 | 34 | [直达](https://www.nowcoder.com/feed/main/detail/e72c4b75edc245349f79e20d44834301) |
| 19 | [浦发银行 AI开发 一面](01_逐篇面经与问题.md#p019) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/c200fd35c881415086928e113028e4c8) |
| 20 | [滴滴 全栈开发 一面](01_逐篇面经与问题.md#p020) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/fdfdc68a64304d2ebccdebd81a3c83d5) |
| 21 | [滴滴 全栈开发 二面](01_逐篇面经与问题.md#p021) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/769a04d2a0ff4b2aad603d5ceac135dd) |
| 22 | [滴滴 全栈开发 三面](01_逐篇面经与问题.md#p022) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/43a6a546ea444a9b8bdf11fbe62d6528) |
| 23 | [滴滴 全栈开发 hr面](01_逐篇面经与问题.md#p023) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/cd06837b102f4451adbfcd9a66b903d9) |
| 24 | [天行 全栈开发 一面](01_逐篇面经与问题.md#p024) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/9ebc4c02113349ff8f21adb84a166228) |
| 25 | [蚂蚁 财富 全栈开发 一面](01_逐篇面经与问题.md#p025) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/8e2141959212494f8da61bd98503b528) |
| 26 | [蚂蚁 复活赛 agent开发 一面](01_逐篇面经与问题.md#p026) | 已采集 | 21 | [直达](https://www.nowcoder.com/feed/main/detail/39451cad5d2245b491d16778f2a9ca01) |
| 27 | [蚂蚁 复活赛 agent开发 二面](01_逐篇面经与问题.md#p027) | 已采集 | 18 | [直达](https://www.nowcoder.com/feed/main/detail/beae35cec366487a918abee5421216f2) |
| 28 | [千寻智能 平台开发 一面](01_逐篇面经与问题.md#p028) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/0710cc2eecc9444299dc38be78de3f76) |
| 29 | [千寻智能 全栈开发 二面](01_逐篇面经与问题.md#p029) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/aa9d624ef29445b6b62ae2aa25695b2f) |
| 30 | [千寻智能 平台开发 hr面](01_逐篇面经与问题.md#p030) | 已采集 | 6 | [直达](https://www.nowcoder.com/feed/main/detail/8b6c92305cfd4db1a77b5b645d6f155b) |
| 31 | [联信 go开发 一面](01_逐篇面经与问题.md#p031) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/3a71a3df3d84412a96d4207ba9e683e0) |
| 32 | [QH硬件初创 agent开发 一面](01_逐篇面经与问题.md#p032) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/d3ed7d6441c34ecf8d5a77b0c74c284d) |
| 33 | [QH硬件初创 二面](01_逐篇面经与问题.md#p033) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/cd146e673d604a948c9de74cc6e95176) |
| 34 | [久尺todesk 全栈 一面](01_逐篇面经与问题.md#p034) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/85f9537ded2c42499793808d55cf9aa7) |
| 35 | [久尺todesk 全栈开发 二面](01_逐篇面经与问题.md#p035) | 已采集 | 26 | [直达](https://www.nowcoder.com/feed/main/detail/49809d530c1b4219bf9ef9e143da2852) |
| 36 | [转转 FDE 线下面试](01_逐篇面经与问题.md#p036) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/6204344a50a04c46a6220b2d73c426bc) |
| 37 | [csig 全栈开发 一面](01_逐篇面经与问题.md#p037) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/09592a6a2f3e4825a6b8eade28ff3486) |
| 38 | [CSIG 二面](01_逐篇面经与问题.md#p038) | 已采集 | 6 | [直达](https://www.nowcoder.com/feed/main/detail/c36ad5614e4f4e9388723672a8fc166c) |
| 39 | [超参数 agent开发 一面](01_逐篇面经与问题.md#p039) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/8e77c295f6cb4cd4b709d14804afb987) |
| 40 | [阿里国际 agent中台 一面](01_逐篇面经与问题.md#p040) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/960e56063bf84714a2b8d3b53bfc2552) |
| 41 | [阿里国际 agent 二面](01_逐篇面经与问题.md#p041) | 已采集 | 22 | [直达](https://www.nowcoder.com/feed/main/detail/b163baeb304e432d9b4c9c218ed467fa) |
| 42 | [阿里国际 agent开发 三面](01_逐篇面经与问题.md#p042) | 已采集 | 26 | [直达](https://www.nowcoder.com/feed/main/detail/747f07e71f4448bebdce6ada5de800cd) |
| 43 | [阿里国际 agent开发 hr面](01_逐篇面经与问题.md#p043) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/3a39ff1f5e5a49febee53b78831f3965) |
| 44 | [同花顺 agent开发 一面](01_逐篇面经与问题.md#p044) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/89dde87cceb142d09e90dead6e9e5aa3) |
| 45 | [同花顺 agent开发 三面](01_逐篇面经与问题.md#p045) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/88c55ee65af04ac98c218b9d17c47a71) |
| 46 | [b站 agent开发 一面](01_逐篇面经与问题.md#p046) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/ffe029cd569348ae88def6848218092d) |
| 47 | [b站 agent开发 二面](01_逐篇面经与问题.md#p047) | 已采集 | 20 | [直达](https://www.nowcoder.com/feed/main/detail/794d53d2d5b4437eb47cb606910c8fa1) |
| 48 | [b站 agent开发 三面](01_逐篇面经与问题.md#p048) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/14d7f7ffffe74f45a8b3bce4c677d927) |
| 49 | [b站 agent开发 hr面](01_逐篇面经与问题.md#p049) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/6855477ef53a4c41803ca9c4c74a393e) |
| 50 | [贵阳 小厂 一面](01_逐篇面经与问题.md#p050) | 已采集 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/3b735e42d8d04876b374eb3934715e5a) |
| 51 | [拼多多 基础平台开发 一面](01_逐篇面经与问题.md#p051) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/fff50c196dc142b5852c242ab4fb95ce) |
| 52 | [拼多多 基础平台开发 二面](01_逐篇面经与问题.md#p052) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/8d08de77b3dc41fc8136afe689f4933d) |
| 53 | [浦银金科 全栈开发 一面](01_逐篇面经与问题.md#p053) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/8b4074225f714bc58e9a7045aa56db44) |
| 54 | [唯品会 agent开发 一面](01_逐篇面经与问题.md#p054) | 已采集 | 27 | [直达](https://www.nowcoder.com/feed/main/detail/64c0631bfa1d4dfa9be3d5956f8a3b97) |
| 55 | [唯品会 agent开发 二面](01_逐篇面经与问题.md#p055) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/33f007f02f1f4090b38194314163d598) |
| 56 | [moka agent开发 一面](01_逐篇面经与问题.md#p056) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/520a8fd058b64965a036b5c92376fc90) |
| 57 | [微博 智搜 一面](01_逐篇面经与问题.md#p057) | 已采集 | 6 | [直达](https://www.nowcoder.com/feed/main/detail/5ebb27f4c9b040e5967d2b0f2eafcbca) |
| 58 | [智元 cpp 一面](01_逐篇面经与问题.md#p058) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/64ff21f2197f468485b4cea545ea5907) |
| 59 | [懂车帝 agent开发 一面](01_逐篇面经与问题.md#p059) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/8d84590d7efe4c78943b28708b4395f2) |
| 60 | [懂车帝 全栈开发 复活赛 一面](01_逐篇面经与问题.md#p060) | 已采集 | 26 | [直达](https://www.nowcoder.com/feed/main/detail/ed19194fefb943529e33697a50601114) |
| 61 | [懂车帝 复活赛 全栈开发 二面](01_逐篇面经与问题.md#p061) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/e094947868cc44aea148b7a38e974ad6) |
| 62 | [深信服 agent开发 一面](01_逐篇面经与问题.md#p062) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/45b40914f438434b88b60a21e3d5ec1e) |
| 63 | [深信服 agent开发 hr面](01_逐篇面经与问题.md#p063) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/f4f2010c48f94f88b696173f2fa5ffcb) |
| 64 | [深信服 agent 三面](01_逐篇面经与问题.md#p064) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/b64e8fddbfc642ec9aa33bcdb9aab9aa) |
| 65 | [虾皮 agent开发 一面](01_逐篇面经与问题.md#p065) | 已采集 | 10 | [直达](https://www.nowcoder.com/feed/main/detail/c831cf23b7da46e3b6f460d0ed2a4875) |
| 66 | [虾皮 agent 二面 已](01_逐篇面经与问题.md#p066) | 已采集 | 7 | [直达](https://www.nowcoder.com/feed/main/detail/345b668e35a9451bb397a9189dfdc943) |
| 67 | [广州报业 agent开发 一面](01_逐篇面经与问题.md#p067) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/f3a38b6580714965bfeac1cadeadabe9) |
| 68 | [小满科技 agent开发 一面](01_逐篇面经与问题.md#p068) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/5f3df51243ad425c83e81e359ce82c36) |
| 69 | [百度 服务端开发 一面](01_逐篇面经与问题.md#p069) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/68342ea9b032419f9a2f0ff20423a282) |
| 70 | [小红书 全栈开发 一面](01_逐篇面经与问题.md#p070) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/fc049ba49e77409298a532c10947d5de) |
| 71 | [小红书 生态全栈开发 二面](01_逐篇面经与问题.md#p071) | 已采集 | 23 | [直达](https://www.nowcoder.com/feed/main/detail/9b438a5f19b248de9ca33064dded22b8) |
| 72 | [久尺todesk 全栈开发 三面](01_逐篇面经与问题.md#p072) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/612c668b6132434c82adc655a52ccbcb) |
| 73 | [电信 Golang工程师 一面](01_逐篇面经与问题.md#p073) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/b727536203bc4741808a81e9e2c17d45) |
| 74 | [中电信 管控agent 二面](01_逐篇面经与问题.md#p074) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/cd2b942850dd46679b681567e733fdb0) |
| 75 | [电信 golang开发 三面](01_逐篇面经与问题.md#p075) | 已采集 | 19 | [直达](https://www.nowcoder.com/feed/main/detail/11fd5a6821ed422c832662b1ab5bc1e0) |
| 76 | [高德 agent开发 一面](01_逐篇面经与问题.md#p076) | 已采集 | 12 | [直达](https://www.nowcoder.com/feed/main/detail/0c02771670284a2cad2aab983294580b) |
| 77 | [高德地图 agent开发 二面](01_逐篇面经与问题.md#p077) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/0208597586e744c884bdc571dc441fad) |
| 78 | [步乐 平台开发 一面](01_逐篇面经与问题.md#p078) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/622f8daf8c4f4bf2986b6ddce7536f64) |
| 79 | [阿里 agent开发 一面](01_逐篇面经与问题.md#p079) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/6b51e5798cd14717bdcb60ca54ca6f11) |
| 80 | [阿里淘天 agent开发 二面](01_逐篇面经与问题.md#p080) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/061b68e50121468ca1f882bef5c957f4) |
| 81 | [阿里淘天 agent开发 三面](01_逐篇面经与问题.md#p081) | 已采集 | 23 | [直达](https://www.nowcoder.com/feed/main/detail/b6b453976c2d4e43a872054d695c2fe2) |
| 82 | [量化开发 一面](01_逐篇面经与问题.md#p082) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/e5b322e81efc442f91d4702713dc5558) |
| 83 | [阿里千问 agent infra 一面](01_逐篇面经与问题.md#p083) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/10d5334563244bc4a248c155b71fb083) |
| 84 | [叉车机器人 cpp 一面](01_逐篇面经与问题.md#p084) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/90f3962e64e34f61a242e612379eedbb) |
| 85 | [顺丰 agent开发 一面](01_逐篇面经与问题.md#p085) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/7cab90ca59084f64bc19d1cb13935937) |
| 86 | [顺丰 agent开发 二面](01_逐篇面经与问题.md#p086) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/93a26b84a6634558b7228bf350c709b5) |
| 87 | [基动 agent 一面](01_逐篇面经与问题.md#p087) | 已采集 | 25 | [直达](https://www.nowcoder.com/feed/main/detail/64e31a28581b4e21a1e8e1aee236b6b4) |
| 88 | [阿里国际 业务agent 一面](01_逐篇面经与问题.md#p088) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/3c305b0c1565458ba05c9906322f5327) |
| 89 | [电信 风控agent 二面](01_逐篇面经与问题.md#p089) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/22e18a3d20734429aec41b37744beadc) |
| 90 | [电信 golang开发 二面](01_逐篇面经与问题.md#p090) | 已采集 | 20 | [直达](https://www.nowcoder.com/feed/main/detail/99dc4d2ad46446a7bf1173a4d64d3f5a) |
| 91 | [字节抖音 社招 一面](01_逐篇面经与问题.md#p091) | 已采集 | 21 | [直达](https://www.nowcoder.com/feed/main/detail/a385d6cc457d47c99c03cb8ea752ab89) |
| 92 | [招聘 agent 二面](01_逐篇面经与问题.md#p092) | 已采集 | 32 | [直达](https://www.nowcoder.com/feed/main/detail/16675d793c0c42e8a6b46d42fb561561) |
| 93 | [网易 全栈开发 一面](01_逐篇面经与问题.md#p093) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/0b702f3f811b4952a98d76c232ed2db6) |
| 94 | [快手 中台全栈开发 一面](01_逐篇面经与问题.md#p094) | 已采集 | 16 | [直达](https://www.nowcoder.com/feed/main/detail/69f817c5e6b147b1868aa41b07e835ba) |
| 95 | [快手 全栈开发 二面](01_逐篇面经与问题.md#p095) | 已采集 | 15 | [直达](https://www.nowcoder.com/feed/main/detail/3526c4c9bf1c4b80acdfa9ee7bacd548) |
| 96 | [遥望科技 agent开发 hr面](01_逐篇面经与问题.md#p096) | 已采集 | 20 | [直达](https://www.nowcoder.com/feed/main/detail/0021afda5c754f7d85ae6c965063dacd) |
| 97 | [阿里控股 agent开发 一面](01_逐篇面经与问题.md#p097) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/85c8873901c744688fa7267145b9b3ce) |
| 98 | [阿里控股 AI全栈开发 二面](01_逐篇面经与问题.md#p098) | 已采集 | 17 | [直达](https://www.nowcoder.com/feed/main/detail/a11a3a9e0d824969b44db5bb2149ef9f) |
| 99 | [阿里千问 agent开发 一面](01_逐篇面经与问题.md#p099) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/463438ee0d9e403b98e8578a05ba4e3f) |
| 100 | [阿里 千问 平台开发 复活赛 一面](01_逐篇面经与问题.md#p100) | 已采集 | 19 | [直达](https://www.nowcoder.com/feed/main/detail/141447389dab4e8e9ca6db742a514f39) |
| 101 | [传音 数据平台开发 一面](01_逐篇面经与问题.md#p101) | 已采集 | 11 | [直达](https://www.nowcoder.com/feed/main/detail/ebc4abbf1c404d0e8d7a3eedf701480e) |
| 102 | [迅雷 全栈开发 一面](01_逐篇面经与问题.md#p102) | 已采集 | 18 | [直达](https://www.nowcoder.com/feed/main/detail/d4e2c561aada41479bfd6ee99eb3e38d) |
| 103 | [阿里ATH infra 平台开发 一面](01_逐篇面经与问题.md#p103) | 已采集 | 20 | [直达](https://www.nowcoder.com/feed/main/detail/9b6badb8d83a4306ad8fb9e50e58cace) |
| 104 | [知识科技 数据agent 一面](01_逐篇面经与问题.md#p104) | 已采集 | 14 | [直达](https://www.nowcoder.com/feed/main/detail/9c52d114887148bd88dac675229d8dfe) |
| 105 | [知识科技 数据平台 二面](01_逐篇面经与问题.md#p105) | 已采集 | 21 | [直达](https://www.nowcoder.com/feed/main/detail/c478feeef29340caac7b8c44d5a6c5e4) |
| 106 | [拼多多 agent 复活赛 一面](01_逐篇面经与问题.md#p106) | 已采集 | 25 | [直达](https://www.nowcoder.com/feed/main/detail/2109cf8eb0254507911fbf86bcbf51e4) |
| 107 | [viture agent平台开发 一面](01_逐篇面经与问题.md#p107) | 已采集 | 13 | [直达](https://www.nowcoder.com/feed/main/detail/c4c614b12d564af3b37c30c241072973) |
| 108 | [孝量化 后端开发 一面](01_逐篇面经与问题.md#p108) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/87319d167f494d28a361ffd4a0215e06) |
| 109 | [memtensor 全栈开发 一面](01_逐篇面经与问题.md#p109) | 已采集 | 31 | [直达](https://www.nowcoder.com/feed/main/detail/6af8a31964434012a95de8f4c16403b8) |
| 110 | [商汤 全栈开发 一面](01_逐篇面经与问题.md#p110) | 已采集 | 9 | [直达](https://www.nowcoder.com/feed/main/detail/4dab7dac5d114250a5b8025bb05cf17f) |
