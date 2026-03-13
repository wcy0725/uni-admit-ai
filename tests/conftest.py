"""测试配置和共享fixtures"""

import os
import time
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Page, Playwright, Browser


# 截图保存目录
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Streamlit 应用地址
STREAMLIT_URL = "http://localhost:8501"


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """创建浏览器实例"""
    browser = playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Generator[Page, None, None]:
    """创建页面实例"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def take_screenshot(page: Page, name: str) -> str:
    """
    截取页面截图并保存

    Args:
        page: Playwright页面对象
        name: 截图名称（不含扩展名）

    Returns:
        截图文件路径
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png"
    filepath = SCREENSHOT_DIR / filename
    page.screenshot(path=str(filepath))
    return str(filepath)


def wait_for_page_load(page: Page, timeout: int = 10000) -> None:
    """
    等待页面加载完成

    Args:
        page: Playwright页面对象
        timeout: 超时时间（毫秒）
    """
    page.wait_for_load_state("networkidle", timeout=timeout)


def check_for_errors(page: Page) -> list[str]:
    """
    检查页面是否有错误

    Args:
        page: Playwright页面对象

    Returns:
        错误信息列表
    """
    errors = []
    error_elements = page.query_selector_all('[class*="stException"], [class*="error"]')
    for elem in error_elements:
        text = elem.inner_text()
        if text:
            errors.append(text)
    return errors


def navigate_to_page(page: Page, page_name: str) -> None:
    """
    导航到指定页面

    Args:
        page: Playwright页面对象
        page_name: 页面名称（如"院校列表"、"分数推荐院校"等）
    """
    page.goto(STREAMLIT_URL, timeout=30000)
    wait_for_page_load(page)
    page.click(f'text={page_name}')
    wait_for_page_load(page)