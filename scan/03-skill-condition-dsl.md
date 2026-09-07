# 3. 技能条件 DSL（skill_data）+ 三层判定模型

## skill_data（2167 行）条件列 = 明文表达式
- `condition_1 / condition_2 / precondition_1` 列 = 条件表达式字符串
- 语法：`变量==值`（== >= <=），`&`=AND，`@`=OR
- 例：`ground_type==2&ground_condition==3@ground_type==2&ground_condition==4`（沙+重/不良）
- 求值器：StandaloneSimulator.SkillTrigger*；变量包 VariableRaceParameter{Weather, GroundCondition}

## 确认存在的条件变量（语义）
track_id(=race_course_set.id)、ground_type(1芝/2沙)、ground_condition(1良/2稍重/3重/4不良)、weather(1晴/2阴/3雨/4雪)、course_distance、distance_type(1短/2英/3中/4长)、corner(0=直线)、is_finalcorner、is_finalcorner_laterhalf、is_last_straight、slope(0平/1上/2下)、phase(0..3)、phase_firsthalf、phase_firsthalf_random、phase_random、phase_laterhalf_random、all_corner_random、straight_random、up_slope_random、down_slope_random、distance_rate、distance_rate_after_random、remain_distance、order、order_rate、bashin_diff_infront/behind、running_style(1逃2先3差4追)、base_speed/stamina/power/guts/wiz、activate_count_all、is_used_skill_id、is_lastspurt、lastspurt、is_overtake、overtake_target_time、is_surrounded、temptation_count、is_temptation、running_style_temptation_opponent_count_nige/senko/sashi/oikomi、accumulatetime、blocked_front_continuetime、infront_near_lane_time、hp_per、change_order_onetime、distance_diff_rate、is_badstart、gate_number（条件0命中）

## 变量命中统计（LIKE 计数）
distance_type 769 / corner 355 / straight 175 / ground_type 147 / track_id 96(多为disable_singlemode=1 剧情NPC技) / slope 70 / weather 12 / hp 14 / gate_number 0

## 双末脚变量（全力全开类技能）
- `is_lastspurt`：是否已进入末脚状态（0/1）
- `lastspurt`：末脚判定质量——1=判定成功 / 2=富余成功（TrueExceedNeedMaxHp 体力绰绰有余）
- IL2CPP：LastSpurtCalcResult{True, TrueExceedNeedMaxHp, FalseBelowNeedMinHp, False}

### 样例
- 100131: `is_finalcorner==1&corner!=0&distance_diff_rate<=30&distance_type==4&lastspurt==2` → TargetSpeed+0.45
- 100991: `is_lastspurt==1&order_rate<=40&>=30&ground_type==2&lastspurt==2` → Accel+0.40
- 101361: `phase==2&lastspurt==2&order_rate>=40` → CurrentSpeedNaturalDecel+0.35（解除自然减速）
- 120611: `is_lastspurt==1&phase==3` → TargetSpeed+0.35

## 智力门槛技能族（21 例）
- 固定两档：base_wiz>=1200（强化）/>=1000（基础）
- 智力做"解锁更优分支"的门槛，不做数值乘区（与 WizCoef{Threshold,Multiply} 一致）
- 代表：110871 ふわもこアワー、105502211 いざショーベラスタイム♪、103202111 ラプラスの悪魔、111902111 雪暗れに微笑む、101151 我が覇道

## 三层判定模型（核心结论）
1. **有效（condition 通过）**：skill_data condition_1/2 明文 DSL——纯静态可判
2. **能开（发动窗口命中）**：赛道静态变量可枚举 + 过程变量(order_rate/phase/hp)需分布
3. **生效（数值落地）**：效果类型×数值×时长×剩余赛道长度是否够铺
   - 例：迫影类"下坡加速"需下坡段剩余足够长度，短赛道开了也没数值
- 判定器输入 = {race_course_set, course_param(弯道坡道), entry数, race_condition 天气×马场分布枚举}
- 效果层结构：SkillAbilityType 54值（TargetSpeed=27/Accel=31/CurrentSpeed=21/HpRate=9 等）；数值=万分比；SkillAbilityTimeUsage 9值（Direct/MultiplyRemainHp/MultiplyDistanceDiffTop/AddThroughUpSlopeCount）；SkillAbilityValueLevelUsage（Normal/Ignore/Inverse）

## 马场状态相关技能（9 种模式约20技能）
良×5、稍/重/不良×5、沙+重/不良×5、沙≥重×1、芝恶×1、芝良×1、晴良×1、雨不良×1、智1200中长良×1
