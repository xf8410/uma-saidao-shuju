# 7. 全力冲刺（全開スパート / RunAtFullSpeed）与两段式固有技

> 用户指正：全力全开 ≠ 末脚。两者是**两个独立状态**——末脚（lastspurt）是末段加速的判定，全力冲刺（run_at_full_speed）是末脚判定成功**之后**的冲刺阶段状态。

## 状态变量
- `run_at_full_speed_random==1`：全力冲刺阶段的随机位置（触发窗口变量）
- 求值器：SkillTriggerRunAtFullSpeedRandom（继承 SkillTriggerDistanceBase）
- 运行时：IHorseRunAtFullSpeedCalculator{UpdateRunAtFullSpeed, get_IsRunAtFullSpeed}

## 杏目固有 Peerless Heroine（skill_data id=101291 全行实查）

两段式固有，一个 id 带两组 condition/ability：

**段1（condition_1）**：
```
phase==1 & corner!=0 & order_rate<=50 & ground_type==1
```
- ability_type_1_1 = **22**（CurrentSpeedNaturalDecel，解除自然减速）
- float_ability_value = 4500（0.45）
- float_ability_time = 30000（万分秒 = 3.0s）
- float_cooldown_time = 5000000（500s）
- ability_time_usage = 1（Direct 固定时长）
- target_type = 1（目标=自己）
- popularity_add_param_1 = 3, value = 60（人气加成）

**段2（condition_2）**：
```
is_activate_other_skill_detail==1 & run_at_full_speed_random==1 & order<=3 & distance_type==3
```
- ability_type_2_1 = **48**（AddExPower！）
- float_ability_value = 4000（0.4）
- float_ability_time = 20000（2.0s）
- 段2 要求同 id 的**段1（detail 1）已发动**——`is_activate_other_skill_detail==1` 就是这个链式标记

与 wiki 记录逐项吻合（触发代码/数值/持续时间/冷却 500）。

## もう一踏ん張り（id=204222 全行实查）

```
run_at_full_speed_random==1 & distance_type==3
```
- ability_type_1_1 = **48 AddExPower**，value = 2000（0.2），time = 2s，cooldown = 500s
- is_general_skill = 1（普通技能）

## ★ ability 48 = AddExPower 的机械含义

**"全力冲刺阶段强化冲刺"不是直接加速度**——ability 48 往 **ExtraTargetSpeed**（冲出额外速度段，见 04 文件 ExtraTargetSpeedParam/ExtraTargetSpeedPer）塞值，即强化"冲出判定"的那条额外速度曲线。

全开状态技能族：
- 204222：AddExPower 0.2（强化冲出）
- 204262：`run_at_full_speed_random==1` → ability 22（解除自然减速）0.25

## run_at_full_speed 全部使用者（7 条，全量）

| id | 条件 | 备注 |
|---|---|---|
| 101291 | 段2: is_activate_other_skill_detail==1 & run_at_full_speed_random==1 & order<=3 & distance_type==3 | 杏目固有段2 |
| 101361 | 段2: is_activate_other_skill_detail==1 & run_at_full_speed_random==1 & **is_used_skill_id_with_detail_one==204452** | 跨技能链式（段1=lastspurt==2 富余末脚）|
| 204222 | run_at_full_speed_random==1 & distance_type==3 | もう一踏ん張り |
| 204262 | run_at_full_speed_random==1 | 普通版 |
| 100503111 | 段2: ... & run_at_full_speed_random==1 & track_id==10005 & base_stamina>=1000 | 中山限定+耐力门槛 |
| 111801111 | 段2: ... & run_at_full_speed_random==1 & order_rate 20~50 | 差马固有 |
| 111801211 | 段2: ... & run_at_full_speed_random==1 & order_rate 20~50 | 同上另一段 |

## 两段式固有技的通用机制（结构级）

1. 一个 skill id 有 condition_1 / condition_2 两组独立段（各自带 ability×3 / time / cooldown / target / popularity）
2. `is_activate_other_skill_detail==1` = "同 id 的 detail 1（第一段）发动过"标记 → 段2 解锁
3. `is_used_skill_id_with_detail_one==<id>` = 更强链式：**指定 detail 1 用的技能 id**（跨技能链，101361→204452）
4. 段2 触发窗口常用 run_at_full_speed_random（全力冲刺段）或 is_lastspurt（末脚段）——全部可静态枚举

## 其他新变量
`run_at_full_speed_random` / `is_activate_other_skill_detail` / `is_used_skill_id_with_detail_one` / `compete_fight_count`（101031 缠斗计数>0）
