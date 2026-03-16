"""院校详情页面

展示院校的详细信息。
"""

import streamlit as st

from components.selectors import get_current_selection
from core.data_loader import load_admission_data
from core.university_filter import get_university_score_info
from models.enums import SubjectType


def render() -> None:
    """渲染院校详情页面"""
    # 从 URL 参数获取院校名称（综合评价页面跳转）
    query_params = st.query_params
    university_name = query_params.get("university", "")

    # 从 session_state 获取要查看的院校代码（院校列表页面跳转）
    target_code = st.session_state.get("detail_university_code")

    # 获取当前选择
    selection = get_current_selection()
    province = selection["province"]
    year = selection["year"]
    batch = selection["batch"]

    if not province or not year:
        st.warning("请先选择省份和年份")
        return

    # 加载院校数据
    universities = load_admission_data(province, year, batch)

    if not universities:
        st.warning("未找到对应的录取数据")
        return

    # 如果有 URL 参数，根据校名查找院校代码（遍历所有批次）
    if university_name:
        import urllib.parse
        university_name = urllib.parse.unquote(university_name)
        # 查找匹配的院校
        for uni in universities:
            if uni.name == university_name:
                target_code = uni.code
                break

        # 如果当前批次没找到，尝试所有批次
        if not target_code:
            from core.data_loader import get_available_batches
            batches = get_available_batches(province, year)
            for b in batches:
                universities = load_admission_data(province, year, b)
                for uni in universities:
                    if uni.name == university_name:
                        target_code = uni.code
                        break
                if target_code:
                    break

    if not target_code:
        st.warning("请从院校列表页面选择要查看的院校")
        if st.button("返回院校列表"):
            st.switch_page("app_pages/university_list.py")
        return

    # 查找目标院校（先尝试当前批次，再尝试所有批次）
    target_university = None
    for uni in universities:
        if uni.code == target_code:
            target_university = uni
            break

    # 如果当前批次没找到，尝试所有批次
    if not target_university:
        from core.data_loader import get_available_batches
        batches = get_available_batches(province, year)
        for b in batches:
            unis = load_admission_data(province, year, b)
            for uni in unis:
                if uni.code == target_code:
                    target_university = uni
                    break
            if target_university:
                break

    if not target_university:
        st.error("未找到该院校信息")
        if st.button("返回院校列表"):
            st.switch_page("app_pages/university_list.py")
        return

    # 显示院校详情
    st.title(f"🏫 {target_university.name}")

    # 基本信息
    with st.container(border=True):
        st.subheader("基本信息")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**院校代码**: {target_university.code}")

            if target_university.official_website:
                st.markdown(
                    f"**官方网站**: [{target_university.official_website}]"
                    f"({target_university.official_website})"
                )
            else:
                st.markdown("**官方网站**: -")

        with col2:
            st.markdown(
                f"**招生电话**: {target_university.admission_phone or '-'}"
            )
            st.markdown(f"**电子邮箱**: {target_university.email or '-'}")

    # 院校简介
    if target_university.introduction:
        with st.container(border=True):
            st.subheader("院校简介")
            st.markdown(target_university.introduction)

    # 录取分数信息
    with st.container(border=True):
        st.subheader("录取分数信息")

        # 获取所有录取记录
        if target_university.admission_score:
            records = target_university.admission_score.liaoning

            if records:
                # 按科目分组显示
                physics_records = [r for r in records if r.category == "物理类"]
                history_records = [r for r in records if r.category == "历史类"]

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 物理类")
                    if physics_records:
                        for r in physics_records:
                            st.markdown(f"- **最低分**: {r.min_score}")
                            if r.rank:
                                st.markdown(f"  - 位次: {r.rank}")
                            st.markdown(f"  - 批次: {r.batch}")
                    else:
                        st.info("暂无物理类录取数据")

                with col2:
                    st.markdown("### 历史类")
                    if history_records:
                        for r in history_records:
                            st.markdown(f"- **最低分**: {r.min_score}")
                            if r.rank:
                                st.markdown(f"  - 位次: {r.rank}")
                            st.markdown(f"  - 批次: {r.batch}")
                    else:
                        st.info("暂无历史类录取数据")

            else:
                st.info("暂无录取分数数据")

        else:
            st.info("暂无录取分数数据")

    # 返回按钮
    st.divider()

    # 获取来源页面
    source_page = st.session_state.get("detail_source_page", "university_list")

    # 来源页面映射
    page_map = {
        "university_list": "app_pages/university_list.py",
        "score_to_university": "app_pages/score_to_university.py",
        "comprehensive_evaluation": "app_pages/comprehensive_evaluation.py",
    }

    # 来源页面名称映射
    page_names = {
        "university_list": "院校列表",
        "score_to_university": "分数推荐院校",
        "comprehensive_evaluation": "综合评价",
    }

    target_page = page_map.get(source_page, "app_pages/university_list.py")
    target_name = page_names.get(source_page, "院校列表")

    if st.button(f"← 返回{target_name}", type="secondary"):
        st.switch_page(target_page)


# 页面入口
if __name__ == "__main__":
    render()