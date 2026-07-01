"""
全局常量定义
YERC 协议魔数、默认IP、心跳间隔、速度上限等
"""

# ===== YERC 协议常量 =====
# 报文魔数 "YERC"
YERC_MAGIC = bytes([0x59, 0x45, 0x52, 0x43])
# 标头部大小（固定 32 字节）
YERC_HEADER_SIZE = 32
# 数据块编号固定值
YERC_BLOCK_NUM = b"99999999"
# 命令类型标识
YERC_CMD_TYPE_READ = 0x01   # 读取
YERC_CMD_TYPE_WRITE = 0x00  # 写入
# 状态响应：0x80 成功，0x81+ 错误
YERC_STATUS_SUCCESS = 0x80

# ===== YERC 命令编号 =====
YERC_CMD_STATUS = 0x72      # 读取机器人状态
YERC_CMD_POSITION = 0x75    # 读取机器人位置
YERC_CMD_ALARM = 0x70       # 读取报警信息
YERC_CMD_TORQUE = 0x74      # 读取各轴力矩
YERC_CMD_AXIS_CONFIG = 0x73 # 读取轴构成
YERC_CMD_B_VARIABLE = 0x7A  # B 变量读写
YERC_CMD_P_VARIABLE = 0x7F  # P 变量读写
YERC_CMD_IO = 0x76          # IO 信号读写

# ===== 机器人状态常量 =====
# 运行模式枚举
ROBOT_MODE_TEACHING = "teaching"   # 示教模式
ROBOT_MODE_PLAY = "play"          # 再现模式
ROBOT_MODE_REMOTE = "remote"       # 远程模式
ROBOT_MODE_IDLE = "idle"          # 空闲
ROBOT_MODE_ERROR = "error"         # 错误

# ===== 安全常量 =====
# 各角色速度上限百分比
ROLE_SPEED_LIMITS = {
    "admin": 100,
    "operator": 30,
    "engineer": 80,
    "observer": 0,
}

# 预设速度档位
SPEED_PRESETS = {
    "micro": {"label": "微动档", "range": (1, 5)},
    "slow": {"label": "慢速档", "range": (10, 20)},
    "normal": {"label": "正常档", "range": (30, 60)},
    "high": {"label": "高速档", "range": (70, 100)},
}

# 轴名称映射
AXIS_NAMES = {
    1: {"name": "S轴(J1)", "desc": "本体旋转"},
    2: {"name": "L轴(J2)", "desc": "下臂前后"},
    3: {"name": "U轴(J3)", "desc": "上臂上下"},
    4: {"name": "R轴(J4)", "desc": "下臂旋转"},
    5: {"name": "B轴(J5)", "desc": "手腕上下"},
    6: {"name": "T轴(J6)", "desc": "手腕旋转"},
    7: {"name": "E轴(J7)", "desc": "第7轴"},
}

# ===== 通信常量 =====
# 默认超时时间（秒）
DEFAULT_UDP_TIMEOUT = 0.5
# 最大重试次数
MAX_RETRIES = 3
# 心跳间隔（秒）
HEARTBEAT_INTERVAL = 1.0
# WebSocket 断线重连间隔（秒）
WS_RECONNECT_INTERVAL = 3
# WebSocket 最大重连次数
WS_MAX_RECONNECT = 10

# ===== 调试终端常量 =====
# 默认发送频率限制（次/秒）
DEFAULT_SEND_RATE_LIMIT = 10
# 接收缓冲区大小（字节）
RECEIVE_BUFFER_SIZE = 2048
# 报文日志最大显示条数
PACKET_LOG_DISPLAY_MAX = 100

# ===== 数据库常量 =====
# 操作日志保留天数
OPERATION_LOG_RETENTION_DAYS = 180

# ===== 报警常量 =====
ALARM_LEVEL_CRITICAL = "critical"   # 重度
ALARM_LEVEL_WARNING = "warning"     # 轻度
ALARM_LEVEL_INFO = "info"           # 信息
