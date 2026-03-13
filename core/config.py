"""配置常量定义

定义路径构建函数、默认策略常量等配置。
"""

from pathlib import Path

from models.enums import BatchType, SubjectType


# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"


# 冲保稳区间策略配置（分数偏移量）
RANGE_STRATEGY = {
    "reach": {"min_offset": 5, "max_offset": 10},   # 冲：+5~10分
    "stable": {"min_offset": -5, "max_offset": 5},  # 稳：±5分
    "safety": {"min_offset": -15, "max_offset": -10},  # 保：-10~15分
}


def get_rank_table_path(province: str, year: int, subject: SubjectType) -> Path:
    """构建一分一段表路径

    Args:
        province: 省份名称（如"辽宁"）
        year: 年份（如2025）
        subject: 科目类型（物理类/历史类）

    Returns:
        一分一段表文件路径
    """
    filename = f"rank_table_{subject.file_suffix}.tsv"
    return DATA_DIR / province / str(year) / filename


def get_admission_path(province: str, year: int, batch: BatchType) -> Path:
    """构建录取数据路径

    Args:
        province: 省份名称（如"辽宁"）
        year: 年份（如2025）
        batch: 批次类型

    Returns:
        录取数据文件路径
    """
    filename = f"admission_{batch.file_suffix}.json"
    return DATA_DIR / province / str(year) / filename