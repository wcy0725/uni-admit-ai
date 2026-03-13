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
            "app_pages/university_detail.py",
            title="院校详情",
            icon=":material/info:",
        ),
    ]

    # 创建导航（侧边栏）
    page = st.navigation(pages, position="sidebar")

    # 侧边栏标题
    with st.sidebar:
        st.title("🎓 高考志愿填报助手")
        st.divider()

    # 渲染全局选择器（在主区域顶部）
    st.markdown("### 数据筛选")
    render_global_selectors()
    st.divider()

    # 运行当前页面
    page.run()


if __name__ == "__main__":
    main()