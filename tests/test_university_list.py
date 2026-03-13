"""院校列表页面UI测试"""

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


class TestUniversityListPage:
    """院校列表页面测试类"""

    def test_page_loads_successfully(self, page: Page):
        """测试页面加载成功"""
        navigate_to_page(page, "院校列表")
        time.sleep(8)
        take_screenshot(page, "01_university_list_initial")

        # 检查无错误
        errors = check_for_errors(page)
        assert len(errors) == 0, f"页面不应有错误: {errors}"

        # 检查关键元素
        page_text = page.inner_text('body')
        assert "院校" in page_text, "页面应包含院校相关内容"
        assert "所院校" in page_text, "应显示院校数量"

    def test_table_display(self, page: Page):
        """测试表格显示"""
        navigate_to_page(page, "院校列表")
        time.sleep(8)
        take_screenshot(page, "02_university_list_table")

        # 检查表格是否存在
        table = page.query_selector('table')
        assert table is not None, "应存在数据表格"

        # 检查表格内容
        table_text = table.inner_text()
        assert "院校名称" in table_text or "院校代码" in table_text, "表格应包含院校信息"

    def test_search_university(self, page: Page):
        """测试搜索院校功能"""
        navigate_to_page(page, "院校列表")
        time.sleep(5)

        # 找到搜索框
        search_input = page.query_selector('input[placeholder*="搜索"]')
        if search_input:
            search_input.fill("北京大学")
            time.sleep(3)
            take_screenshot(page, "03_university_list_search")

            # 检查搜索结果
            page_text = page.inner_text('body')
            assert "北京大学" in page_text, "应显示北京大学"

    def test_search_by_code(self, page: Page):
        """测试按代码搜索"""
        navigate_to_page(page, "院校列表")
        time.sleep(5)

        search_input = page.query_selector('input[placeholder*="搜索"]')
        if search_input:
            search_input.fill("0001")
            time.sleep(3)
            take_screenshot(page, "04_university_list_search_code")

            # 检查搜索结果
            page_text = page.inner_text('body')
            # 0001 是北京大学
            assert "北京" in page_text or "0001" in page_text, "应显示对应院校"

    def test_pagination(self, page: Page):
        """测试分页功能"""
        navigate_to_page(page, "院校列表")
        time.sleep(5)

        take_screenshot(page, "05_university_list_page1")

        # 找到页码输入框
        page_input = page.query_selector('input[type="number"]')
        if page_input:
            page_input.fill("2")
            time.sleep(3)
            take_screenshot(page, "06_university_list_page2")

            # 验证页面内容变化
            page_text = page.inner_text('body')
            assert "所院校" in page_text, "应显示院校数量"

    def test_navigate_to_detail(self, page: Page):
        """测试跳转到院校详情"""
        navigate_to_page(page, "院校列表")
        time.sleep(8)

        take_screenshot(page, "07_university_list_before_nav")

        # 点击查看详情按钮
        detail_btn = page.query_selector('button:has-text("查看详情")')
        assert detail_btn is not None, "应存在查看详情按钮"

        detail_btn.click()
        time.sleep(5)
        take_screenshot(page, "08_university_list_after_nav")

        # 验证跳转成功
        page_text = page.inner_text('body')
        assert "基本信息" in page_text or "院校代码" in page_text, "应跳转到院校详情页"

    def test_official_website_link(self, page: Page):
        """测试官网链接"""
        navigate_to_page(page, "院校列表")
        time.sleep(8)

        take_screenshot(page, "09_university_list_links")

        # 检查是否有链接列
        links = page.query_selector_all('a')
        # 表格中的官网链接
        assert len(links) > 0, "应存在官网链接"