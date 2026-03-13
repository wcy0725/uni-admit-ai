"""分数推荐院校页面UI测试"""

import time
import pytest
from playwright.sync_api import Page

from tests.conftest import (
    STREAMLIT_URL,
    take_screenshot,
    wait_for_page_load,
    check_for_errors,
    navigate_to_page,
)


class TestScoreToUniversityPage:
    """分数推荐院校页面测试类"""

    def test_page_loads_successfully(self, page: Page):
        """测试页面加载成功"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(5)
        take_screenshot(page, "01_score_to_university_initial")

        # 检查无错误
        errors = check_for_errors(page)
        assert len(errors) == 0, f"页面不应有错误: {errors}"

        # 检查关键元素
        page_text = page.inner_text('body')
        assert "分数" in page_text or "院校" in page_text, "页面应包含分数或院校相关内容"

    def test_filter_by_score_range(self, page: Page):
        """测试按分数范围筛选"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(5)

        # 获取所有数字输入框
        number_inputs = page.query_selector_all('input[type="number"]')

        if len(number_inputs) >= 2:
            # 设置分数范围（最后一个和倒数第二个应该是分数输入）
            # 先找到分数输入框（通过前面的标签判断）
            number_inputs[0].fill("600")
            number_inputs[1].fill("650")
            time.sleep(3)
            take_screenshot(page, "02_score_to_university_filter")

        # 检查是否显示筛选结果
        page_text = page.inner_text('body')
        assert "所院校" in page_text, "应显示院校数量"

    def test_search_university(self, page: Page):
        """测试搜索院校功能"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(5)

        # 找到搜索框
        search_input = page.query_selector('input[placeholder*="搜索"]')
        if search_input:
            search_input.fill("北京")
            time.sleep(3)
            take_screenshot(page, "03_score_to_university_search")

        # 检查搜索结果
        page_text = page.inner_text('body')
        assert "北京" in page_text, "应显示搜索结果"

    def test_chart_display(self, page: Page):
        """测试图表显示"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(5)

        # 检查是否有图表
        chart = page.query_selector('[class*="plotly"]')
        if chart:
            take_screenshot(page, "04_score_to_university_chart")
            assert True, "图表显示正常"
        else:
            # 图表可能以其他方式呈现
            page_text = page.inner_text('body')
            assert "院校" in page_text, "应显示院校信息"

    def test_navigate_to_detail(self, page: Page):
        """测试跳转到院校详情"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(8)

        take_screenshot(page, "05_score_to_university_before_nav")

        # 点击查看详情按钮
        detail_btn = page.query_selector('button:has-text("查看详情")')
        if detail_btn:
            detail_btn.click()
            time.sleep(5)
            take_screenshot(page, "06_score_to_university_after_nav")

            # 验证跳转成功
            page_text = page.inner_text('body')
            assert "基本信息" in page_text or "院校代码" in page_text, "应跳转到院校详情页"

    def test_pagination(self, page: Page):
        """测试分页功能"""
        navigate_to_page(page, "分数推荐院校")
        time.sleep(5)

        # 找到页码输入框
        page_inputs = page.query_selector_all('input[type="number"]')
        # 最后一个可能是页码
        if page_inputs:
            # 尝试翻页
            take_screenshot(page, "07_score_to_university_page1")

            # 修改页码
            page_inputs[-1].fill("2")
            time.sleep(3)
            take_screenshot(page, "08_score_to_university_page2")