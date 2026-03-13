"""枚举类型定义

定义科目类型和批次类型的枚举，用于数据过滤和路径构建。
"""

from enum import Enum


class SubjectType(Enum):
    """科目类型枚举

    对应一分一段表文件命名：
    - PHYSICS: rank_table_l.tsv (物理类/理科)
    - HISTORY: rank_table_w.tsv (历史类/文科)
    """

    PHYSICS = "l"
    HISTORY = "w"

    @property
    def display_name(self) -> str:
        """获取中文显示名称"""
        names = {"l": "物理类", "w": "历史类"}
        return names[self.value]

    @property
    def file_suffix(self) -> str:
        """获取文件名后缀"""
        return self.value


class BatchType(Enum):
    """批次类型枚举

    对应录取数据文件命名：
    - EARLY: admission_1.json (提前批)
    - SPECIAL: admission_2.json (特殊类型批)
    - REGULAR: admission_3.json (常规批)
    """

    EARLY = "1"
    SPECIAL = "2"
    REGULAR = "3"

    @property
    def display_name(self) -> str:
        """获取中文显示名称"""
        names = {"1": "提前批", "2": "特殊类型批", "3": "常规批"}
        return names[self.value]

    @property
    def file_suffix(self) -> str:
        """获取文件名后缀"""
        return self.value