"""Enhanced function plotter with built-in function library, presets, and derivative display."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSlider, QFrame, QGroupBox,
    QComboBox, QSizePolicy, QSplitter, QScrollArea,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from style import CYAN, GREEN, ROSE, TEXT_MUTED, PURPLE


#  Built-in function library 
PRESET_FUNCTIONS: dict[str, dict] = {
    "sin": {
        "name": " sin(x)",
        "fn": lambda x, a, b, c: a * np.sin(b * x + c),
        "eq_template": "y = {a}sin({b}x + {c})",
        "der_template": "y' = {a}{b}cos({b}x+{c})",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": "?|a|?T=2/|b|?c",
    },
    "cos": {
        "name": " cos(x)",
        "fn": lambda x, a, b, c: a * np.cos(b * x + c),
        "eq_template": "y = {a}cos({b}x + {c})",
        "der_template": "y' = -{a}{b}sin({b}x+{c})",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": "in/2os()=sin(+/2)",
    },
    "tan": {
        "name": " tan(x)",
        "fn": lambda x, a, b, c: a * np.tan(b * x + c),
        "eq_template": "y = {a}tan({b}x + {c})",
        "der_template": "y' = {a}{b}sec({b}x+{c})",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": " x=/2+k ?/2 ??",
    },
    "exp": {
        "name": " e^x",
        "fn": lambda x, a, b, c: a * np.exp(b * x) + c,
        "eq_template": "y = {a}e^({b}x) + {c}",
        "der_template": "y' = {a}{b}e^({b}x)",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": "e?.71828'(x)=e^x(0,1)",
    },
    "log": {
        "name": " ln(x)",
        "fn": lambda x, a, b, c: a * np.log(np.abs(b * x) + 1e-10) + c,
        "eq_template": "y = {a}ln({b}x) + {c}",
        "der_template": "y' = {a}/x  (x>0)",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": "e^xx>0n(1)=0",
    },
    "poly2": {
        "name": " ax+bx+c",
        "fn": lambda x, a, b, c: a * x**2 + b * x + c,
        "eq_template": "y = {a}x + {b}x + {c}",
        "der_template": "y' = 2{a}x + {b}",
        "params": {"a": 1.0, "b": 0.0, "c": 0.0},
        "category": "Polynomial",
        "description": "Quadratic parabola, symmetric about vertex x = -b/(2a)",
    },
    "poly3": {
        "name": " ax+bx+cx+d",
        "fn": lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
        "eq_template": "y = {a}x + {b}x + {c}x + {d}",
        "der_template": "y' = 3{a}x + 2{b}x + {c}",
        "params": {"a": 1.0, "b": 0.0, "c": 0.0, "d": 0.0},
        "category": "Polynomial",
        "description": "?1??",
    },
    "sqrt": {
        "name": "??x)",
        "fn": lambda x, a, b, c: a * np.sqrt(np.abs(b * x) + 1e-10) + c,
        "eq_template": "y = {a}?{b}x) + {c}",
        "der_template": "y' = {a}{b}/(2?{b}x))",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "",
        "description": "",
    },
    "sigmoid": {
        "name": "Sigmoid 1/(1+e^(-x))",
        "fn": lambda x, a, b, c: a / (1 + np.exp(-b * x + c)),
        "eq_template": "y = {a}/(1+e^(-{b}x+{c}))",
        "der_template": "y' = {a}{b}(x)(1-(x))",
        "params": {"a": 1.0, "b": 1.0, "c": 0.0},
        "category": "?",
        "description": "S(0,1)?",
    },
    "custom": {
        "name": "",
        "fn": None,
        "eq_template": "",
        "der_template": "",
        "params": {},
        "category": "",
        "description": " Python  np. ?x ",
    },
}


class MatplotlibCanvas(FigureCanvasQTAgg):
    """Matplotlib figure canvas with dark theme."""

    def __init__(self, width=8, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#0a0e1a")
        self.ax = self.fig.add_subplot(111)
        self._apply_dark_theme()
        super().__init__(self.fig)

    def _apply_dark_theme(self):
        self.ax.set_facecolor("#0a0e1a")
        for spine in self.ax.spines.values():
            spine.set_color("#334155")
        self.ax.tick_params(colors="#94a3b8")
        self.ax.xaxis.label.set_color("#e2e8f0")
        self.ax.yaxis.label.set_color("#e2e8f0")
        self.ax.grid(True, color="#1e293b", linewidth=0.5)


class FunctionPlotterPage(QWidget):
    def __init__(self):
        super().__init__()
        self._current_fn = "sin"
        self._params: dict[str, float] = dict(PRESET_FUNCTIONS["sin"]["params"])
        self._x_range = (-10, 10)
        self._init_ui()
        self._plot()

    def _init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        #  Left Control Panel 
        panel = QFrame()
        panel.setObjectName("glass-panel")
        panel.setFixedWidth(340)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(10)

        # Title
        title = QLabel("Function Plotter")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {CYAN}; font-family: 'Orbitron','Microsoft YaHei';")
        panel_layout.addWidget(title)

        #  Preset Selection 
        preset_group = QGroupBox("Built-in Functions")
        preset_group.setStyleSheet(f"""
            QGroupBox {{ color: {GREEN}; font-size: 12px; font-weight: 700; border: 1px solid {GREEN}40; border-radius: 6px; margin-top: 8px; padding-top: 16px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
        """)
        preset_layout = QVBoxLayout(preset_group)
        preset_layout.setSpacing(6)

        self._preset_combo = QComboBox()
        self._preset_combo.setStyleSheet(f"""
            QComboBox {{ background: #0a0e1a; border: 1px solid {CYAN}60; border-radius: 4px; color: {CYAN}; padding: 6px; }}
            QComboBox:hover {{ border-color: {CYAN}; }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{ background: #0d1117; color: #e2e8f0; selection-background-color: {CYAN}30; }}
        """)
        for key, fn in PRESET_FUNCTIONS.items():
            self._preset_combo.addItem(f"{fn['name']}  [{fn['category']}]", key)
        self._preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self._preset_combo)

        # Preset description
        self._preset_desc = QLabel(PRESET_FUNCTIONS["sin"]["description"])
        self._preset_desc.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; padding: 4px;")
        self._preset_desc.setWordWrap(True)
        preset_layout.addWidget(self._preset_desc)

        panel_layout.addWidget(preset_group)

        #  Parameter Sliders 
        self._sliders_widget = QWidget()
        self._sliders_layout = QVBoxLayout(self._sliders_widget)
        self._sliders_layout.setContentsMargins(0, 0, 0, 0)
        self._sliders_layout.setSpacing(6)
        panel_layout.addWidget(self._sliders_widget)

        #  Quick Preset Buttons 
        quick_group = QGroupBox("Quick Examples")
        quick_group.setStyleSheet(f"""
            QGroupBox {{ color: {PURPLE}; font-size: 12px; font-weight: 700; border: 1px solid {PURPLE}40; border-radius: 6px; margin-top: 8px; padding-top: 16px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
        """)
        quick_layout = QVBoxLayout(quick_group)
        quick_layout.setSpacing(4)
        quick_btns = [
            ("sin(2x) - freq double", "sin", {"a": 1, "b": 2, "c": 0}),
            ("2sin(x) - amp double", "sin", {"a": 2, "b": 1, "c": 0}),
            ("sin(x+pi/2) - phase", "sin", {"a": 1, "b": 1, "c": np.pi / 2}),
            ("0.5x^2 - wide para", "poly2", {"a": 0.5, "b": 0, "c": 0}),
            ("2e^x - steep exp", "exp", {"a": 2, "b": 1, "c": 0}),
            ("ln(2x) - shift log", "log", {"a": 1, "b": 2, "c": 0}),
        ]
        for label, fn_key, params in quick_btns:
            btn = QPushButton(label)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; border: 1px solid {TEXT_MUTED}50; color: {TEXT_MUTED}; border-radius: 4px; padding: 4px 8px; font-size: 11px; text-align: left; }}
                QPushButton:hover {{ border-color: {PURPLE}; color: {PURPLE}; }}
            """)
            btn.clicked.connect(lambda checked, k=fn_key, p=params: self._apply_quick_preset(k, p))
            quick_layout.addWidget(btn)
        panel_layout.addWidget(quick_group)

        #  Equation Display 
        self._eq_label = QLabel("y = sin(x)")
        self._eq_label.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {CYAN}; font-family: 'Fira Code','Consolas'; padding: 8px; border: 1px solid {CYAN}50; border-radius: 6px;")
        self._eq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self._eq_label)

        #  Derivative Display 
        self._der_label = QLabel("y' = cos(x)")
        self._der_label.setStyleSheet(f"font-size: 13px; color: {GREEN}; font-family: 'Fira Code','Consolas'; padding: 4px;")
        self._der_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self._der_label)

        #  Range Control 
        range_group = QGroupBox("X ")
        range_group.setStyleSheet(f"""
            QGroupBox {{ color: {TEXT_MUTED}; font-size: 11px; border: 1px solid {TEXT_MUTED}30; border-radius: 4px; margin-top: 6px; padding-top: 12px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; }}
        """)
        range_layout = QHBoxLayout(range_group)
        range_layout.setSpacing(8)
        for label, value in [("-10", -10), ("+10", 10)]:
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
            range_layout.addWidget(lbl)
        panel_layout.addWidget(range_group)

        panel_layout.addStretch()
        root.addWidget(panel)

        #  Right: Matplotlib Canvas 
        self._canvas = MatplotlibCanvas(width=8, height=6, dpi=100)
        root.addWidget(self._canvas, 1)

        # Initialize sliders for default function
        self._build_sliders("sin")

    def _build_sliders(self, fn_key: str):
        """Build parameter sliders for the current function."""
        # Clear existing sliders
        while self._sliders_layout.count():
            item = self._sliders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        fn = PRESET_FUNCTIONS[fn_key]
        self._slider_refs: dict[str, tuple[QSlider, QLabel]] = {}

        for param, default in fn["params"].items():
            row = QHBoxLayout()
            row.setSpacing(8)

            lbl = QLabel(param)
            lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; min-width: 24px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(lbl)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(-100, 100)
            slider.setValue(int(float(default) * 10))
            slider.setPageStep(1)
            slider.setSingleStep(1)
            slider.setStyleSheet(f"""
                QSlider::groove:horizontal {{ background: #1e293b; height: 4px; border-radius: 2px; }}
                QSlider::sub-page:horizontal {{ background: {CYAN}40; border-radius: 2px; }}
                QSlider::handle:horizontal {{ background: {CYAN}; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; border: none; }}
                QSlider::handle:horizontal:hover {{ background: #00e5ff; }}
            """)
            slider.valueChanged.connect(self._on_slider_changed)
            row.addWidget(slider, 1)

            val_label = QLabel(f"{default:.1f}")
            val_label.setStyleSheet(f"color: {CYAN}; font-size: 11px; min-width: 36px; font-family: 'Fira Code';")
            row.addWidget(val_label)

            self._sliders_layout.addLayout(row)
            self._slider_refs[param] = (slider, val_label)

    def _on_preset_changed(self, index: int):
        fn_key = self._preset_combo.currentData()
        if fn_key == self._current_fn:
            return
        self._current_fn = fn_key
        fn = PRESET_FUNCTIONS[fn_key]
        self._params = dict(fn["params"])
        self._preset_desc.setText(fn["description"])
        self._build_sliders(fn_key)
        self._plot()

    def _on_slider_changed(self):
        for param, (slider, val_label) in self._slider_refs.items():
            val = slider.value() / 10.0
            self._params[param] = val
            val_label.setText(f"{val:.1f}")
        self._plot()

    def _apply_quick_preset(self, fn_key: str, params: dict):
        self._current_fn = fn_key
        # Update combo
        for i in range(self._preset_combo.count()):
            if self._preset_combo.itemData(i) == fn_key:
                self._preset_combo.setCurrentIndex(i)
                break
        self._params = dict(params)
        fn = PRESET_FUNCTIONS[fn_key]
        self._preset_desc.setText(fn["description"])
        self._build_sliders(fn_key)
        # Set slider values
        for param, val in params.items():
            if param in self._slider_refs:
                self._slider_refs[param][0].setValue(int(val * 10))
                self._slider_refs[param][1].setText(f"{val:.1f}")
        self._plot()

    def _plot(self):
        fn_def = PRESET_FUNCTIONS[self._current_fn]
        x = np.linspace(self._x_range[0], self._x_range[1], 400)

        try:
            if fn_def["fn"] is not None:
                y = fn_def["fn"](x, **self._params)
            else:
                # Custom function 'not implemented yet
                y = np.zeros_like(x)
        except Exception:
            y = np.zeros_like(x)

        self._canvas.ax.clear()
        self._canvas.ax.set_facecolor("#0a0e1a")
        for spine in self._canvas.ax.spines.values():
            spine.set_color("#334155")
        self._canvas.ax.tick_params(colors="#94a3b8")
        self._canvas.ax.grid(True, color="#1e293b", linewidth=0.5)

        # Plot
        self._canvas.ax.plot(x, y, color=CYAN, linewidth=2.0, label=fn_def["name"])

        # Axes lines
        self._canvas.ax.axhline(y=0, color="#475569", linewidth=0.8)
        self._canvas.ax.axvline(x=0, color="#475569", linewidth=0.8)

        self._canvas.ax.set_xlim(self._x_range)
        # Auto y-range with some padding
        y_min, y_max = np.nanmin(y), np.nanmax(y)
        pad = max(abs(y_max - y_min) * 0.1, 1.0)
        self._canvas.ax.set_ylim(y_min - pad, y_max + pad)

        self._canvas.ax.legend(loc="upper right", facecolor="#0d1117", edgecolor="#334155",
                               labelcolor="#e2e8f0", fontsize=10)
        self._canvas.draw()

        # Update equation & derivative labels
        self._update_labels(fn_def)

    def _update_labels(self, fn_def: dict):
        # Build equation string
        eq = fn_def.get("eq_template", "y = f(x)")
        try:
            eq = eq.format(**{k: f"{v:.1f}" for k, v in self._params.items()})
        except KeyError:
            pass
        self._eq_label.setText(eq)

        # Derivative
        der = fn_def.get("der_template", "")
        try:
            der = der.format(**{k: f"{v:.1f}" for k, v in self._params.items()})
        except (KeyError, ValueError):
            pass
        self._der_label.setText(der if der else "y' = f'(x)")
