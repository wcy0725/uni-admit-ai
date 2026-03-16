"""综合评价录取页面

显示辽宁省所有综合评价录取的院校信息。
"""

import streamlit as st
import pandas as pd
import re

from components.selectors import get_current_selection
from core.data_loader import load_admission_data
from models.enums import SubjectType


def parse_comprehensive_score(score_str: str) -> float | None:
    """解析综合评价成绩（保留小数）

    Args:
        score_str: 分数字符串，如"综合评价成绩 613.8"

    Returns:
        浮点数分数，如果无法解析返回 None
    """
    if not score_str or "综合评价" not in score_str:
        return None

    # 从字符串中提取第一个数字（支持小数）
    match = re.search(r"(\d+\.?\d*)", score_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def render() -> None:
    """渲染综合评价录取页面"""
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

    st.subheader("综合评价录取")

    # 收集综合评价录取数据（先存储原始分数用于排序）
    comprehensive_data = []
    category = subject.display_name

    for uni in universities:
        records = uni.get_admission_records(category)
        for record in records:
            # 只保留综合评价录取
            if "综合评价" in record.min_score:
                score = parse_comprehensive_score(record.min_score)
                comprehensive_data.append(
                    {
                        "院校名称": uni.name,
                        "院校代码": uni.code,
                        "_score_raw": score if score is not None else 0.0,
                    }
                )

    if comprehensive_data:
        df = pd.DataFrame(comprehensive_data)

        # 确保 _score_raw 是 float 类型
        df["_score_raw"] = pd.to_numeric(df["_score_raw"], errors="coerce").fillna(0)

        # 按分数升序排序（数值排序）
        df = df.sort_values("_score_raw", ascending=True)

        # 格式化分数显示
        df["综合评价成绩"] = df["_score_raw"].apply(
            lambda x: int(x) if x == int(x) else x
        )

        # 准备显示用的 DataFrame
        display_df = df[["院校名称", "院校代码", "综合评价成绩"]].copy()

        st.write(f"共找到 **{len(comprehensive_data)}** 条综合评价录取记录")

        st.divider()

        # 显示带选择功能的表格
        event = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="comprehensive_eval_df",
            column_config={
                "院校名称": st.column_config.TextColumn("院校名称", width="large"),
                "院校代码": st.column_config.TextColumn("院校代码", width="small"),
                "综合评价成绩": st.column_config.NumberColumn("综合评价成绩", width="small"),
            },
        )

        # 获取选中的行，直接跳转
        selected_indices = event.selection.rows if event and event.selection else []
        if selected_indices:
            idx = selected_indices[0]
            selected_code = display_df.iloc[idx]["院校代码"]
            st.session_state.detail_university_code = selected_code
            st.session_state.detail_source_page = "comprehensive_evaluation"
            st.switch_page("app_pages/university_detail.py")

    else:
        st.info("该批次/科目类型下没有综合评价录取数据")


# 页面入口
if __name__ == "__main__":
    render()
