"""位次查分数页面

输入位次查询对应分数，并计算冲保稳区间。
"""

import streamlit as st

from components.charts import create_rank_range_chart, display_chart
from components.selectors import get_current_selection
from core.data_loader import load_rank_table
from core.rank_calculator import calculate_rank_range, find_score_by_rank


def render() -> None:
    """渲染位次查分数页面"""
    # 获取当前选择
    selection = get_current_selection()
    province = selection["province"]
    year = selection["year"]
    subject = selection["subject"]

    if not province or not year:
        st.warning("请先选择省份和年份")
        return

    # 加载一分一段表
    rank_table = load_rank_table(province, year, subject)

    if rank_table is None or rank_table.empty:
        st.error("未找到对应的一分一段表数据")
        return

    st.subheader("输入位次查询分数")

    # 输入位次
    max_rank = int(rank_table["cumulative_rank"].max())
    min_rank = int(rank_table["cumulative_rank"].min())

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        target_rank = st.number_input(
            "请输入位次",
            min_value=min_rank,
            max_value=max_rank,
            value=min(20000, max_rank),
            step=1,
            help=f"位次范围: {min_rank} - {max_rank}",
        )

    with col2:
        st.markdown(
            """
            <style>
            div.stButton > button {
                margin-top: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        search_btn = st.button("查询", type="primary", width="stretch")

    # 查询结果
    if search_btn or target_rank:
        score = find_score_by_rank(rank_table, target_rank)

        if score:
            # 显示查询结果
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("对应分数", f"{score}分")
                with col2:
                    st.metric("输入位次", f"第{target_rank}名")
                with col3:
                    # 查找该分数对应的累计人数
                    mask = rank_table["score"] == score
                    if mask.any():
                        count = int(rank_table.loc[mask, "count"].iloc[0])
                        st.metric("该分数人数", f"{count}人")

            st.divider()

            # 冲保稳区间计算
            st.subheader("冲保稳区间分析")

            # 可调节参数
            col1, col2, col3 = st.columns(3)
            with col1:
                reach_min = st.number_input("冲 - 最低加分", value=5, min_value=0, max_value=50)
                reach_max = st.number_input("冲 - 最高加分", value=10, min_value=0, max_value=50)
            with col2:
                stable_min = st.number_input("稳 - 最低减分", value=5, min_value=0, max_value=50)
                stable_max = st.number_input("稳 - 最高加分", value=5, min_value=0, max_value=50)
            with col3:
                safety_min = st.number_input("保 - 最低减分", value=15, min_value=0, max_value=50)
                safety_max = st.number_input("保 - 最高减分", value=10, min_value=0, max_value=50)

            strategy = {
                "reach": {"min_offset": reach_min, "max_offset": reach_max},
                "stable": {"min_offset": -stable_min, "max_offset": stable_max},
                "safety": {"min_offset": -safety_min, "max_offset": -safety_max},
            }

            ranges = calculate_rank_range(rank_table, score, strategy)

            # 显示区间卡片
            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):
                    st.markdown("### 🔥 冲")
                    r = ranges["reach"]
                    st.write(f"**分数区间**: {r['min_score']} - {r['max_score']} 分")
                    if r["min_rank"] and r["max_rank"]:
                        st.write(f"**位次区间**: {r['min_rank']} - {r['max_rank']}")
                    if st.button("查看推荐院校", key="btn_reach"):
                        st.session_state.nav_score_min = r["min_score"]
                        st.session_state.nav_score_max = r["max_score"]
                        st.session_state.nav_target = "score_to_university"
                        st.session_state.score_source_page = "rank_to_score"
                        st.switch_page("app_pages/score_to_university.py")

            with col2:
                with st.container(border=True):
                    st.markdown("### ✅ 稳")
                    r = ranges["stable"]
                    st.write(f"**分数区间**: {r['min_score']} - {r['max_score']} 分")
                    if r["min_rank"] and r["max_rank"]:
                        st.write(f"**位次区间**: {r['min_rank']} - {r['max_rank']}")
                    if st.button("查看推荐院校", key="btn_stable"):
                        st.session_state.nav_score_min = r["min_score"]
                        st.session_state.nav_score_max = r["max_score"]
                        st.session_state.nav_target = "score_to_university"
                        st.session_state.score_source_page = "rank_to_score"
                        st.switch_page("app_pages/score_to_university.py")

            with col3:
                with st.container(border=True):
                    st.markdown("### 🛡️ 保")
                    r = ranges["safety"]
                    st.write(f"**分数区间**: {r['min_score']} - {r['max_score']} 分")
                    if r["min_rank"] and r["max_rank"]:
                        st.write(f"**位次区间**: {r['min_rank']} - {r['max_rank']}")
                    if st.button("查看推荐院校", key="btn_safety"):
                        st.session_state.nav_score_min = r["min_score"]
                        st.session_state.nav_score_max = r["max_score"]
                        st.session_state.nav_target = "score_to_university"
                        st.session_state.score_source_page = "rank_to_score"
                        st.switch_page("app_pages/score_to_university.py")

            # 图表展示
            st.divider()
            fig = create_rank_range_chart(score, ranges)
            display_chart(fig)

        else:
            st.error("未找到对应的分数，请检查输入的位次是否有效")


# 页面入口
if __name__ == "__main__":
    render()