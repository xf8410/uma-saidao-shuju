# 5. HorseRaceInfo.InitGroundConditionParam 反汇编记录

- 方法地址：0x7d2961f954（2048B 已抓）
- 惰性加载静态单例（ADRP+LDR 全局 → [x21] → [x8+0xB8] → CBZ 则 BL 初始化）
- 从单例取 **+0xC8 和 +0xD0 两个数组**（疑似 芝/沙 各一组 GroundModifierParam[4]），按 ground 1..4 分支取元素
- 读 GroundModifierParam.addSpeed([x8+0x10]) 做 FADD 并入速度参数；addPower/multiHpSub 同型分支
- 写 4 个连续 float 字段（+0x54/+0x58/+0x5C/+0x60）= 常量 2000.0f（0x44FA0000，MOVZ W8,#0x44FA LSL16）
- ret_offsets：[236,256,904,1156,1532,1700,1728,2024] 多出口，多重 CBZ 空检查
- 结论：马场状态参与比赛模拟（加减速/加力/HP消耗倍率），数据在运行时初始化的静态结构里

## GetSlopeValue（static, 4参数）0x7d27fcb91c
- LDR S0,[X1] → 常量池 FMUL（万分比缩放）→ 与 0 比较 → SlopeType 分支写 1/2/0（上/下/平）
- LDR S0,[X0,#0x20] 同缩放后 STR [X19]——slope per 输出

## GetMotivationCoef（static）0x7d27fda148
- 查 masterRaceMotivationRate 表 → 万分比→float（0.96~1.04）

## GroundModifierParam 数值仍未拿到
- 不在 master.mdb（全表清单已排除 %baba%/%modify%/%ground%/%condition%）
- /il2cpp/search_float 2000 只命中 SO text 段 1 处（指令附近，非数据）
- 拿值路径：①进比赛后 object_dump/read_mem ②资源包 .br 文件（meta key captured:false）③callers 找构造者

## 工具层怪象（MCP 包装层问题，与 SO 无关）
部分端点稳定报 T003"缺参数"：type_detail / method_detail / object_dump / private_file_inventory
可用替代：disassemble / search_methods / dumpclass / mdb/raw / field / static / callers

## 查询纪律（防闪退）
- race_env_define 1000 行全量（~2MB JSON）是最后成功查询，其后游戏闪退
- /mdb/raw 一律 LIMIT≤100、max_kib≤512；禁全量 env/text 类查询
