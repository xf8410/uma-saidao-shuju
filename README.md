# uma-saidao-shuju — 赛马娘赛道/比赛机制挖掘档案

> 全部结论来自 2026-09-05 实机挖掘（APP-VER 2.30.0，hlpatch SO v3.27.24，IL2CPP 端点 + master.mdb SQL 直查）。
> 每一条都有工具返回为证，无推测填充；缺口如实标注。

## 目录

| 文件 | 内容 |
|---|---|
| [scan/01-class-structure.md](01-class-structure.md) | 赛道类结构：RaceCourseSet/RaceTrack/RaceInfo/CourseParam/分段几何/SkillTrigger* |
| [scan/02-mdb-track-data.md](02-mdb-track-data.md) | mdb 实值：17场地140赛道全量、race_condition 天气→马场抽签表 |
| [scan/03-skill-condition-dsl.md](03-skill-condition-dsl.md) | 技能条件 DSL：条件变量全表、双末脚变量、智力门槛族、三层判定模型 |
| [scan/04-race-mechanics-params.md](04-race-mechanics-params.md) | 比赛机制参数结构：焦躁/封堵/末脚/竞争/位置保持/省力/目标速度/坡道/心态/场地消耗/状态变量总表 |
| [scan/05-disasm-and-notes.md](05-disasm-and-notes.md) | 关键反汇编记录（InitGroundConditionParam 等）、工具层问题、查询纪律 |

## 核心成果速览

1. **赛道静态表 100%**：140 条赛道全量（距离/芝沙/内外回/转向/狭窄/浮道宽）+ 适性倍率（0~10500 万分比）
2. **天气→马场抽签表**：area 仅 999/5/6 三档；晴→良90/稍重10、阴→良78/稍重22、雨→重55/不良45；area6 特例雨天芝=重100%
3. **技能条件 = 明文 DSL**：`&`=AND `@`=OR；双末脚变量 is_lastspurt/lastspurt（2=富余）；智力门槛 1200/1000 两档
4. **比赛机制参数结构全明**：ConservePower 省力系统（PaseDown 充能、争顶/焦躁耗能）、TemptationParam 12参数（含跑法迁移概率）、PositionKeep 6模式37参数、BaseTargetSpeed 4相位+随机抖动
5. **心态**：race_motivation_rate ±4% 全五维统一乘区，赛前可见无概率分支

## 三层判定模型

1. **有效** = condition DSL 通过（纯静态）
2. **能开** = 发动窗口命中（静态可枚举+过程分布）
3. **生效** = 数值落地（效果×时长×赛道余量够不够铺）

例：迫影类下坡加速需下坡段剩余足够长度；全力全开类需 lastspurt==2（末脚富余判定）。

## 剩余缺口（须进一场比赛抓取）

1. RaceParamDefine 资产数值（所有 XxxParam 的具体数字）
2. courses/<id> 资产文件（每赛道弯道/直道/坡道精确米数）
3. GroundModifierParam 数值（重/不良场地 addSpeed/addPower/multiHpSub）

## 免责

本仓库为个人逆向学习笔记，不含游戏资源本体，不含任何绕过验证的作弊功能。
