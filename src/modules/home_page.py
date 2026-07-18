"""Home page - immersive knowledge graph with custom force-directed graph + particle background + quotes."""

from __future__ import annotations

import math
import random
from typing import Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSizePolicy,
)
from PySide6.QtCore import (
    Qt, QTimer, QRectF, Signal,
)
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient,
    QRadialGradient, QPainterPath,
)

from widgets.particle_canvas import ParticleCanvas
from widgets.force_graph import ForceGraphWidget
from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED, AMBER, EMERALD

# ── Quotations ─────────────────────────────────────────────────
QUOTES: list[tuple[str, str]] = [
    ("数学是上帝用来书写宇宙的语言。", "伽利略"),
    ("大自然这本书是用数学语言写成的。", "伽利略"),
    ("数学，如果正确地看它，不但拥有真理，而且也具有至高的美。", "罗素"),
    ("哪里有数学，哪里就有美。", "普罗克洛斯"),
    ("纯数学，就其本质而言，是逻辑思想的诗篇。", "爱因斯坦"),
    ("数学是符号加逻辑。", "罗素"),
    ("宇宙之大，粒子之微，火箭之速，化工之巧，地球之变，生物之谜，日用之繁，无处不用数学。", "华罗庚"),
]


class QuoteWidget(QWidget):
    """Animated quotation rotator."""

    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self._index = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_quote)
        self._timer.start(6000)

    def _next_quote(self):
        self._index = (self._index + 1) % len(QUOTES)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()

        text, author = QUOTES[self._index]
        text_font = QFont("Microsoft YaHei", 13)
        text_font.setItalic(True)
        p.setFont(text_font)
        p.setPen(QColor(TEXT_MUTED))
        p.drawText(QRectF(0, 4, w, 28), Qt.AlignmentFlag.AlignCenter, text)

        auth_font = QFont("Microsoft YaHei", 10)
        p.setFont(auth_font)
        p.setPen(QColor(CYAN))
        p.drawText(QRectF(0, 34, w, 20), Qt.AlignmentFlag.AlignCenter, "—— " + author)


class HomePage(QWidget):
    """Main home page with particle background, force-directed knowledge graph, and quotes."""

    navigate = Signal(str)

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        # Full page stack: particle bg -> content
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Particle Background ──
        self._particles = ParticleCanvas(self, particle_count=80)
        self._particles.setGeometry(0, 0, 1, 1)

        # ── Main Content ──
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 16, 40, 16)
        content_layout.setSpacing(4)

        # Hero title
        hero = QLabel("MATH·OS")
        hero.setStyleSheet("""
            font-family: 'Orbitron', 'Microsoft YaHei';
            font-size: 32px;
            font-weight: 700;
            color: #00d4ff;
            padding: 0;
            background: transparent;
        """)
        hero.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(hero)

        # Subtitle
        sub = QLabel("沉浸式知识图谱 · 数学基础体系")
        sub.setStyleSheet(f"font-size: 14px; color: {TEXT_MUTED}; font-family: 'Microsoft YaHei'; background: transparent;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(sub)

        content_layout.addSpacing(8)

        # ── Stats Bar ──
        stats = QFrame()
        stats.setStyleSheet(f"""
            QFrame {{
                background: rgba(13, 17, 23, 0.6);
                border: 1px solid rgba(0, 212, 255, 0.15);
                border-radius: 10px;
            }}
        """)
        stats_layout = QHBoxLayout(stats)
        stats_layout.setContentsMargins(20, 8, 20, 8)
        for text in ["📊 5 个知识领域", "📝 200+ 公式", "🔍 实时交互", "🌌 数字宇宙"]:
            lbl = QLabel(text)
            lbl.setStyleSheet(f"color: {CYAN}; font-size: 12px; font-family: 'Microsoft YaHei'; background: transparent;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stats_layout.addWidget(lbl)
        content_layout.addWidget(stats)

        content_layout.addSpacing(8)

        # ── Force-Directed Knowledge Graph ──
        graph_instructions = QLabel("🖱 拖动节点 | 点击跳转 | 中心节点脉冲")
        graph_instructions.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; background: transparent; padding: 0 8px;")
        graph_instructions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(graph_instructions)

        self._graph = ForceGraphWidget()
        self._graph.setStyleSheet("background: transparent;")
        self._graph.setMinimumHeight(420)
        self._graph.node_clicked.connect(self._on_node_click)
        content_layout.addWidget(self._graph, 1)

        # ── Quick Links Row ──
        quick_row = QHBoxLayout()
        quick_row.setSpacing(10)

        links = [
            ("📐 函数绘图", "function-plotter"),
            ("🔢 数论基础", "number-theory-basics"),
            ("📝 公式编辑", "formula-editor"),
            ("⚛️ 物理模拟", "physics-simulator"),
            ("📜 数学史", "math-history"),
        ]
        for label, target in links:
            btn = QPushButton(label)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(13, 17, 23, 0.5);
                    border: 1px solid {CYAN}40;
                    border-radius: 8px;
                    color: {TEXT_MUTED};
                    padding: 8px 16px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    border-color: {CYAN};
                    color: {CYAN};
                    background: rgba(0, 212, 255, 0.08);
                }}
            """)
            btn.clicked.connect(lambda checked, t=target: self.navigate.emit(t))
            quick_row.addWidget(btn)
        content_layout.addLayout(quick_row)

        # ── Quote ──
        quote = QuoteWidget()
        content_layout.addWidget(quote)

        root.addWidget(content)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._particles:
            self._particles.setGeometry(0, 0, self.width(), self.height())

    def _on_node_click(self, node_id: str):
        route_map = {
            "algebra": "function-plotter",
            "geometry": "formula-editor",
            "analysis": "function-plotter",
            "probability": "physics-simulator",
            "linear_algebra": "function-plotter",
            "num_theory": "number-theory-basics",
        }
        target = route_map.get(node_id, node_id)
        self.navigate.emit(target)
