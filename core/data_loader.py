"""数据加载器

实现数据加载、缓存和动态路径解析功能。
"""

import json
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from core.config import DATA_DIR, get_admission_path, get_rank_table_path
from models.enums import BatchType, SubjectType
from models.schemas import University


@st.cache_data(ttl=None, max_entries=50)
def load_rank_table(
    province: str, year: int, subject_type: SubjectType
) -> Optional[pd.DataFrame]:
    """加载一分一段表

    Args:
        province: 省份名称
        year: 年份
        subject_type: 科目类型（物理类/历史类）

    Returns:
        DataFrame，包含列：score(分数)、count(人数)、cumulative_rank(累计位次)
        如果文件不存在返回 None
    """
    file_path = get_rank_table_path(province, year, subject_type)

    if not file_path.exists():
        return None

    try:
        df = pd.read_csv(file_path, sep="\t")
        # 重命名列为标准名称
        df.columns = ["score", "count", "cumulative_rank"]
        return df
    except Exception as e:
        st.error(f"加载一分一段表失败: {e}")
        return None


@st.cache_data(ttl=None, max_entries=50)
def load_admission_data(
    province: str, year: int, batch: BatchType
) -> list[University]:
    """加载院校录取数据

    Args:
        province: 省份名称
        year: 年份
        batch: 批次类型

    Returns:
        院校列表（Pydantic 模型）
    """
    file_path = get_admission_path(province, year, batch)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        universities = []
        for item in data:
            try:
                university = University(**item)
                universities.append(university)
            except Exception as e:
                # 跳过解析失败的数据
                continue

        return universities
    except Exception as e:
        st.error(f"加载录取数据失败: {e}")
        return []


@st.cache_data(ttl=3600, max_entries=10)
def get_available_provinces() -> list[str]:
    """获取可用省份列表

    从 data/ 目录动态扫描可用的省份。

    Returns:
        省份名称列表
    """
    if not DATA_DIR.exists():
        return []

    provinces = []
    for item in DATA_DIR.iterdir():
        if item.is_dir():
            provinces.append(item.name)

    return sorted(provinces)


@st.cache_data(ttl=3600, max_entries=10)
def get_available_years(province: str) -> list[int]:
    """获取指定省份的可用年份列表

    Args:
        province: 省份名称

    Returns:
        年份列表（降序）
    """
    province_dir = DATA_DIR / province
    if not province_dir.exists():
        return []

    years = []
    for item in province_dir.iterdir():
        if item.is_dir():
            try:
                years.append(int(item.name))
            except ValueError:
                continue

    return sorted(years, reverse=True)


@st.cache_data(ttl=3600, max_entries=10)
def get_available_batches(province: str, year: int) -> list[BatchType]:
    """获取指定省份和年份的可用批次列表

    Args:
        province: 省份名称
        year: 年份

    Returns:
        批次类型列表
    """
    province_year_dir = DATA_DIR / province / str(year)
    if not province_year_dir.exists():
        return []

    batches = []
    for batch in BatchType:
        file_path = province_year_dir / f"admission_{batch.file_suffix}.json"
        if file_path.exists():
            batches.append(batch)

    return batches