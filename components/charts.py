"""图表组件

使用 Plotly 创建可视化图表。
"""

from typing import Optional

import plotly.graph_objects as go
import streamlit as st

from models.enums import SubjectType
from models.schemas import University
from core.university_filter import get_university_score_info, parse_score


def create_score_distribution_chart(
    universities: list[University],
    subject_type: SubjectType,
    top_n: int = 10,
) -> Optional[go.Figure]:
    """创建院校分数分布条形图

    展示录取分数最高的前 N 所院校。

    Args:
        universities: 院校列表
        subject_type: 科目类型
        top_n: 显示前 N 所院校

    Returns:
        Plotly Figure 对象
    """
    if not universities:
        return None

    # 收集院校分数数据
    data = []
    for university in universities:
        score_info = get_university_score_info(university, subject_type)
        if score_info["min_score"]:
            data.append(
                {
                    "name": university.name,
                    "score": score_info["min_score"],
                    "rank": score_info["min_rank"],
                }
            )

    if not data:
        return None

    # 按分数排序，取前 N 个
    data.sort(key=lambda x: x["score"], reverse=True)
    data = data[:top_n]

    # 创建条形图
    fig = go.Figure(
        data=[
            go.Bar(
                x=[d["score"] for d in data],
                y=[d["name"] for d in data],
                orientation="h",
                text=[f"{d['score']}分 (位次: {d['rank'] or 'N/A'})" for d in data],
                textposition="outside",
                marker_color="#1E88E5",
            )
        ]
    )

    fig.update_layout(
        title=f"录取分数最高的前 {len(data)} 所院校",
        xaxis_title="最低录取分数",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),  # 高分在上
        height=max(400, len(data) * 40),
        margin=dict(l=150, r=50, t=50, b=50),
        showlegend=False,
    )

    return fig


def create_rank_range_chart(
    score: int,
    ranges: dict,
) -> go.Figure:
    """创建冲保稳区间可视化图表

    Args:
        score: 基准分数
        ranges: 冲保稳区间数据

    Returns:
        Plotly Figure 对象
    """
    # 准备数据
    categories = []
    scores_min = []
    scores_max = []
    colors = []

    range_config = {
        "reach": {"name": "冲", "color": "#FF7043"},
        "stable": {"name": "稳", "color": "#66BB6A"},
        "safety": {"name": "保", "color": "#42A5F5"},
    }

    for range_type in ["reach", "stable", "safety"]:
        if range_type in ranges:
            config = range_config[range_type]
            categories.append(config["name"])
            scores_min.append(ranges[range_type]["min_score"])
            scores_max.append(ranges[range_type]["max_score"])
            colors.append(config["color"])

    # 创建条形图
    fig = go.Figure()

    for i, (cat, min_s, max_s, color) in enumerate(
        zip(categories, scores_min, scores_max, colors)
    ):
        fig.add_trace(
            go.Bar(
                name=cat,
                x=[cat],
                y=[max_s - min_s],
                base=min_s,
                marker_color=color,
                text=f"{min_s}-{max_s}分",
                textposition="inside",
            )
        )

    # 添加基准分数线
    fig.add_hline(
        y=score,
        line_dash="dash",
        line_color="red",
        annotation_text=f"基准分数: {score}",
        annotation_position="right",
    )

    fig.update_layout(
        title="冲保稳区间分析",
        xaxis_title="策略区间",
        yaxis_title="分数",
        height=400,
        showlegend=False,
        barmode="group",
    )

    return fig


def display_chart(figure: Optional[go.Figure]) -> None:
    """显示图表

    Args:
        figure: Plotly Figure 对象
    """
    if figure:
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info("暂无数据可显示")