# 8. 赛程表 + 攻略站交叉验证（course_param 来源打通）

## mdb 赛程三层链路（全部实查）

### race（2916 行）
id(3001=京都金杯) / group / **grade** / **course_set**(→race_course_set.id) / entry_num / is_dirtgrade / start_gate / goal_gate / ff_* 表现字段 / start_date

grade 枚举（GROUP BY 实查）：
| grade | 数量 | 语义 |
|---|---|---|
| 0 | 26 | 特殊/剧情 |
| 100 | 1324 | Pre-OP |
| 200 | 165 | OP |
| 300 | 229 | G3 |
| 400 | 357 | G2 |
| 700 | 78 | 传奇类? |
| 800 | 53 | 传奇类? |
| 900 | 158 | 日常类? |
| 999 | 256 | 剧情类? |
| 1000 | 270 | 日常类? |

### race_instance（3403 行）
id（=race_id×100+序）/ race_id / npc_group_id / **date**（年月编码）/ time / clock_time / race_number

### single_mode_program（育成赛程）
race_instance_id → {month, half, race_permission, need_fan_count, fan_set_id, reward_set_id, filly_only_flag(牡牝限定), entry_decrease(出赛数递减), grade_rate_id, reserve_program_id, random_group_id}

例：301101（京都金杯 instance）→ program 182 {month:2, half:1, need_fan_count:750, filly_only_flag:1}

single_mode_race_group：program_id → race_group_id（自由赛/分组用）

## ★ 攻略站交叉验证（ウマ娘.攻略.tools）

### race/tracks 页
与 mdb race_course_set **140 条完全一致**（各场地芝/沙数量与距离全部对上）。

### race/races/3001（京都金杯）详情页
course_set 10805（京都芝1600）的分段数据，页面 JSON 内嵌的就是 **CourseParam 原始数组**：

```json
params: [
  {id:0, type:99, length:20000, distance:0},
  {id:10805002, type:2, raceTrackCourseId:10805, distance:20000, length:50000, value:2},
  {id:10805000, type:0, raceTrackCourseId:10805, distance:70000, length:25000, value:3},
  {id:10805001, type:0, raceTrackCourseId:10805, distance:95000, length:24700, value:4},
  {id:10805003, type:2, raceTrackCourseId:10805, distance:119700, length:40300, value:1}
]
```

- **type 0 = コーナー（value=弯道号 3/4）**
- **type 2 = 直線（value=直線型：1=直線1最终直线 / 2=直線2）**
- distance / length 单位 = 万分米（20000=200m）
- 与游戏内 CourseParam{type, distance, values[]} 结构/索引**完全对应**（见 scan/01）

### 京都芝1600 完整分段（站点展示）
| 区间 | 内容 |
|---|---|
| 0-200m | 無（起始段）|
| 200-700m | 直線2 |
| 700-950m | コーナー3 |
| 950-1197m | コーナー4 |
| 1197-1600m | 直線1（最终直线）|

坡道（SLOPE{PER,LENGTH}）：
- 450-550m **+2%**（上坡）
- 550-775m **+1%**（上坡）
- 775-925m **-2%**（下坡）

相位边界（PhaseBaseTargetSpeedPer 四段的分段依据）：
- 序盤 0-267 / 中盤 267-1067 / 終盤 1067-1333 / ラストスパート 1333-1600
- ポジションキープ区間（位置保持区间）0-667

## 结论：模拟器最后一块拼图的获取路径打通

1. 攻略站有一手 course_param 数据（格式与游戏 IL2CPP 结构双向印证）
2. 140 赛道的分段/坡道/相位可从攻略站全量获取，**不再必须进比赛 dump**
3. GroundModifierParam（场地消耗数值）仍需进比赛
4. mdb 侧 race/race_instance/single_mode_program 链路完整，可把"哪场比赛在哪个赛道"完整还原
