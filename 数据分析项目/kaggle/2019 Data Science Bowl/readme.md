# 2019年12月14日开始项目
### 一、提出问题
1. 通过测验需要几次尝试

### 二、理解数据
|  Field |  Description |
|  -------|  ------- |
|  event_id |  随机生成的事件类型的唯一标识符。映射到event_id规格表中的列。 |
|  game_session | 在单个游戏或视频播放会话中随机生成的唯一标识符分组事件。
|timestamp | 客户生成的日期时间
|event_data |包含事件参数的半结构化JSON格式的字符串。默认字段是：event_count，event_code，和game_time; 否则，字段由事件类型确定。
|installation_id | 在单个安装的应用程序实例中随机生成的唯一标识符将游戏会话分组。
|event_count | 游戏会话内事件的增量计数器（偏移为1）。提取自event_data。
|event_code | 事件“类别”的标识符。每个游戏唯一，但可以在多个游戏中重复。例如，事件代码“ 2000”始终标识所有游戏的“开始游戏”事件。提取自event_data。
|game_time | 自游戏会话开始以来的时间（以毫秒为单位）。提取自event_data。
|title  | 游戏或视频的标题。
|type | 游戏或视频的媒体类型。可能的值为：“游戏”，“评估”，“活动”，“剪辑”。
|world | 游戏或视频所属的应用程序部分。有助于确定媒体的教育课程目标。可能的值为：“ NONE”（在应用程序的开始屏幕上），“ REEPOTPCITY”（长度/高度），“ |MAGMAPEAK”（容量/排量），“ CRYSTALCAVES”（重量）。
