# 高考志愿填报助手

基于 Streamlit 构建的高考志愿填报辅助系统，用于展示中国高考往年录取数据。

## 功能特性

- **位次查分数**: 输入位次查询对应分数，计算冲保稳区间
- **分数推荐院校**: 根据分数范围筛选院校，支持模糊搜索
- **院校列表**: 展示院校基本信息，支持搜索和跳转
- **院校详情**: 展示院校完整信息

## 技术栈

- Python 3.10
- Streamlit
- Pandas
- Plotly
- Pydantic

## 快速开始

```bash
# 安装依赖
uv sync

# 启动应用
uv run streamlit run streamlit_app.py
```

## 数据结构

数据存放于 `data/` 文件夹，路径规则：`data/[省份]/[年份]/`

```
data/
└── 辽宁/
    └── 2025/
        ├── rank_table_l.tsv    # 物理类一分一段表
        ├── rank_table_w.tsv    # 历史类一分一段表
        └── admission_1.json    # 提前批院校录取数据
```

### 文件命名规则

| 文件模式 | 含义 |
|---------|------|
| `rank_table_l.tsv` | 物理类/理科一分一段表 |
| `rank_table_w.tsv` | 历史类/文科一分一段表 |
| `admission_1.json` | 提前批 |
| `admission_2.json` | 特殊类型批 |
| `admission_3.json` | 常规批 |

## 测试

本项目使用 Playwright 进行 UI 自动化测试，测试时会自动截图并保存。

### 安装测试依赖

```bash
# 安装测试依赖
uv pip install pytest pytest-playwright

# 安装 Playwright 浏览器
uv run playwright install chromium
```

### 运行测试

```bash
# 运行所有测试
uv run pytest tests/ -v

# 运行单个测试文件
uv run pytest tests/test_university_list.py -v

# 运行特定测试用例
uv run pytest tests/test_university_list.py::TestUniversityListPage::test_navigate_to_detail -v
```

### 测试覆盖

| 测试文件 | 测试内容 | 测试数量 |
|---------|---------|---------|
| `test_rank_to_score.py` | 位次查分数页面 | 4 |
| `test_score_to_university.py` | 分数推荐院校页面 | 6 |
| `test_university_list.py` | 院校列表页面 | 7 |
| `test_university_detail.py` | 院校详情页面 | 8 |

### 截图文件

测试过程中会自动截图，保存在 `tests/screenshots/` 目录，命名格式：

```
{YYYYMMDD_HHMMSS}_{序号}_{测试名称}.png
```

例如：
- `20260313_142946_01_rank_to_score_initial.png`
- `20260313_143123_06_score_to_university_after_nav.png`

## 项目结构

```
uni-admit-ai/
├── streamlit_app.py            # 主入口文件
├── app_pages/                  # 页面模块
│   ├── rank_to_score.py        # 位次查分数页面
│   ├── score_to_university.py  # 分数推荐院校页面
│   ├── university_list.py      # 院校列表页面
│   └── university_detail.py    # 院校详情页面
├── core/                       # 核心业务逻辑
│   ├── config.py               # 配置常量
│   ├── data_loader.py          # 数据加载器
│   ├── rank_calculator.py      # 位次计算
│   └── university_filter.py    # 院校筛选
├── models/                     # 数据模型
│   ├── enums.py                # 枚举类型
│   └── schemas.py              # Pydantic 模型
├── components/                 # UI 组件
│   ├── selectors.py            # 共用选择器
│   └── charts.py               # 图表组件
├── tests/                      # 测试目录
│   ├── conftest.py             # 测试配置
│   ├── test_*.py               # 测试文件
│   └── screenshots/            # 测试截图
├── data/                       # 数据目录
└── .streamlit/
    └── config.toml             # Streamlit 配置
```