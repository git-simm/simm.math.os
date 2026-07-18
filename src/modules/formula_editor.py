"""Formula editor with enhanced LaTeX rendering, geometry canvas, and parameter sliders."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QGroupBox,
    QSlider, QSplitter, QTabWidget, QLineEdit,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer, Signal, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QFontDatabase,
    QPainterPath, QMouseEvent, QWheelEvent,
)

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED, AMBER

# ── Common LaTeX formulas ──────────────────────────────────────
COMMON_FORMULAS = [
    ("勾股定理", r"a^2 + b^2 = c^2"),
    ("求根公式", r"x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}"),
    ("欧拉公式", r"e^{i\pi} + 1 = 0"),
    ("二项式定理", r"(a+b)^n = \sum_{k=0}^n \binom{n}{k} a^{n-k} b^k"),
    ("三角恒等式", r"\sin^2\theta + \cos^2\theta = 1"),
    ("微积分基础", r"\frac{d}{dx}x^n = nx^{n-1}"),
    ("积分公式", r"\int x^n dx = \frac{x^{n+1}}{n+1} + C"),
    ("级数展开", r"e^x = \sum_{n=0}^\infty \frac{x^n}{n!}"),
    ("贝叶斯定理", r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}"),
    ("傅里叶变换", r"X(\omega) = \int_{-\infty}^\infty x(t)e^{-j\omega t}dt"),
]

# ── Geometry shapes for the interactive canvas ────────────────
SHAPES = ["circle", "square", "triangle", "parabola", "ellipse"]


class GeometryCanvas(QWidget):
    """Interactive geometry canvas with draggable shapes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 350)
        self._shape = "circle"
        self._params = {"radius": 80, "angle": 0, "x": 200, "y": 175}
        self._dragging = False
        self._drag_start = None
        self.setMouseTracking(True)

    def set_shape(self, shape: str):
        self._shape = shape
        self.update()

    def set_params(self, **kwargs):
        self._params.update(kwargs)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        self._dragging = True
        self._drag_start = event.position()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            delta = event.position() - self._drag_start
            self._params["x"] += delta.x()
            self._params["y"] += delta.y()
            self._drag_start = event.position()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._dragging = False

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y() / 120
        self._params["radius"] = max(10, self._params["radius"] + delta * 10)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Dark background with grid
        p.fillRect(0, 0, w, h, QColor("#0a0e1a"))

        # Grid lines
        grid_pen = QPen(QColor("#1e293b"))
        grid_pen.setWidthF(0.5)
        p.setPen(grid_pen)
        step = 40
        for i in range(0, w, step):
            p.drawLine(i, 0, i, h)
        for j in range(0, h, step):
            p.drawLine(0, j, w, j)

        # Axes
        axis_pen = QPen(QColor("#475569"))
        axis_pen.setWidthF(1.0)
        p.setPen(axis_pen)
        p.drawLine(w // 2, 0, w // 2, h)
        p.drawLine(0, h // 2, w, h // 2)

        # Shape drawing
        px, py = self._params["x"], self._params["y"]
        r = self._params["radius"]
        color = QColor(CYAN)

        p.setBrush(QBrush(QColor(0, 212, 255, 40)))
        pen = QPen(color)
        pen.setWidthF(2.5)
        p.setPen(pen)

        if self._shape == "circle":
            p.drawEllipse(int(px - r), int(py - r), int(2 * r), int(2 * r))
            # Center point
            p.setBrush(QBrush(color))
            p.drawEllipse(int(px - 3), int(py - 3), 6, 6)
            # Radius line
            p.setPen(QPen(QColor(GREEN), 1, Qt.PenStyle.DashLine))
            p.drawLine(int(px), int(py), int(px + r), int(py))

        elif self._shape == "square":
            p.drawRect(int(px - r), int(py - r), int(2 * r), int(2 * r))
            # Diagonal
            p.setPen(QPen(QColor(PURPLE), 1, Qt.PenStyle.DashLine))
            p.drawLine(int(px - r), int(py - r), int(px + r), int(py + r))

        elif self._shape == "triangle":
            h_tri = r * math.sqrt(3)
            path = QPainterPath()
            path.moveTo(px, py - h_tri / 1.5)
            path.lineTo(px - r, py + h_tri / 3)
            path.lineTo(px + r, py + h_tri / 3)
            path.closeSubpath()
            p.drawPath(path)

        elif self._shape == "parabola":
            path = QPainterPath()
            path.moveTo(px - r * 1.5, py + r)
            for t in range(-100, 101):
                x = px + t * r * 1.5 / 100
                y = py - (t / 100) ** 2 * r
                path.lineTo(x, y)
            p.drawPath(path)
            # Focus point
            p.setBrush(QBrush(QColor(ROSE)))
            p.setPen(Qt.PenStyle.NoPen)
            focal_y = py - r + r / 4
            p.drawEllipse(int(px - 4), int(focal_y - 4), 8, 8)

        elif self._shape == "ellipse":
            p.drawEllipse(int(px - r * 1.4), int(py - r * 0.7), int(2.8 * r), int(1.4 * r))
            # Foci
            e = 0.8
            c = r * 1.4 * e
            p.setBrush(QBrush(QColor(AMBER)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(px - c - 3), int(py - 3), 6, 6)
            p.drawEllipse(int(px + c - 3), int(py - 3), 6, 6)


import math  # needed for triangle height


class FormulaRendererWidget(QWidget):
    """Renders LaTeX formulas using matplotlib's built-in TeX support."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 200)
        self._latex = r"e^{i\pi} + 1 = 0"
        self._dpi = 100

        self._fig = Figure(figsize=(6, 2), dpi=self._dpi, facecolor="#0a0e1a")
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor("#0a0e1a")
        self._ax.axis("off")
        self._canvas = FigureCanvasQTAgg(self._fig)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._canvas)
        self._render()

    def set_latex(self, latex: str):
        self._latex = latex
        self._render()

    def _render(self):
        self._ax.clear()
        self._ax.set_facecolor("#0a0e1a")
        self._ax.axis("off")
        try:
            self._ax.text(0.5, 0.5, f"${self._latex}$", fontsize=28,
                          ha="center", va="center", color="#00d4ff",
                          transform=self._ax.transAxes)
        except Exception:
            self._ax.text(0.5, 0.5, self._latex, fontsize=18,
                          ha="center", va="center", color="#f43f5e",
                          transform=self._ax.transAxes)
        self._canvas.draw()


class FormulaEditorPage(QWidget):
    """Main formula editor page with LaTeX input, render, geometry canvas, and presets."""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        # Title
        title = QLabel("📝 公式编辑 & 几何画板")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {CYAN}; font-family: 'Orbitron','Microsoft YaHei';")
        root.addWidget(title)

        # ── Main horizontal split ──
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(splitter, 1)

        # ── Left Panel ──
        left = QFrame()
        left.setObjectName("glass-panel")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        # LaTeX Input
        input_label = QLabel("LaTeX 公式输入")
        input_label.setStyleSheet(f"color: {GREEN}; font-weight: 700; font-size: 13px;")
        left_layout.addWidget(input_label)

        self._latex_input = QTextEdit()
        self._latex_input.setPlaceholderText("输入 LaTeX 公式，例如：\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}")
        self._latex_input.setMaximumHeight(80)
        self._latex_input.setStyleSheet(f"""
            QTextEdit {{
                background: #0a0e1a;
                border: 1px solid {CYAN}50;
                border-radius: 6px;
                color: {TEXT_MUTED};
                font-family: 'Fira Code', 'Consolas';
                font-size: 13px;
                padding: 8px;
            }}
            QTextEdit:focus {{ border-color: {CYAN}; }}
        """)
        self._latex_input.textChanged.connect(self._on_latex_changed)
        left_layout.addWidget(self._latex_input)

        # Render button
        render_btn = QPushButton("🎨 渲染 LaTeX")
        render_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        render_btn.setStyleSheet(f"""
            QPushButton {{ background: {CYAN}20; border: 1px solid {CYAN}50; color: {CYAN}; border-radius: 6px; padding: 8px; font-weight: 700; }}
            QPushButton:hover {{ background: {CYAN}30; border-color: {CYAN}; }}
        """)
        render_btn.clicked.connect(lambda: self._formula_render.set_latex(self._latex_input.toPlainText().strip() or "e^{i\\pi}+1=0"))
        left_layout.addWidget(render_btn)

        # ── Common Formulas ──
        preset_group = QGroupBox("常用公式 (点击插入)")
        preset_group.setStyleSheet(f"""
            QGroupBox {{ color: {PURPLE}; font-size: 11px; font-weight: 700; border: 1px solid {PURPLE}30; border-radius: 6px; margin-top: 8px; padding-top: 14px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; }}
        """)
        preset_layout = QVBoxLayout(preset_group)
        preset_layout.setSpacing(4)

        for name, formula in COMMON_FORMULAS:
            btn = QPushButton(f"{name}: {formula[:50]}{'...' if len(formula) > 50 else ''}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; border: none; color: {TEXT_MUTED}; font-size: 11px; text-align: left; padding: 4px 8px; }}
                QPushButton:hover {{ color: {CYAN}; background: {CYAN}10; border-radius: 4px; }}
            """)
            btn.clicked.connect(lambda checked, f=formula: self._latex_input.setPlainText(f))
            preset_layout.addWidget(btn)
        left_layout.addWidget(preset_group)

        left_layout.addStretch()
        splitter.addWidget(left)

        # ── Right: Tab Widget with Render + Geometry Canvas ──
        right = QTabWidget()
        right.setStyleSheet(f"""
            QTabWidget::pane {{ background: transparent; border: none; }}
            QTabBar::tab {{ color: {TEXT_MUTED}; padding: 8px 20px; border-bottom: 2px solid transparent; }}
            QTabBar::tab:selected {{ color: {CYAN}; border-bottom: 2px solid {CYAN}; }}
            QTabBar::tab:hover:!selected {{ color: {GREEN}; }}
        """)

        # Tab 1: Formula Render
        self._formula_render = FormulaRendererWidget()
        self._formula_render.set_latex(r"e^{i\pi} + 1 = 0")
        right.addTab(self._formula_render, "📐 LaTeX 渲染")

        # Tab 2: Geometry Canvas
        geo_panel = QWidget()
        geo_layout = QVBoxLayout(geo_panel)
        geo_layout.setContentsMargins(0, 0, 0, 0)

        geo_toolbar = QHBoxLayout()
        geo_toolbar.setSpacing(6)
        for shape in SHAPES:
            btn = QPushButton(shape.capitalize())
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; border: 1px solid {CYAN}40; color: {TEXT_MUTED}; border-radius: 4px; padding: 5px 12px; font-size: 11px; }}
                QPushButton:hover {{ border-color: {CYAN}; color: {CYAN}; }}
            """)
            btn.clicked.connect(lambda checked, s=shape: self._geo_canvas.set_shape(s))
            geo_toolbar.addWidget(btn)
        geo_layout.addLayout(geo_toolbar)

        geo_hint = QLabel("🖱 拖动移动图形 | 滚轮缩放 | 左上角：点击切换图形")
        geo_hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px;")
        geo_layout.addWidget(geo_hint)

        self._geo_canvas = GeometryCanvas()
        geo_layout.addWidget(self._geo_canvas, 1)
        right.addTab(geo_panel, "📏 几何画板")

        splitter.addWidget(right)
        splitter.setSizes([350, 650])

    def _on_latex_changed(self):
        # Live preview: debounce with a small timer
        latex = self._latex_input.toPlainText().strip()
        if latex:
            self._formula_render.set_latex(latex)
