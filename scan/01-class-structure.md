# 1. 赛道类结构 + 静态表

> 2026-09-05 通过 hlpatch IL2CPP 端点全量扫描，APP-VER 2.30.0。

## 静态表（Master data，SQLite ORM）

### MasterRaceCourseSet → 行类 RaceCourseSet（赛道组主表）
| 字段 | 类型 | 语义 |
|---|---|---|
| Id | int | 赛道组 id（10001札幌…10203デルマー）|
| RaceTrackId | int | 所属竞马场 |
| Distance | int | 距离(m) |
| Ground | int | 芝/沙（1芝 2沙）|
| Inout | int | 内回り/外回り |
| Turn | int | 回转方向（1右 2左 4直线）|
| TightTrack | bool | 狭窄赛道（小回り，技能条件用）|
| RunOutside | bool | 外回走行 |
| RunUp | int | 退走距离（实际跑动=Distance+RunUp）|
| FenceSet | int | 栅栏组 |
| FloatLaneMax | int | 最大浮动赛道宽度 |
| CourseSetStatusId | int | → CourseSetStatus |
| FinishTimeMin/MinRandomRange/Max/MaxRandomRange | int ×4 | 完走时间范围 |

### MasterRaceTrack → RaceTrack（竞马场表）
Id, InitialLaneType, EnableHalfGate(半闸), HorseNumGateVariation, TurfVisionType, FootsmokeColorType, Area, OverrunResultType, FlagType, GatePanelType, GateLampType, BoardConditionType, ResultBoardType。纯表现/闸位侧。

### race_proper_ground_rate（场地适性倍率，万分比）
G=0 F=1000 E=3000 D=5000 C=7000 B=8000 A=9000 S=10000 S+=10500

### race_proper_distance_rate（距离适性 → speed/power 万分比）
F:1000/4000 E:2000/5000 D:4000/6000 C:6000/10000 B:8000/10000 A:9000/10000 S:10000/10000 S+:10500/10000

## 运行时：Gallop.RaceInfo
- 引用 RaceCourseSet/FenceSet/RaceTrack；GoalGate, RaceTrackVariationId
- RotationCategory: Undefined/Right/Left/StraightRight/StraightLeft
- GroundCondition: Good/Soft/Hard/Bad(+Random)，Weather/SubWeather/Season/Time
- **SlopeList / CornerList / StraightList**（StandaloneSimulator.CourseSlope/CourseCorner/CourseStraight）——分段几何，模拟器核心

## StandaloneSimulator 分段结构
- **CourseSlope**: StartDistance, EndDistance, SlopeType(Null/Up/Down), SlopePer(坡度%), IsContinuousSameTypeSlope
- **CourseCorner**: StartDistance, EndDistance, cornerNumber, IsFinalCorner
- **CourseStraight**: StartDistance, EndDistance, Range, frontType(StraightFrontType: Front/AcrossFront/FalseStraight伪直道), FrontTypeNumber, _isLast

## CourseParam（每赛道一份，运行时解析）
- 字段：_paramType(CourseParamType), _distance(float), _distanceOffsetPerLane, _values(int[])
- _values 按 type 有专用索引：STRAIGHT{START_END,TYPE,IS_LAST} / CORNER{NO,DISTANCE} / SLOPE{PER,LENGTH} / MOVELANEPOINT{IN_OR_OUT} / LANEMAXCHANGE{LANEMAX}
- slope PER 在 _values 里是 int（万分比→%）
- 资产路径：ResourcePath.GetCourseParamPath(courseSetId)，疑似 courses/<id>

## 消费链（运行时）
CourseEventManager.Init → CourseEventParam.InitCourseEvent → {CourseEventCorner[], CourseEventStraight[], CourseEventSlope[], FirstMoveLanePointDistance, IsExistLastStraightEvent}
RaceUtil.CalcSlopeList → CourseSlope；HorseSlopeCalculator.SlopePer2SlopeType/CalcUpSlopeAddSpeed/CalcDownSlopeAddSpeed
RaceInfo.get_SlopeList/CornerList/StraightList = 技能条件变量(slope/corner/is_last_straight)的来源

## 技能条件类（StandaloneSimulator.SkillTrigger*）
RaceTrackId / RaceTightTrack / GroundType / GroundCondition / CourseDistance / CourseDistanceType / GateNumber / GateNumberRate —— 技能"场地/距离/闸位"条件全在此挂接。变量包 = VariableRaceParameter{Weather, GroundCondition}
