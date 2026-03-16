"""高考志愿填报助手

主入口文件，配置多页面导航和全局选择器。
"""

import streamlit as st

from components.selectors import init_session_state, render_global_selectors


def main() -> None:
    """主函数"""
    # 设置页面配置
    st.set_page_config(
        page_title="高考志愿填报助手",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 初始化全局状态
    init_session_state()

    # 定义页面导航
    pages = [
        st.Page(
            "app_pages/rank_to_score.py",
            title="位次查分数",
            icon=":material/analytics:",
        ),
        st.Page(
            "app_pages/score_to_university.py",
            title="分数推荐院校",
            icon=":material/school:",
        ),
        st.Page(
            "app_pages/university_list.py",
            title="院校列表",
            icon=":material/format_list_bulleted:",
        ),
        st.Page(
            "app_pages/comprehensive_evaluation.py",
            title="综合评价",
            icon=":material/stars:",
        ),
        st.Page(
            "app_pages/university_detail.py",
            title="院校详情",
            icon=":material/info:",
        ),
    ]

    # 侧边栏导航和选择器
    with st.sidebar:
        # 创建导航（侧边栏）
        page = st.navigation(pages, position="sidebar")

        # 渲染全局选择器到侧边栏
        render_global_selectors(sidebar_mode=True)

    # 运行当前页面
    page.run()


if __name__ == "__main__":
    main()