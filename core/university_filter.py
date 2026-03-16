"""院校筛选逻辑

实现按分数范围筛选和模糊搜索院校的功能。
"""

import re
from typing import Optional

from models.enums import SubjectType
from models.schemas import University


def parse_score(score_str: str) -> Optional[int]:
    """解析分数字符串

    处理可能的格式：
    - "600" -> 600
    - "综合评价成绩613.8" -> None (无法直接比较)
    - "" -> None

    Args:
        score_str: 分数字符串

    Returns:
        整数分数，如果无法解析返回 None
    """
    if not score_str:
        return None

    try:
        return int(float(score_str))
    except ValueError:
        # 尝试从字符串中提取数字
        match = re.search(r"(\d+\.?\d*)", score_str)
        if match:
            try:
                return int(float(match.group(1)))
            except ValueError:
                return None
        return None


def filter_universities_by_score(
    universities: list[University],
    min_score: int,
    max_score: int,
    subject_type: SubjectType,
) -> list[University]:
    """按分数范围筛选院校

    Args:
        universities: 院校列表
        min_score: 最低分数
        max_score: 最高分数
        subject_type: 科目类型

    Returns:
        筛选后的院校列表
    """
    category = subject_type.display_name
    result = []

    for university in universities:
        records = university.get_admission_records(category)
        # 先计算院校的最低分（排除综合评价）
        uni_min_score = None
        for record in records:
            # 跳过综合评价录取
            if "综合评价" in record.min_score:
                continue
            score = parse_score(record.min_score)
            if score:
                if uni_min_score is None or score < uni_min_score:
                    uni_min_score = score

        # 检查院校最低分是否在范围内
        if uni_min_score and min_score <= uni_min_score <= max_score:
            result.append(university)

    return result


def search_universities(
    universities: list[University], keyword: str
) -> list[University]:
    """模糊搜索院校

    支持按院校名称或院校代码搜索。

    Args:
        universities: 院校列表
        keyword: 搜索关键词

    Returns:
        匹配的院校列表
    """
    if not keyword:
        return universities

    keyword = keyword.strip().lower()
    result = []

    for university in universities:
        # 按名称搜索
        if keyword in university.name.lower():
            result.append(university)
            continue

        # 按代码搜索
        if keyword in university.code.lower():
            result.append(university)
            continue

        # 在录取记录中搜索代码
        if university.admission_score and university.admission_score.liaoning:
            for record in university.admission_score.liaoning:
                if keyword in record.code.lower():
                    result.append(university)
                    break

    return result


def get_university_score_info(
    university: University, subject_type: SubjectType
) -> dict:
    """获取院校在指定科目的分数信息

    Args:
        university: 院校对象
        subject_type: 科目类型

    Returns:
        {
            "min_score": 最低分数,
            "min_rank": 最低分数对应的位次,
            "records": 录取记录列表
        }
    """
    category = subject_type.display_name
    records = university.get_admission_records(category)

    min_score = None
    min_rank = None

    for record in records:
        # 跳过综合评价录取
        if "综合评价" in record.min_score:
            continue

        score = parse_score(record.min_score)
        if score:
            # 找到更低的分数时，更新分数和对应的位次
            if min_score is None or score < min_score:
                min_score = score
                # 位次取该分数对应的位次
                min_rank = parse_score(record.rank) if record.rank else None

    return {
        "min_score": min_score,
        "min_rank": min_rank,
        "records": records,
    }


def sort_universities_by_score(
    universities: list[University],
    subject_type: SubjectType,
    ascending: bool = False,
) -> list[University]:
    """按录取分数排序院校

    Args:
        universities: 院校列表
        subject_type: 科目类型
        ascending: 是否升序（默认降序，高分在前）

    Returns:
        排序后的院校列表
    """
    category = subject_type.display_name

    def get_sort_key(university: University) -> int:
        score_info = get_university_score_info(university, subject_type)
        return score_info["min_score"] or 0

    return sorted(universities, key=get_sort_key, reverse=not ascending)