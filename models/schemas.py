"""数据模型定义

使用 Pydantic 定义院校信息和录取记录的数据模型。
"""

from typing import Optional
from pydantic import BaseModel, Field


class AdmissionRecord(BaseModel):
    """单个录取记录

    表示一所院校在某个省份、某个科目的录取信息。
    """

    code: str = Field(..., description="院校代码")
    category: str = Field(..., description="科目类型：物理类/历史类")
    min_score: str = Field(..., description="最低录取分数，可能为'综合评价成绩xxx'")
    batch: str = Field(..., description="批次描述")
    rank: Optional[str] = Field(None, description="录取位次，可能为空")


class AdmissionScore(BaseModel):
    """录取分数信息

    包含年份和各省份的录取记录列表。
    """

    year: int = Field(..., description="录取年份")
    liaoning: list[AdmissionRecord] = Field(
        default_factory=list, description="辽宁省录取记录"
    )
    source: str = Field(default="admission.json", description="数据来源文件")


class University(BaseModel):
    """院校信息模型

    包含院校基本信息和录取分数数据。
    """

    name: str = Field(..., description="院校名称")
    code: str = Field(..., description="院校代码")
    year: int = Field(..., description="数据年份")
    official_website: Optional[str] = Field(None, description="官方网站")
    admission_phone: Optional[str] = Field(None, description="招生电话")
    email: Optional[str] = Field(None, description="电子邮箱")
    introduction: Optional[str] = Field(None, description="院校简介")
    admission_score: Optional[AdmissionScore] = Field(None, description="录取分数信息")
    status: str = Field(default="success", description="数据状态")

    def get_admission_records(
        self, category: str | None = None
    ) -> list[AdmissionRecord]:
        """获取录取记录

        Args:
            category: 科目类型过滤，如"物理类"、"历史类"。
                     如果为 None，返回所有记录。

        Returns:
            录取记录列表
        """
        if not self.admission_score or not self.admission_score.liaoning:
            return []

        records = self.admission_score.liaoning
        if category:
            records = [r for r in records if r.category == category]

        return records

    def get_min_score(self, category: str) -> Optional[str]:
        """获取指定科目的最低分数

        Args:
            category: 科目类型

        Returns:
            最低分数字符串，如果不存在返回 None
        """
        records = self.get_admission_records(category)
        if not records:
            return None

        # 尝试找到数值型的最低分
        min_score = None
        for record in records:
            score_str = record.min_score
            # 提取数值型分数
            try:
                # 尝试直接转换为数字
                score = int(score_str)
                if min_score is None or score < min_score:
                    min_score = score
            except ValueError:
                # 如果是"综合评价成绩xxx"格式，跳过
                continue

        return str(min_score) if min_score else records[0].min_score

    def get_min_rank(self, category: str) -> Optional[str]:
        """获取指定科目的最低位次

        Args:
            category: 科目类型

        Returns:
            最低位次字符串，如果不存在返回 None
        """
        records = self.get_admission_records(category)
        if not records:
            return None

        # 找到最低位次
        min_rank = None
        for record in records:
            if record.rank:
                try:
                    rank = int(record.rank)
                    if min_rank is None or rank < min_rank:
                        min_rank = rank
                except ValueError:
                    continue

        return str(min_rank) if min_rank else None