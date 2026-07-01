"""初始表结构迁移脚本"""

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """升级：创建所有初始表"""
    pass  # 使用 create_all 方式，Alembic 迁移脚本为空


def downgrade() -> None:
    """降级：删除所有表"""
    pass
