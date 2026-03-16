"""院校列表页面

展示所有院校的基本信息，支持搜索和跳转详情。
"""

import streamlit as st

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

    st.divider()

    # 表头
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 1])
    with col1:
        st.markdown("**院校名称**")
    with col2:
        st.markdown("**代码**")
    with col3:
        st.markdown("**物理分**")
    with col4:
        st.markdown("**物理位次**")
    with col5:
        st.markdown("**历史分**")
    with col6:
        st.markdown("**历史位次**")
    with col7:
        st.markdown("**操作**")

    st.divider()

    # 数据行
    for uni in page_data:
        physics_info = get_university_score_info(uni, SubjectType.PHYSICS)
        history_info = get_university_score_info(uni, SubjectType.HISTORY)

        col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 1])
        with col1:
            st.write(uni.name)
        with col2:
            st.write(uni.code)
        with col3:
            st.write(physics_info["min_score"] or "-")
        with col4:
            st.write(physics_info["min_rank"] or "-")
        with col5:
            st.write(history_info["min_score"] or "-")
        with col6:
            st.write(history_info["min_rank"] or "-")
        with col7:
            if st.button(
                "查看",
                key=f"view_list_{uni.code}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.detail_university_code = uni.code
                st.switch_page("app_pages/university_detail.py")


# 页面入口
if __name__ == "__main__":
    render()