"""位次计算逻辑

实现位次与分数的互查功能，以及冲保稳区间计算。
"""

from typing import Optional

import pandas as pd

from core.config import RANGE_STRATEGY


def find_score_by_rank(rank_table: pd.DataFrame, target_rank: int) -> Optional[int]:
    """根据位次查找对应分数

    使用二分查找在累积位次中找到对应的分数。

    Args:
        rank_table: 一分一段表 DataFrame，包含 cumulative_rank 列
        target_rank: 目标位次

    Returns:
        对应分数，若超出范围返回 None
    """
    if rank_table is None or rank_table.empty:
        return None

    # 检查位次是否在有效范围内
    max_rank = rank_table["cumulative_rank"].max()
    min_rank = rank_table["cumulative_rank"].min()

    if target_rank > max_rank:
        # 位次超出最大值，返回最低分
        return int(rank_table.loc[rank_table["cumulative_rank"].idxmax(), "score"])
    if target_rank < min_rank:
        # 位次低于最高分对应的最小位次
        return int(rank_table.loc[rank_table["cumulative_rank"].idxmin(), "score"])

    # 找到第一个累积位次 >= 目标位次的行
    mask = rank_table["cumulative_rank"] >= target_rank
    if not mask.any():
        return None

    idx = mask.idxmax()
    return int(rank_table.loc[idx, "score"])


def find_rank_by_score(rank_table: pd.DataFrame, target_score: int) -> Optional[int]:
    """根据分数查找对应位次

    Args:
        rank_table: 一分一段表 DataFrame
        target_score: 目标分数

    Returns:
        对应位次，若超出范围返回 None
    """
    if rank_table is None or rank_table.empty:
        return None

    # 找到分数对应的行
    mask = rank_table["score"] == target_score
    if mask.any():
        return int(rank_table.loc[mask, "cumulative_rank"].iloc[0])

    return None


def calculate_rank_range(
    rank_table: pd.DataFrame,
    base_score: int,
    strategy: dict | None = None,
) -> dict[str, dict]:
    """计算冲保稳区间

    Args:
        rank_table: 一分一段表 DataFrame
        base_score: 基准分数
        strategy: 策略配置，默认使用 RANGE_STRATEGY
            {
                "reach": {"min_offset": 5, "max_offset": 10},   # 冲
                "stable": {"min_offset": -5, "max_offset": 5},  # 稳
                "safety": {"min_offset": -15, "max_offset": -10}  # 保
            }

    Returns:
        {
            "reach": {"min_score": x, "max_score": y, "min_rank": a, "max_rank": b},
            "stable": {...},
            "safety": {...}
        }
    """
    if strategy is None:
        strategy = RANGE_STRATEGY

    result = {}

    for range_type, offsets in strategy.items():
        min_offset = offsets["min_offset"]
        max_offset = offsets["max_offset"]

        min_score = base_score + min_offset
        max_score = base_score + max_offset

        # 确保 min_score <= max_score
        if min_score > max_score:
            min_score, max_score = max_score, min_score

        # 查找对应的位次
        min_rank = find_rank_by_score(rank_table, max_score)  # 高分对应低位次
        max_rank = find_rank_by_score(rank_table, min_score)  # 低分对应高位次

        result[range_type] = {
            "min_score": min_score,
            "max_score": max_score,
            "min_rank": min_rank,
            "max_rank": max_rank,
        }

    return result


def get_score_range_info(
    rank_table: pd.DataFrame, min_score: int, max_score: int
) -> dict:
    """获取分数区间信息

    Args:
        rank_table: 一分一段表 DataFrame
        min_score: 最低分数
        max_score: 最高分数

    Returns:
        {
            "min_rank": 最低分数对应的位次,
            "max_rank": 最高分数对应的位次,
            "total_count": 区间内的总人数
        }
    """
    min_rank = find_rank_by_score(rank_table, min_score)
    max_rank = find_rank_by_score(rank_table, max_score)

    # 计算区间内的总人数
    total_count = None
    if min_rank and max_rank:
        total_count = max_rank - min_rank + 1

    return {
        "min_rank": min_rank,
        "max_rank": max_rank,
        "total_count": total_count,
    }