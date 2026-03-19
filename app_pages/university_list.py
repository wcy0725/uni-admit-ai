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

    # 准备全部表格数据（用于排序）
    table_data = []
    for uni in filtered:
        physics_info = get_university_score_info(uni, SubjectType.PHYSICS)
        history_info = get_university_score_info(uni, SubjectType.HISTORY)

        # 分数和位次转为数字，便于排序（空值用0代替用于排序）
        physics_score = physics_info["min_score"]
        physics_rank = physics_info["min_rank"]
        history_score = history_info["min_score"]
        history_rank = history_info["min_rank"]

        row = {
            "院校名称": uni.name,
            "院校代码": uni.code,
            "物理最低分": float(physics_score) if physics_score else 0,
            "物理位次": int(physics_rank) if physics_rank else 0,
            "历史最低分": float(history_score) if history_score else 0,
            "历史位次": int(history_rank) if history_rank else 0,
            # 原始值用于显示
            "_物理最低分显示": physics_score or "-",
            "_物理位次显示": physics_rank or "-",
            "_历史最低分显示": history_score or "-",
            "_历史位次显示": history_rank or "-",
        }
        table_data.append(row)

    if not table_data:
        st.info("没有找到符合条件的院校")
        return

    df = pd.DataFrame(table_data)

    st.divider()

    # 用于排序和显示的数据
    display_df = df[["院校名称", "院校代码", "物理最低分", "物理位次", "历史最低分", "历史位次"]].copy()

    event = st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="university_list_df",
        height=35 + 35 * min(10, len(display_df)),  # 表头35px + 每行35px，最多10行
        column_config={
            "院校名称": st.column_config.TextColumn("院校名称"),
            "院校代码": st.column_config.TextColumn("院校代码", width="small"),
            "物理最低分": st.column_config.NumberColumn("物理最低分", width="small"),
            "物理位次": st.column_config.NumberColumn("物理位次", width="small"),
            "历史最低分": st.column_config.NumberColumn("历史最低分", width="small"),
            "历史位次": st.column_config.NumberColumn("历史位次", width="small"),
        },
    )


    # 获取选中的行，直接跳转
    selected_indices = event.selection.rows if event and event.selection else []
    if selected_indices:
        idx = selected_indices[0]
        selected_code = display_df.iloc[idx]["院校代码"]
        st.session_state.detail_university_code = selected_code
        st.session_state.detail_source_page = "university_list"
        st.switch_page("app_pages/university_detail.py")


# 页面入口
if __name__ == "__main__":
    render()