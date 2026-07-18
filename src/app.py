"""MATH路OS - Main Application window with stacked pages, navigation bar, and black-hole theme."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QFontDatabase

from style import BG_DARK, CYAN, PURPLE, GREEN, TEXT_MUTED, STYLESHEET
from modules.home_page import HomePage
from modules.function_plotter import FunctionPlotterPage
from modules.formula_editor import FormulaEditorPage
from modules.math_history import MathHistoryPage
from modules.number_theory_basics import NumberTheoryBasicsPage
from modules.physics_simulator import PhysicsSimulatorPage


class NavButton(QPushButton):
    """Navigation button in the top nav bar."""

    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(f"{icon} {text}".strip(), parent)
        self.setObjectName("nav-link")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self.setProperty("class", "nav-link")


class NavBar(QFrame):
    """Top navigation bar with MATH路OS branding and nav buttons."""

    navigate = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("navbar")
        self._buttons: dict[str, NavButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(4)

        # ── Brand ──
        brand = QLabel("MATH路OS")
        brand.setStyleSheet("""
            font-family: 'Orbitron', 'Microsoft YaHei';
            font-size: 20px;
            font-weight: 700;
            color: #00d4ff;
            background: transparent;
        """)
        layout.addWidget(brand)

        # Divider
        divider = QLabel("|")
        divider.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 16px; margin: 0 12px; background: transparent;")
        layout.addWidget(divider)

        # ── Nav Links ──
        nav_items = [
            ("home", "🏠 首页"),
            ("function-plotter", "📈 函数"),
            ("formula-editor", "📝 公式"),
            ("math-history", "📜 数学史"),
            ("number-theory-basics", "🔢 数论"),
            ("physics-simulator", "⚛️ 模拟"),
        ]

        for route, label in nav_items:
            btn = NavButton(label)
            btn.clicked.connect(lambda checked, r=route: self.navigate.emit(r))
            layout.addWidget(btn)
            self._buttons[route] = btn

        layout.addStretch()

        # Version
        version = QLabel("v2.0")
        version.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; background: transparent;")
        layout.addWidget(version)

    def set_active(self, route: str):
        for key, btn in self._buttons.items():
            btn.setChecked(key == route)
            if key == route:
                btn.setProperty("nav-active", True)
            else:
                btn.setProperty("nav-active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATH路OS - 沉浸式数学学习系统")
        self.resize(1280, 820)
        self.setMinimumSize(1000, 680)

        # ── Central Widget ──
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Nav Bar ──
        self._navbar = NavBar()
        self._navbar.navigate.connect(self._on_navigate)
        root.addWidget(self._navbar)

        # ── Page Stack ──
        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        # ── Register Pages ──
        self._pages: dict[str, QWidget] = {}

        # Home page
        home = HomePage()
        home.navigate.connect(self._on_navigate)
        self._add_page("home", home)

        # Function plotter
        self._add_page("function-plotter", FunctionPlotterPage())

        # Formula editor
        self._add_page("formula-editor", FormulaEditorPage())

        # Math history
        self._add_page("math-history", MathHistoryPage())

        # Number theory basics
        self._add_page("number-theory-basics", NumberTheoryBasicsPage())

        # Physics simulator
        self._add_page("physics-simulator", PhysicsSimulatorPage())

        # ── Start on home ──
        self._navigate_to("home")

    def _add_page(self, route: str, widget: QWidget):
        self._pages[route] = widget
        self._stack.addWidget(widget)

    def _on_navigate(self, route: str):
        self._navigate_to(route)

    def _navigate_to(self, route: str):
        if route in self._pages:
            self._stack.setCurrentWidget(self._pages[route])
            self._navbar.set_active(route)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    # Set default font
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
