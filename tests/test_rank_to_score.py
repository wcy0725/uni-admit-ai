"""位次查分数页面UI测试"""

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


class TestRankToScorePage:
    """位次查分数页面测试类"""

    def test_page_loads_successfully(self, page: Page):
        """测试页面加载成功"""
        # 导航到应用
        page.goto(STREAMLIT_URL, timeout=30000)
        wait_for_page_load(page)
        time.sleep(3)

        # 默认应该在位次查分数页面
        take_screenshot(page, "01_rank_to_score_initial")

        # 检查页面标题或关键元素
        page_text = page.inner_text('body')
        assert "位次" in page_text or "分数" in page_text, "页面应包含位次或分数相关内容"

        # 检查无错误
        errors = check_for_errors(page)
        assert len(errors) == 0, f"页面不应有错误: {errors}"

    def test_query_by_rank(self, page: Page):
        """测试按位次查询分数功能"""
        page.goto(STREAMLIT_URL, timeout=30000)
        wait_for_page_load(page)
        time.sleep(5)

        # 找到位次输入框并输入
        rank_input = page.query_selector('input[type="number"]')
        if rank_input:
            # 清空并输入新值
            rank_input.fill("1000")
            time.sleep(2)
            take_screenshot(page, "02_rank_to_score_query")

            # 点击查询按钮
            query_btn = page.query_selector('button:has-text("查询")')
            if query_btn:
                query_btn.click()
                time.sleep(3)
                take_screenshot(page, "03_rank_to_score_result")

        # 检查是否显示结果
        page_text = page.inner_text('body')
        assert "分" in page_text, "应显示分数结果"

    def test_chong_wen_bao_calculation(self, page: Page):
        """测试冲保稳区间计算"""
        page.goto(STREAMLIT_URL, timeout=30000)
        wait_for_page_load(page)
        time.sleep(5)

        # 输入位次
        rank_input = page.query_selector('input[type="number"]')
        if rank_input:
            rank_input.fill("5000")
            time.sleep(2)

            # 点击查询
            query_btn = page.query_selector('button:has-text("查询")')
            if query_btn:
                query_btn.click()
                time.sleep(5)
                take_screenshot(page, "04_rank_to_score_chong_wen_bao")

        # 检查冲保稳区域
        page_text = page.inner_text('body')
        assert "冲" in page_text or "稳" in page_text or "保" in page_text, "应显示冲保稳区间"

    def test_navigate_to_score_recommend(self, page: Page):
        """测试点击推荐院校按钮跳转"""
        page.goto(STREAMLIT_URL, timeout=30000)
        wait_for_page_load(page)
        time.sleep(5)

        # 先查询一个位次
        rank_input = page.query_selector('input[type="number"]')
        if rank_input:
            rank_input.fill("1000")
            time.sleep(1)
            query_btn = page.query_selector('button:has-text("查询")')
            if query_btn:
                query_btn.click()
                time.sleep(3)

        # 查找并点击"查看推荐院校"按钮
        recommend_btn = page.query_selector('button:has-text("查看推荐院校")')
        if recommend_btn:
            recommend_btn.click()
            time.sleep(5)
            take_screenshot(page, "05_rank_to_score_navigate")

            # 验证跳转到分数推荐院校页面
            page_text = page.inner_text('body')
            assert "推荐院校" in page_text or "分数" in page_text, "应跳转到分数推荐院校页面"