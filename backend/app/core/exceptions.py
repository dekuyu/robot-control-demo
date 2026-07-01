"""
自定义异常定义
按错误码规范：R{模块编号}{错误编号}
"""


class AppException(Exception):
    """应用基础异常"""
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


# ===== 认证异常 (R01xx) =====
class AuthenticationError(AppException):
    """认证失败"""
    def __init__(self, message: str = "认证失败", error_code: str = "R0101"):
        super().__init__(message, error_code, 401)


class AccountLockedError(AppException):
    """账号被锁定"""
    def __init__(self, message: str = "账号已被锁定，请15分钟后重试"):
        super().__init__(message, "R0102", 403)


class TokenExpiredError(AppException):
    """Token 过期"""
    def __init__(self, message: str = "Token 已过期"):
        super().__init__(message, "R0103", 401)


class PermissionDeniedError(AppException):
    """权限不足"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, "R0104", 403)


# ===== 机器人连接异常 (R02xx) =====
class RobotNotConnectedError(AppException):
    """机器人未连接"""
    def __init__(self, message: str = "机器人未连接"):
        super().__init__(message, "R0201", 503)


class RobotConnectionTimeoutError(AppException):
    """UDP 连接超时"""
    def __init__(self, message: str = "UDP 连接超时"):
        super().__init__(message, "R0901", 504)


# ===== 安全异常 (R03xx) =====
class SafetyViolationError(AppException):
    """安全检查未通过"""
    def __init__(self, message: str = "安全检查未通过", error_code: str = "R0301"):
        super().__init__(message, error_code, 403)


class SpeedLimitExceededError(AppException):
    """速度超限"""
    def __init__(self, message: str = "速度设定超出安全限制"):
        super().__init__(message, "R0302", 403)


class InterlockViolationError(AppException):
    """互锁冲突"""
    def __init__(self, message: str = "当前状态下禁止远程控制"):
        super().__init__(message, "R0303", 403)


class AxisLimitExceededError(AppException):
    """轴限位超出"""
    def __init__(self, message: str = "目标角度超出软件限位"):
        super().__init__(message, "R0304", 403)


class EmergencyStopActiveError(AppException):
    """急停激活中"""
    def __init__(self, message: str = "急停已激活，禁止任何启动操作"):
        super().__init__(message, "R0305", 403)


# ===== 控制异常 (R04xx) =====
class ServoOperationError(AppException):
    """伺服操作失败"""
    def __init__(self, message: str = "伺服操作失败"):
        super().__init__(message, "R0401", 500)


class ControlCommandError(AppException):
    """控制指令执行失败"""
    def __init__(self, message: str = "控制指令执行失败"):
        super().__init__(message, "R0402", 500)


# ===== 位置/变量异常 (R05xx) =====
class VariableError(AppException):
    """变量读写异常"""
    def __init__(self, message: str = "变量操作失败"):
        super().__init__(message, "R0501", 400)


class PositionError(AppException):
    """位置数据异常"""
    def __init__(self, message: str = "位置操作失败"):
        super().__init__(message, "R0502", 400)


# ===== UDP 通信异常 (R09xx) =====
class YERCProtocolError(AppException):
    """YERC 协议解析失败"""
    def __init__(self, message: str = "YERC 响应解析失败"):
        super().__init__(message, "R0902", 500)


class YERCResponseError(AppException):
    """YERC 响应错误"""
    def __init__(self, message: str = "机器人返回错误响应"):
        super().__init__(message, "R0903", 500)


# ===== 系统异常 (R10xx) =====
class InternalServerError(AppException):
    """内部服务器错误"""
    def __init__(self, message: str = "内部服务器错误"):
        super().__init__(message, "R1001", 500)


class DatabaseError(AppException):
    """数据库错误"""
    def __init__(self, message: str = "数据库操作失败"):
        super().__init__(message, "R1002", 500)
