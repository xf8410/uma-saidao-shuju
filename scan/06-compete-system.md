# 6. 比拼（Compete）系统全参数——追比/缠斗/守位的完整状态机

## 三层结构
1. **CompeteTop（争顶）**：两马并列争第一的对抗
2. **CompeteFight（缠斗/挂かり合い）**：并排互顶拉锯
3. **SecureLead（守位）**：领跑方保优势（逃马专属逻辑）

## CompeteTopParam（15参数全结构）
| 字段 | 类型 | 语义 |
|---|---|---|
| CheckStartDistance | float | 检查起始距离 |
| CheckEndSection / EndSection | int | 检查/生效区间（distance_rate 段）|
| NigeCount / OonigeCount | int | 逃马/大逃计数（按对面跑法触发）|
| DistanceGap1 / DistanceGap2 | float | 两段距离接近阈值 |
| LaneGap1 / LaneGap2 | float | 两段车道接近阈值 |
| TimeCoef1/2/3 | float | 比拼持续三档时间系数 |
| AddParam1Coef1/2/3 | float | 比拼加成三档（对应 TimeCoef）|

流程：进入区间 → 判定接近（距离+车道双阈值）→ 持续三档时间 → 每档给加成。

## CompeteFightParam（14参数全结构）
| 字段 | 类型 | 语义 |
|---|---|---|
| DistanceGap / LaneGap | float | 缠斗判定阈值 |
| SpeedGap | float | 速度差阈值（咬住对方才算缠斗）|
| TargetContinueTime / TargetContinueDistance | float | 缠斗持续时长/距离 |
| TargetOrderPer | int | 目标名次概率 |
| HpPer / HpPer2 | int | **两档体力比**（消耗/判定关键档）|
| AddParam1Coef1/2/3 | float | 加成组1（三档）|
| AddParam2Coef1/2/3 | float | 加成组2（三档）|
- HorseCompeteFightRunningNumber._runningNumber：缠斗进行计数器

## SecureLeadParam（19参数全结构）——逃马守位
| 字段 | 类型 | 语义 |
|---|---|---|
| StartSection / EndSection | int | 生效区间 |
| CheckIntervalSec / CoolDownSec | int | 检查间隔/冷却 |
| PerCoef | float | 触发率系数 |
| ActiveSec | int | 生效时长 |
| SafetyLeadAddend | int | 基础安全领先差 |
| SafetyLeadCoef | float | 安全差系数 |
| SafetyLeadRunningStyleDistanceArray | 数组 | **安全差按 我方跑法(含Oonige) × 对方跑法 二维查表**（Threshold 按 OpponentRunningStyleDistanceThreshold）|
| SpeedUpGutsDivisor/Exponent/Coef | float | 守位加速（根性驱动）|
| SpeedUpRunningStyleCoefArray | 数组 | 跑法差分 |
| MinorBonusNearDistance/PerThreshold/CoefArray | | 小奖励 |
| ConsumeStaminaValue | int | 守位即时体力消耗 |
| ConsumeStaminaRunningStyleCoefArray / CourseDistanceCoefArray{Threshold,Coef} | 数组 | 守位消耗按跑法×赛道距离 |

流程：每 CheckInterval 检查领先差是否 < SafetyLead（按对方跑法查表）→ 不足则根性驱动 SpeedUp 拉开 → 持续耗体力。

## 超车目标 OvertakeTarget
- HorseOvertakeTargetCalculator：CollectOvertakeTarget / CheckOvertakeTarget / HasOverTakeTarget / get_OverTakeHorseList
- 技能条件：is_overtake==1（正在超车）/ overtake_target_time>=1（咬住目标时长）
- SkillTriggerOvertakeTargetHaveNoOrderUp/DownContinueTime：咬住目标但被压住的时长条件

## RunningStyleEx
= RunningStyle + **Oonige**（大逃=第5跑法，参与全部二维查表）

## 比拼消耗三通道（与省力系统闭环）
1. 省力值扣减：DecreaseConservePowerMode.CompeteTop
2. 逃马 HP 倍率：HpParam.HpDecRateBaseTemptationAndCompeteTopNige（被争顶时）
3. 即时 Stamina 消耗：CompeteFight/SecureLead 的 ConsumeStamina 系

末段版 = CompeteBeforeSpurt（33参数，见 04 文件），结构同源。

## 技能侧钩子
- SkillTriggerCompeteFightCount（缠斗计数）
- SkillTriggerNearHorseCount（邻近马数）
- SkillTriggerChangeOrderUp/Down ×{PhaseMiddle, PhaseEndAfter, Corner, LastSpurt, FinalCornerAfter, LaterHalf}（名次变化时机族 12 个）
- 技能条件 hp_per 与 CompeteFight.HpPer 双档呼应

## 数值缺口
CompeteTopParam/CompeteFightParam/SecureLeadParam 的具体数字在 RaceParamDefine 资产，须进比赛 dump。
