"""共用选择器组件

实现年份、省份、科目、批次的共用选择器，使用 session_state 管理状态。
"""

from typing import Optional

import streamlit as st

from core.data_loader import get_available_batches, get_available_provinces, get_available_years
from models.enums import BatchType, SubjectType


def init_session_state() -> None:
    """初始化 session_state 中的选择器状态"""
    if "selected_province" not in st.session_state:
        st.session_state.selected_province = None
    if "selected_year" not in st.session_state:
        st.session_state.selected_year = None
    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = SubjectType.PHYSICS
    if "selected_batch" not in st.session_state:
        st.session_state.selected_batch = BatchType.EARLY


def render_global_selectors() -> dict:
    """渲染顶部共用选择器

    Returns:
        dict: {
            "province": str,
            "year": int,
            "subject": SubjectType,
            "batch": BatchType
        }
    """
    init_session_state()

    # 获取可用选项
    provinces = get_available_provinces()

    # 如果没有选择省份，默认选择第一个
    if not provinces:
        st.warning("未找到数据目录，请检查 data/ 文件夹")
        return {
            "province": None,
            "year": None,
            "subject": SubjectType.PHYSICS,
            "batch": BatchType.EARLY,
        }

    if st.session_state.selected_province is None:
        st.session_state.selected_province = provinces[0]

    # 使用水平布局
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        province = st.selectbox(
            "省份",
            options=provinces,
            index=provinces.index(st.session_state.selected_province)
            if st.session_state.selected_province in provinces
            else 0,
            key="province_selector",
            help="选择省份",
        )
        st.session_state.selected_province = province

    # 获取该省份可用年份
    years = get_available_years(province)
    with col2:
        if years:
            year = st.selectbox(
                "年份",
                options=years,
                index=years.index(st.session_state.selected_year)
                if st.session_state.selected_year in years
                else 0,
                key="year_selector",
                help="选择年份",
            )
            st.session_state.selected_year = year
        else:
            year = None
            st.selectbox(
                "年份",
                options=["无数据"],
                disabled=True,
                key="year_selector_disabled",
            )

    # 获取该省份年份可用批次
    batches = get_available_batches(province, year) if year else []
    with col3:
        subject = st.segmented_control(
            "科目",
            options=[SubjectType.PHYSICS, SubjectType.HISTORY],
            selection_mode="single",
            default=st.session_state.selected_subject,
            format_func=lambda x: x.display_name,
            key="subject_selector",
            help="选择科目类型",
        )
        st.session_state.selected_subject = subject

    with col4:
        if batches:
            batch = st.selectbox(
                "批次",
                options=batches,
                index=batches.index(st.session_state.selected_batch)
                if st.session_state.selected_batch in batches
                else 0,
                format_func=lambda x: x.display_name,
                key="batch_selector",
                help="选择批次",
            )
            st.session_state.selected_batch = batch
        else:
            batch = BatchType.EARLY
            st.selectbox(
                "批次",
                options=["无数据"],
                disabled=True,
                key="batch_selector_disabled",
            )

    return {
        "province": province,
        "year": year,
        "subject": subject,
        "batch": batch,
    }


def get_current_selection() -> dict:
    """获取当前选择器的值

    Returns:
        dict: 当前选择器状态
    """
    init_session_state()
    return {
        "province": st.session_state.selected_province,
        "year": st.session_state.selected_year,
        "subject": st.session_state.selected_subject,
        "batch": st.session_state.selected_batch,
    }