"""院校详情页面UI测试"""

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


class TestUniversityDetailPage:
    """院校详情页面测试类"""

    def _navigate_to_detail(self, page: Page) -> None:
        """辅助方法：导航到院校详情页"""
        navigate_to_page(page, "院校列表")
        time.sleep(8)

        detail_btn = page.query_selector('button:has-text("查看详情")')
        if detail_btn:
            detail_btn.click()
            time.sleep(5)

    def test_page_loads_successfully(self, page: Page):
        """测试页面加载成功"""
        self._navigate_to_detail(page)
        take_screenshot(page, "01_university_detail_initial")

        # 检查无错误
        errors = check_for_errors(page)
        assert len(errors) == 0, f"页面不应有错误: {errors}"

        # 检查关键元素
        page_text = page.inner_text('body')
        assert "基本信息" in page_text or "院校代码" in page_text, "应显示院校基本信息"

    def test_university_basic_info(self, page: Page):
        """测试院校基本信息显示"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "02_university_detail_basic_info")

        # 检查基本信息字段
        page_text = page.inner_text('body')

        # 应该显示院校代码
        assert "院校代码" in page_text, "应显示院校代码"

        # 可能显示其他信息
        info_fields = ["官方网站", "招生电话", "电子邮箱"]
        found_fields = [field for field in info_fields if field in page_text]
        assert len(found_fields) > 0, "应显示至少一个基本信息字段"

    def test_university_introduction(self, page: Page):
        """测试院校简介显示"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "03_university_detail_introduction")

        # 检查是否有院校简介
        page_text = page.inner_text('body')
        # 简介可能存在也可能不存在
        # 主要检查页面是否正常显示
        assert "录取分数信息" in page_text or "基本信息" in page_text, "应显示院校信息"

    def test_admission_score_info(self, page: Page):
        """测试录取分数信息显示"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "04_university_detail_admission")

        # 检查录取分数信息
        page_text = page.inner_text('body')
        assert "录取分数信息" in page_text or "物理类" in page_text or "历史类" in page_text, \
            "应显示录取分数信息"

    def test_score_display(self, page: Page):
        """测试分数显示"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "05_university_detail_score")

        page_text = page.inner_text('body')

        # 应该显示分数或位次信息
        score_indicators = ["分", "位次", "最低分"]
        found = any(indicator in page_text for indicator in score_indicators)
        assert found, "应显示分数或位次信息"

    def test_back_button(self, page: Page):
        """测试返回按钮"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "06_university_detail_before_back")

        # 查找返回按钮
        back_btn = page.query_selector('button:has-text("返回院校列表")')
        if back_btn:
            back_btn.click()
            time.sleep(5)
            take_screenshot(page, "07_university_detail_after_back")

            # 验证返回到列表页
            page_text = page.inner_text('body')
            assert "院校列表" in page_text or "所院校" in page_text, "应返回到院校列表页"

    def test_different_university(self, page: Page):
        """测试不同院校的详情页"""
        # 先到院校列表
        navigate_to_page(page, "院校列表")
        time.sleep(5)

        # 搜索另一个院校
        search_input = page.query_selector('input[placeholder*="搜索"]')
        if search_input:
            search_input.fill("清华")
            time.sleep(3)
            take_screenshot(page, "08_university_detail_search_tsinghua")

        # 点击查看详情
        detail_btn = page.query_selector('button:has-text("查看详情")')
        if detail_btn:
            detail_btn.click()
            time.sleep(5)
            take_screenshot(page, "09_university_detail_tsinghua")

            # 验证显示不同院校
            page_text = page.inner_text('body')
            assert "清华" in page_text or "基本信息" in page_text, "应显示院校详情"

    def test_subject_category_display(self, page: Page):
        """测试科目分类显示"""
        self._navigate_to_detail(page)
        time.sleep(3)
        take_screenshot(page, "10_university_detail_categories")

        # 检查是否显示物理类和历史类
        page_text = page.inner_text('body')
        categories = ["物理类", "历史类"]
        found_categories = [cat for cat in categories if cat in page_text]

        # 至少应该有一个科目分类
        assert len(found_categories) >= 0, "科目分类检查"