"""分数推荐院校页面

根据分数范围筛选院校。
"""

import streamlit as st
import pandas as pd

from components.selectors import get_current_selection
from core.data_loader import load_admission_data
from core.university_filter import (
    filter_universities_by_score,
    get_university_score_info,
    sort_universities_by_score,
)
from models.enums import SubjectType


def render() -> None:
    """渲染分数推荐院校页面"""
    # 获取当前选择
    selection = get_current_selection()
    province = selection["province"]
    year = selection["year"]
    subject = selection["subject"]
    batch = selection["batch"]

    if not province or not year:
        st.warning("请先选择省份和年份")
        return

    # 加载院校数据
    universities = load_admission_data(province, year, batch)

    if not universities:
        st.warning("未找到对应的录取数据")
        return

    st.subheader("分数筛选与院校推荐")

    # 从其他页面跳转来的参数
    nav_min = st.session_state.get("nav_score_min", None)
    nav_max = st.session_state.get("nav_score_max", None)

    # 如果是从导航跳转来的，保存到 session_state 的固定 key 中
    if nav_min is not None:
        st.session_state.score_filter_min = int(nav_min)
    if nav_max is not None:
        st.session_state.score_filter_max = int(nav_max)

    # 清除导航参数（只使用一次）
    st.session_state.pop("nav_score_min", None)
    st.session_state.pop("nav_score_max", None)

    # 获取分数范围
    category = subject.display_name
    all_scores = []
    for uni in universities:
        records = uni.get_admission_records(category)
        for r in records:
            try:
                score = int(float(r.min_score))
                all_scores.append(score)
            except ValueError:
                continue

    if all_scores:
        global_min = min(all_scores)
        global_max = max(all_scores)
    else:
        global_min = 400
        global_max = 700

    # 分数范围输入
    col1, col2 = st.columns(2)

    # 使用传入的分数范围，如果没有传入则使用全局范围
    with col1:
        default_min = st.session_state.get("score_filter_min", global_min)
        min_score = st.number_input(
            "最低分数",
            min_value=0,
            max_value=750,
            value=default_min,
            step=1,
            key="min_score_input",
        )
        # 更新 session_state
        st.session_state.score_filter_min = min_score

    with col2:
        default_max = st.session_state.get("score_filter_max", global_max)
        max_score = st.number_input(
            "最高分数",
            min_value=0,
            max_value=750,
            value=default_max,
            step=1,
            key="max_score_input",
        )
        # 更新 session_state
        st.session_state.score_filter_max = max_score

    # 筛选逻辑
    filtered = filter_universities_by_score(universities, min_score, max_score, subject)

    # 排序（按分数降序）
    filtered = sort_universities_by_score(filtered, subject, ascending=False)

    st.divider()

    # 显示统计
    st.write(f"共找到 **{len(filtered)}** 所符合条件的院校")

    st.divider()

    # 院校列表
    if filtered:
        # 分页
        page_size = 15
        total_pages = (len(filtered) + page_size - 1) // page_size

        page = st.number_input(
            "页码",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = filtered[start_idx:end_idx]

        # 准备表格数据
        table_data = []
        for uni in page_data:
            score_info = get_university_score_info(uni, subject)
            table_data.append(
                {
                    "院校名称": uni.name,
                    "院校代码": uni.code,
                    "最低分数": score_info["min_score"] or "-",
                    "最低位次": score_info["min_rank"] or "-",
                }
            )

        df = pd.DataFrame(table_data)

        # 显示表格
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "院校名称": st.column_config.TextColumn("院校名称", width="large"),
                "院校代码": st.column_config.TextColumn("院校代码", width="small"),
                "最低分数": st.column_config.TextColumn("最低分数", width="small"),
                "最低位次": st.column_config.TextColumn("最低位次", width="small"),
            },
        )

        st.divider()

        # 跳转详情区域
        st.markdown("### 查看院校详情")

        col1, col2 = st.columns([3, 1])
        with col1:
            selected_uni_name = st.selectbox(
                "选择院校",
                options=[uni.name for uni in page_data],
                key="score_university_selector",
                label_visibility="collapsed",
            )
        with col2:
            if st.button("查看详情", type="primary", use_container_width=True):
                for uni in page_data:
                    if uni.name == selected_uni_name:
                        st.session_state.detail_university_code = uni.code
                        st.switch_page("app_pages/university_detail.py")
                        break

    else:
        st.info("没有找到符合条件的院校，请调整筛选条件")


# 页面入口
if __name__ == "__main__":
    render()