# 4. 比赛机制参数结构（IL2CPP 全字段级）

> 所有 XxxParam 的**具体数值**在 RaceParamDefine 资产里，须进比赛 dump；本文件是结构+语义。

## 焦躁 Temptation（比赛内失控状态）
- TemptationMode：Null / PositionSashi / PositionSenko / PositionNige / Boost（技能强制）
- TemptationParam 12参数：
  - LotSectionMin/Max：可触发区间（distance_rate）
  - StartPerVal1：起始概率；ForceEndTime：强制结束时间（技能可改 SetForceEndTimeBySkill）
  - EndCheckTime/EndPer：结束判定
  - 跑法迁移概率 6 个：OikomiToSashi/Senko/NigePer、SashiToSenko/NigePer、SenkoToNigePer（焦躁会变跑法乱窜）
- 焦躁时 HP 消耗倍率上升：HpParam.HpDecRateBaseTemptation / TemptationAndCompeteTopNige

## 封堵 Block
- BlockParam：FrontBlockDistanceGap/LaneGap、SideBlockDistanceGap/LaneGap、FrontBlockMaxSpeedRateMin/Max（被前马卡时限速）
- BlockedSideMaxContinueTimeCoef{Threshold, Multiply}：侧面被卡持续时长上限（智力系数）

## 末脚判定 LastSpurt
- LastSpurtCalcResult：True / TrueExceedNeedMaxHp / FalseBelowNeedMinHp / False
- 末段开跑 = 体力够不够的判定；FalseBelowNeedMinHp = 体力不足

## 末段前竞争 CompeteBeforeSpurtParam（33 参数）
- Start/EndSection、CheckIntervalSec、CoolDownSec
- DistanceFromTopPerCoef/Exponent：与头马距离的竞争意愿曲线
- NearDistanceForward/Backward + PerExponent
- SameRunningStyleCoefOfNearCharaNumCoef
- SpeedUpPowDivisor/Exponent/Coef + SpeedUpGutsDivisor/Exponent/Coef（力/根性驱动抢位）
- StaminaKeep：WizDivisor/WizExponent（智力决定体力保持判断）+ RandomRangeMin/Max
- ConsumeStaminaValue + 跑法系数数组 + 赛道距离系数数组（争位额外耗体力）
- MinorBonus 系

## 位置保持 PositionKeep（跑法执行）
- PositionKeepMode：SpeedUp / Overtake / PaseUp / PaseDown / PaseUpEx
- PositionKeepParam 37参数：CheckInterval/CoolDown、Start/End/ContinueSection、SpeedUp/Overtake 的 StartPerVal1×BaseTargetSpeedMultiply×EndDistanceDiff（Oonige 大逃差分）、PaseUpDown DistanceDiff Min/Max×跑法、PaseDownBaseTargetSpeedMultiply+PhaseMiddle 变体、PaseUp(Ex)、PaseMaker 换位三参数

## 省力系统 ConservePower（体力经济核心）
- IncreaseConservePowerMode：None / PositionKeepPaceDown（PaseDown 降速时积累）/ NotActivatePositionKeep
- DecreaseConservePowerMode：None / CompeteTop（争第一消耗）/ Temptation（焦躁消耗）
- ConservePowerParam 11参数：ReleaseAccelCoef/ReleaseDeclCoef、ReleaseAccel 跑法×距离数组、DecreaseAccelCoef 数组、ActivityTimeCoef+按距离数组、DefaultCoolDownTime、Increase/Decrease 系数数组、ReleasableActivityTimeThreshold
- 语义：PaseDown 省的力在关键时刻以加/减速度释放——逃马省力、争顶/焦躁耗力

## 目标速度体系
- BaseTargetSpeedParam：PhaseBaseTargetSpeedPerArray[Start/Middle/End/Last] + Ex版 + RandomMinus Val1/Val2 + RandomPlusVal1 + PhaseEndBaseTargetSpeedCoef
- 求值器：GetBaseTargetSpeed / GetBaseTargetSpeedWithoutRandom（随机抖动开关）
- ExtraTargetSpeedParam 10参数：Start/Max 的 Param+Foundation、三种 AccelSuppress、RawSpeedParam、AccelExponent、PowerAdjustCoef
- ExtraTargetSpeedPer{DistanceMin/Max, HpMin/Max, MinCoef/MaxCoef}：距离×体力二维插值
- StaminaLimitBreakBuffParam：TargetSpeedForStaminaCoef/ForWholeCoef、DistanceCoef{Threshold,Multiply}、RandomTable{TableType,Lower,Upper,Probability}、ChangeProbabilityByPower
- PhaseAccelCoef{Start/Middle/End/Last}

## 坡道 Slope
- SlopeParam 6参数：SlopePerThreshold、UpSlopeAddSpeedVal1、DownSlopeAddSpeedVal1/Val2（下坡加速双段）、DownSlopeAddSpeedStartWizRate（下坡加速起始=智力相关率）、DownSlopeAddSpeedEndPer
- HorseSlopeCalculator：SlopePer2SlopeType / CalcUpSlopeAddSpeed / CalcDownSlopeAddSpeed / CalcDownSlopeAccelStart/EndPer
- CourseSlope{Start,End,SlopeType,SlopePer,IsContinuousSameTypeSlope}

## 智力(Wiz)作用面
- WizCoef{WizThreshold, Multiply}：智力阈值→倍率（体力保持判断、被封堵时长）
- WizLimitBreakBuffParam{PhaseParamArray, TargetAbilityTypeArray, SkillSelectionRuleByRarity, WizCoefArray, CourseDistanceCoefArray}
- HorseVisibleCalculator：视野=车道距离窗口 VISIBLE_LANEDISTANCE_MIN/MAX

## 心态（赛前）
- race_motivation_rate：絶不調9600/不調9800/普通10000/好調10200/絶好調10400（万分比，±4%）
- RaceParameter.AdjustByMotivation：MotivationCoef 乘进全五维（统一乘区）
- 心情枚举 Min/Low/Middle/High/Max + Random

## 出闸
- HorseDelayCalculator：IsGoodStart/IsBadStart、GOOD_START_DELAY_RATE / BAD_START_DELAY_RATE
- HorseRaceInfo.get_IsGoodStart/IsBadStart/CalcDelayTime/UpdateStartDash、StartDelayFix（技能修正）
- StartDashState{None, BadStart, GoodStart}

## 场地状态消耗（GroundModifierParam）
- {addSpeed, addPower, multiHpSub}——不在 master.mdb，运行时静态单例构造
- HorseRaceInfo.InitGroundConditionParam 反汇编实锤：单例 +0xC8/+0xD0 数组（芝/沙各一组 GroundModifierParam[4]），按 ground 1..4 分支取值
- 数值待进比赛 object_dump

## 状态变量总表（JikkyoTrigger.Cmd_* 151 个）
- 天气场地：Cmd_Weather/Ground/GroundCondition/GroundType/Course/CourseSetId/CourseDis/CourseAround/GroundChange(中途换场)
- 过程：Cmd_Order/BackOrder/OrderRate/Distance/Length/LastSpurt/HPRate/StaminaZeroDistance(体力归零观测点)/Temptation/RelativeSpeed/RankChange/TimeRankChange/Between/DistanceApproach/Away/FinishLength/Block/Positioning
- 几何：Cmd_LastCorner/DistanceToLastCorner/HomeStraight/BackStraight(正反直线)/Event_Corner/Event_Straight/Event_Distance
- 角色：Cmd_CharaID/RunStyle/ProperGround/ProperDistance/ProperRunningStyle/Motivation/ParamSpeed/.../WizRank/Popularity/SkillActivate/SkillReceived/SkillExtension/GoodStart/BadStart
- 模式：Cmd_RaceIdRange/RaceType/Grade/RaceGroup/SingleMode* 全剧本/WinSaddle/Undefeated/WinRace

## OverRun 大逃
- 专属计算器：HorseAccelCalculatorOverRun/HorseTargetSpeedCalculatorOverRun/HorseTargetLaneCalculatorOverRun
- 结果系统：RaceOverRunResult{Base, LongChamp, America, Null}；race_overrun_pattern 表（纯表现层）

## 表现层（简记）
- CourseRacecourseParam/RaceCourseCameraEvent(四套相机)/CourseStartGate/CourseGoalGate/RaceCourseDistanceTypeValue
- race_env_define season×weather×timezone → 环境资源 id（纯视觉）
