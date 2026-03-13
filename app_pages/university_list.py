"""院校列表页面

展示所有院校的基本信息，支持搜索和跳转详情。
"""

import streamlit as st
import pandas as pd

from components.selectors import get_current_selection
from core.data_loader import load_admission_data
from core.university_filter import get_university_score_info, search_universities
from models.enums import SubjectType


def render() -> None:
    """渲染院校列表页面"""
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

    st.subheader("院校列表")

    # 搜索框
    search_keyword = st.text_input(
        "搜索院校",
        placeholder="输入院校名称或代码搜索...",
        key="university_search",
    )

    # 搜索过滤
    if search_keyword:
        filtered = search_universities(universities, search_keyword)
    else:
        filtered = universities

    st.write(f"共 **{len(filtered)}** 所院校")

    # 分页
    page_size = 15
    total_pages = (len(filtered) + page_size - 1) // page_size

    page = st.number_input(
        "页码",
        min_value=1,
        max_value=max(1, total_pages),
        value=1,
        step=1,
    )

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_data = filtered[start_idx:end_idx]

    # 准备表格数据
    table_data = []
    for uni in page_data:
        physics_info = get_university_score_info(uni, SubjectType.PHYSICS)
        history_info = get_university_score_info(uni, SubjectType.HISTORY)

        row = {
            "院校名称": uni.name,
            "院校代码": uni.code,
            "官网": uni.official_website or "-",
            "物理最低分": physics_info["min_score"] or "-",
            "物理位次": physics_info["min_rank"] or "-",
            "历史最低分": history_info["min_score"] or "-",
            "历史位次": history_info["min_rank"] or "-",
        }
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # 显示表格
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "院校名称": st.column_config.TextColumn("院校名称", width="large"),
            "院校代码": st.column_config.TextColumn("院校代码", width="small"),
            "官网": st.column_config.LinkColumn("官网", width="medium"),
            "物理最低分": st.column_config.TextColumn("物理最低分", width="small"),
            "物理位次": st.column_config.TextColumn("物理位次", width="small"),
            "历史最低分": st.column_config.TextColumn("历史最低分", width="small"),
            "历史位次": st.column_config.TextColumn("历史位次", width="small"),
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
            key="university_selector",
            label_visibility="collapsed",
        )
    with col2:
        if st.button("查看详情", type="primary", use_container_width=True):
            for uni in page_data:
                if uni.name == selected_uni_name:
                    st.session_state.detail_university_code = uni.code
                    st.switch_page("app_pages/university_detail.py")
                    break


# 页面入口
if __name__ == "__main__":
    render()