# Role
你是一位精通 Python 和 Streamlit 的高级数据可视化工程师，擅长开发高考志愿填报辅助系统。

# Task
请基于 Streamlit 在当前目录下构建一个可扩展的"高考志愿填报助手"，用于展示中国高考往年录取数据（重点是辽宁省 2025 提前批录取数据）。

# Technical Stack
- Language: Python 3.10
- Package Manager: UV
- Framework: Streamlit
- Data: Pandas, JSON
- Visualization: Plotly
- Models: Pydantic

# Data Structure
数据存放于 `data/` 文件夹。路径规则：`data/[省份]/[年份]/`。

文件命名规则：
- `rank_table_w.tsv` - 历史类/文科一分一段表（列：分数、人数、累计）
- `rank_table_l.tsv` - 物理类/理科一分一段表
- `admission_1.json` - 提前批院校录取数据
- `admission_2.json` - 特殊类型批
- `admission_3.json` - 常规批

院校录取信息 JSON 示例：
```json
{
  "name": "北京电子科技学院",
  "code": "P018",
  "year": 2025,
  "official_website": "https://www.besti.edu.cn",
  "admission_phone": "",
  "email": "",
  "introduction": "index",
  "admission_score": {
    "year": 2025,
    "liaoning": [
      {
        "code": "P018",
        "category": "历史类",
        "min_score": "634",
        "batch": "2025年辽宁省普通高等学校招生录取普通类本科提前批录取最低分",
        "rank": "426"
      }
    ]
  }
}
```

# Project Structure
```
uni-admit-ai/
├── pyproject.toml              # UV 项目配置
├── README.md                   # 项目说明文档
├── streamlit_app.py            # 主入口文件
├── app_pages/                  # 页面模块目录
│   ├── __init__.py
│   ├── rank_to_score.py        # 位次查分数页面
│   ├── score_to_university.py  # 分数推荐院校页面
│   ├── university_list.py      # 院校列表页面
│   └── university_detail.py    # 院校详情页面
├── core/                       # 核心业务逻辑
│   ├── __init__.py
│   ├── config.py               # 配置常量定义
│   ├── data_loader.py          # 数据加载器
│   ├── rank_calculator.py      # 位次计算逻辑
│   └── university_filter.py    # 院校筛选逻辑
├── models/                     # 数据模型定义
│   ├── __init__.py
│   ├── schemas.py              # Pydantic 数据模型
│   └── enums.py                # 枚举类型定义
├── components/                 # 可复用 UI 组件
│   ├── __init__.py
│   ├── selectors.py            # 共用选择器组件
│   └── charts.py               # 图表组件
├── tests/                      # UI 测试
│   ├── __init__.py
│   ├── conftest.py             # 测试配置和 fixtures
│   ├── test_rank_to_score.py
│   ├── test_score_to_university.py
│   ├── test_university_list.py
│   ├── test_university_detail.py
│   └── screenshots/            # 测试截图保存目录
├── data/                       # 数据目录
│   └── 辽宁/2025/
└── .streamlit/
    └── config.toml             # Streamlit 配置
```

# Functional Requirements

## 全局选择器
顶部有年份选择、省份选择、科目（物理/历史）选择、批次选择。各页面共用。

## 4大功能页面（侧边栏导航，默认进入位次查分数）

### 1. 位次查分数
- 输入位次后，根据顶部的选择，程序自动从 `rank_table_*.tsv` 中查询对应的分数
- 计算冲保稳区间（默认：冲+5~10分、稳±5分、保-10~15分，可调）
- 显示冲保稳分数区间和对应位次
- 点击"查看推荐院校"按钮跳转到分数推荐院校页面

### 2. 分数推荐院校
- 根据顶部的选择+用户输入的分数范围匹配院校
- 支持按"院校名称"或"院校代码"模糊搜索
- 支持 Plotly 条形图展示当前筛选条件下录取分数最高的前 10 所院校
- 分页显示院校列表
- 从下拉框选择院校后点击"查看详情"按钮跳转到院校详情页

### 3. 院校列表
- 展示院校名称、官网、物理最低分及位次、历史最低分及位次
- 根据顶部的选择动态变化
- 支持按"院校名称"或"院校代码"模糊搜索
- 分页显示
- 从下拉框选择院校后点击"查看详情"按钮跳转到院校详情页

### 4. 院校详情页
- 展示院校名称、官网、电话、邮箱、简介
- 展示该院校的录取分数信息（物理类/历史类）
- 有返回按钮

# Code Quality Requirements
- 模块化、函数化、类型提示、完整注释、异常处理
- 使用 `@st.cache_data` 缓存数据加载
- 动态扫描 `data/` 目录获取可用省份、年份、批次

# Important Notes

## Material 图标
使用 Streamlit 的 Material 图标时，必须使用有效的图标名称：
- ✅ `:material/analytics:` - 分析
- ✅ `:material/school:` - 学校
- ✅ `:material/format_list_bulleted:` - 列表
- ✅ `:material/info:` - 信息
- ❌ `:material/ranking:` - 不支持
- ❌ `:material/list:` - 不支持

## 页面跳转
使用 `st.selectbox` + `st.button` 组合实现跳转，而不是 `st.dataframe` 的行选择功能（不稳定）：
```python
col1, col2 = st.columns([3, 1])
with col1:
    selected = st.selectbox("选择院校", options=[...])
with col2:
    if st.button("查看详情", type="primary"):
        st.session_state.detail_university_code = selected_code
        st.switch_page("app_pages/university_detail.py")
```

# Test Requirements

## 测试框架
- pytest + pytest-playwright
- 测试时自动截图，保存到 `tests/screenshots/`
- 截图命名格式：`{YYYYMMDD_HHMMSS}_{序号}_{测试名称}.png`

## 测试内容
为每个页面编写 UI 功能测试：
- 页面加载验证
- 关键功能验证
- 页面跳转验证
- 搜索功能验证

## 测试依赖
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-playwright>=0.4.0",
    "playwright>=1.40.0",
]
```

## 运行测试
```bash
# 安装测试依赖
uv pip install pytest pytest-playwright
uv run playwright install chromium

# 运行测试
uv run pytest tests/ -v
```

# Verification Requirements
1. 必须成功启动应用
2. 所有页面无报错
3. 所有 UI 测试通过
4. 截图正常保存

## 热重载特性
Streamlit 支持热重载（Hot Reload），当代码文件发生变化时，应用会自动重新加载，无需手动重启服务。这大大提高了开发效率。