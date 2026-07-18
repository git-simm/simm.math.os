"""Physics simulator - enhanced with probability dice, coin flip, normal distribution."""

from __future__ import annotations

import math
import random

import numpy as np

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QFrame, QTabWidget, QSizePolicy,
    QGroupBox, QSpinBox,
)
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QPainterPath,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED, AMBER


# ═══════════════════════════════════════════════════════════════
# Probability Dice Simulator
# ═══════════════════════════════════════════════════════════════
class DiceSimulator(QWidget):
    """Roll dice, count frequencies, show histogram."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rolls: list[int] = []
        self._running = False
        self._dice_count = 2
        self._sides = 6

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Controls
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        self._count_spin = QSpinBox()
        self._count_spin.setRange(1, 5)
        self._count_spin.setValue(2)
        self._count_spin.setPrefix("骰子数: ")
        self._count_spin.valueChanged.connect(lambda v: setattr(self, "_dice_count", v))
        self._count_spin.setStyleSheet(f"color: {CYAN}; background: #0a0e1a; border: 1px solid {CYAN}40; border-radius: 4px;")
        ctrl_row.addWidget(self._count_spin)

        roll_once = QPushButton("🎲 单次投掷")
        roll_once.setCursor(Qt.CursorShape.PointingHandCursor)
        roll_once.clicked.connect(self._roll_once)
        roll_once.setStyleSheet(f"QPushButton {{ background: {PURPLE}20; border: 1px solid {PURPLE}50; color: {PURPLE}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {PURPLE}; }}")
        ctrl_row.addWidget(roll_once)

        self._auto_btn = QPushButton("▶ 自动投掷")
        self._auto_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._auto_btn.clicked.connect(self._toggle_auto)
        self._auto_btn.setStyleSheet(f"QPushButton {{ background: {GREEN}20; border: 1px solid {GREEN}50; color: {GREEN}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {GREEN}; }}")
        ctrl_row.addWidget(self._auto_btn)

        reset_btn = QPushButton("🔄 清零")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._reset)
        reset_btn.setStyleSheet(f"QPushButton {{ background: transparent; border: 1px solid {TEXT_MUTED}40; color: {TEXT_MUTED}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {ROSE}; color: {ROSE}; }}")
        ctrl_row.addWidget(reset_btn)

        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)

        # Result display
        self._result_label = QLabel("🎯 结果: --")
        self._result_label.setStyleSheet(f"font-size: 16px; color: {AMBER}; font-family: 'Fira Code';")
        self._result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result_label)

        # Stats
        self._stats_label = QLabel("📊 均值: -- | 标准差: -- | 样本数: 0")
        self._stats_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        self._stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._stats_label)

        # Matplotlib histogram
        self._fig = Figure(figsize=(6, 3), dpi=90, facecolor="#0a0e1a")
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor("#0a0e1a")
        self._canvas = FigureCanvasQTAgg(self._fig)
        layout.addWidget(self._canvas, 1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._roll_once)
        self._plot()

    def _roll_once(self):
        total = sum(random.randint(1, self._sides) for _ in range(self._dice_count))
        self._rolls.append(total)
        self._result_label.setText(f"🎯 结果: {total}")
        self._update_stats()
        self._plot()

    def _toggle_auto(self):
        self._running = not self._running
        if self._running:
            self._auto_btn.setText("⏸ 停止")
            self._timer.start(100)
        else:
            self._auto_btn.setText("▶ 自动投掷")
            self._timer.stop()

    def _reset(self):
        self._rolls.clear()
        self._result_label.setText("🎯 结果: --")
        self._update_stats()
        self._plot()

    def _update_stats(self):
        if not self._rolls:
            self._stats_label.setText("📊 均值: -- | 标准差: -- | 样本数: 0")
            return
        arr = np.array(self._rolls)
        mean_val = np.mean(arr)
        std_val = np.std(arr, ddof=1) if len(arr) > 1 else 0
        self._stats_label.setText(f"📊 均值: {mean_val:.2f} | 标准差: {std_val:.2f} | 样本数: {len(arr)}")

    def _plot(self):
        self._ax.clear()
        self._ax.set_facecolor("#0a0e1a")
        for spine in self._ax.spines.values():
            spine.set_color("#334155")
        self._ax.tick_params(colors="#94a3b8")

        if self._rolls:
            min_val = self._dice_count
            max_val = self._dice_count * self._sides
            bins = list(range(min_val, max_val + 2))
            self._ax.hist(self._rolls, bins=bins, color=CYAN, alpha=0.7, edgecolor="#0a0e1a", linewidth=0.5)
            self._ax.set_xlim(min_val - 0.5, max_val + 0.5)
        else:
            self._ax.text(0.5, 0.5, "点击 单次投掷 开始", ha="center", va="center",
                          color=TEXT_MUTED, fontsize=14, transform=self._ax.transAxes)

        self._ax.set_xlabel("点数之和", color=TEXT_MUTED)
        self._ax.set_ylabel("频次", color=TEXT_MUTED)
        self._canvas.draw()


# ═══════════════════════════════════════════════════════════════
# Coin Flip (Binomial Distribution)
# ═══════════════════════════════════════════════════════════════
class CoinFlipWidget(QWidget):
    """Simulate coin flips, visualize binomial distribution converging to normal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._heads_count = 0
        self._total_flips = 0
        self._history: list[float] = []  # running proportion of heads

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        flip_once = QPushButton("🪙 单次抛掷")
        flip_once.setCursor(Qt.CursorShape.PointingHandCursor)
        flip_once.clicked.connect(lambda: self._flip(1))
        flip_once.setStyleSheet(f"QPushButton {{ background: {AMBER}20; border: 1px solid {AMBER}50; color: {AMBER}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {AMBER}; }}")
        ctrl_row.addWidget(flip_once)

        flip_many = QPushButton("🎰 抛100次")
        flip_many.setCursor(Qt.CursorShape.PointingHandCursor)
        flip_many.clicked.connect(lambda: self._flip(100))
        flip_many.setStyleSheet(f"QPushButton {{ background: {AMBER}20; border: 1px solid {AMBER}50; color: {AMBER}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {AMBER}; }}")
        ctrl_row.addWidget(flip_many)

        self._auto_btn = QPushButton("▶ 自动")
        self._auto_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._auto_btn.clicked.connect(self._toggle_auto)
        self._auto_btn.setStyleSheet(f"QPushButton {{ background: {GREEN}20; border: 1px solid {GREEN}50; color: {GREEN}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {GREEN}; }}")
        ctrl_row.addWidget(self._auto_btn)

        reset_btn = QPushButton("🔄 清零")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._reset)
        reset_btn.setStyleSheet(f"QPushButton {{ background: transparent; border: 1px solid {TEXT_MUTED}40; color: {TEXT_MUTED}; border-radius: 6px; padding: 6px 14px; }} QPushButton:hover {{ border-color: {ROSE}; color: {ROSE}; }}")
        ctrl_row.addWidget(reset_btn)

        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)

        # Results
        self._result_label = QLabel("🪙 正面: 0 | 反面: 0 | 正面比例: 0%")
        self._result_label.setStyleSheet(f"font-size: 14px; color: {AMBER}; font-family: 'Fira Code';")
        self._result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result_label)

        # LLN note
        note = QLabel("💡 大数定律: 投掷次数越多，正面比例趋近50%")
        note.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note)

        # Plot
        self._fig = Figure(figsize=(6, 3), dpi=90, facecolor="#0a0e1a")
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor("#0a0e1a")
        self._canvas = FigureCanvasQTAgg(self._fig)
        layout.addWidget(self._canvas, 1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(lambda: self._flip(1))
        self._plot()

    def _flip(self, n: int):
        heads = sum(1 for _ in range(n) if random.random() < 0.5)
        self._heads_count += heads
        self._total_flips += n
        if self._total_flips > 0:
            self._history.append(self._heads_count / self._total_flips)
        else:
            self._history.append(0.5)
        self._result_label.setText(
            f"🪙 正面: {self._heads_count} | 反面: {self._total_flips - self._heads_count} | 正面比例: {self._heads_count/max(1, self._total_flips)*100:.1f}%"
        )
        self._plot()

    def _toggle_auto(self):
        if self._timer.isActive():
            self._timer.stop()
            self._auto_btn.setText("▶ 自动")
        else:
            self._timer.start(150)
            self._auto_btn.setText("⏸ 停止")

    def _reset(self):
        self._heads_count = 0
        self._total_flips = 0
        self._history.clear()
        self._result_label.setText("🪙 正面: 0 | 反面: 0 | 正面比例: 0%")
        self._plot()

    def _plot(self):
        self._ax.clear()
        self._ax.set_facecolor("#0a0e1a")
        for spine in self._ax.spines.values():
            spine.set_color("#334155")
        self._ax.tick_params(colors="#94a3b8")

        if self._history:
            self._ax.plot(range(len(self._history)), self._history, color=AMBER, linewidth=1.5)
            self._ax.axhline(y=0.5, color=ROSE, linestyle="--", linewidth=1, alpha=0.6)
        else:
            self._ax.text(0.5, 0.5, "点击 单次抛掷 开始", ha="center", va="center",
                          color=TEXT_MUTED, fontsize=14, transform=self._ax.transAxes)

        self._ax.set_ylim(0, 1)
        self._ax.set_xlabel("抛掷次数", color=TEXT_MUTED)
        self._ax.set_ylabel("正面比例", color=TEXT_MUTED)
        self._ax.set_title("大数定律: 比例收敛于0.5", color=AMBER, fontsize=11)
        self._canvas.draw()


# ═══════════════════════════════════════════════════════════════
# Normal Distribution Explorer
# ═══════════════════════════════════════════════════════════════
class NormalDistributionWidget(QWidget):
    """Explore normal distribution with adjustable mu and sigma."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mu = 0.0
        self._sigma = 1.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Sliders
        slider_row = QHBoxLayout()
        slider_row.setSpacing(16)

        # Mu slider
        mu_layout = QVBoxLayout()
        mu_label = QLabel(f"μ (均值): {self._mu:.1f}")
        mu_label.setStyleSheet(f"color: {CYAN}; font-size: 12px;")
        mu_layout.addWidget(mu_label)
        mu_slider = QSlider(Qt.Orientation.Horizontal)
        mu_slider.setRange(-50, 50)
        mu_slider.setValue(0)
        mu_slider.setPageStep(1)
        mu_slider.setSingleStep(1)
        mu_slider.valueChanged.connect(lambda v, l=mu_label: self._update_params(v / 10, self._sigma, l, "mu"))
        mu_slider.setStyleSheet(f"QSlider::groove:horizontal {{ background: #1e293b; height: 4px; }} QSlider::sub-page:horizontal {{ background: {CYAN}40; }} QSlider::handle:horizontal {{ background: {CYAN}; width: 12px; border-radius: 6px; border: none; }}")
        mu_layout.addWidget(mu_slider)
        slider_row.addLayout(mu_layout)

        # Sigma slider
        sig_layout = QVBoxLayout()
        sig_label = QLabel(f"σ (标准差): {self._sigma:.1f}")
        sig_label.setStyleSheet(f"color: {PURPLE}; font-size: 12px;")
        sig_layout.addWidget(sig_label)
        sig_slider = QSlider(Qt.Orientation.Horizontal)
        sig_slider.setRange(1, 50)
        sig_slider.setValue(10)
        sig_slider.setPageStep(1)
        sig_slider.setSingleStep(1)
        sig_slider.valueChanged.connect(lambda v, l=sig_label: self._update_params(self._mu, v / 10, l, "sigma"))
        sig_slider.setStyleSheet(f"QSlider::groove:horizontal {{ background: #1e293b; height: 4px; }} QSlider::sub-page:horizontal {{ background: {PURPLE}40; }} QSlider::handle:horizontal {{ background: {PURPLE}; width: 12px; border-radius: 6px; border: none; }}")
        sig_layout.addWidget(sig_slider)
        slider_row.addLayout(sig_layout)

        layout.addLayout(slider_row)

        # 68-95-99.7 rule
        rule = QLabel("📏 经验法则: μ±1σ = 68.3% | μ±2σ = 95.4% | μ±3σ = 99.7%")
        rule.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px;")
        rule.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rule)

        # Plot
        self._fig = Figure(figsize=(6, 3.5), dpi=90, facecolor="#0a0e1a")
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor("#0a0e1a")
        self._canvas = FigureCanvasQTAgg(self._fig)
        layout.addWidget(self._canvas, 1)

        self._plot()

        # Store refs
        self._mu_slider = mu_slider
        self._sigma_slider = sig_slider
        self._mu_label = mu_label
        self._sigma_label = sig_label

    def _update_params(self, mu: float, sigma: float, label: QLabel, which: str):
        if which == "mu":
            self._mu = mu
            label.setText(f"μ (均值): {mu:.1f}")
        else:
            self._sigma = sigma
            label.setText(f"σ (标准差): {sigma:.1f}")
        self._plot()

    def _plot(self):
        self._ax.clear()
        self._ax.set_facecolor("#0a0e1a")
        for spine in self._ax.spines.values():
            spine.set_color("#334155")
        self._ax.tick_params(colors="#94a3b8")

        x = np.linspace(self._mu - 4 * self._sigma, self._mu + 4 * self._sigma, 300)
        y = (1 / (self._sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - self._mu) / self._sigma) ** 2)

        self._ax.fill_between(x, y, alpha=0.2, color=CYAN)
        self._ax.plot(x, y, color=CYAN, linewidth=2)

        # Mark ±1σ, ±2σ
        for k, color in [(1, GREEN), (2, AMBER)]:
            self._ax.axvline(x=self._mu - k * self._sigma, color=color, linestyle="--", linewidth=0.8, alpha=0.5)
            self._ax.axvline(x=self._mu + k * self._sigma, color=color, linestyle="--", linewidth=0.8, alpha=0.5)

        self._ax.axvline(x=self._mu, color=ROSE, linestyle=":", linewidth=1)
        self._ax.set_xlabel("x", color=TEXT_MUTED)
        self._ax.set_ylabel("概率密度", color=TEXT_MUTED)
        self._ax.set_title(f"正态分布 N({self._mu:.1f}, {self._sigma:.1f}²)", color=CYAN, fontsize=13)
        self._canvas.draw()


# ═══════════════════════════════════════════════════════════════
# Main Physics Simulator Page (wrap existing + add probability)
# ═══════════════════════════════════════════════════════════════
class PhysicsSimulatorPage(QWidget):
    """Main physics + probability simulator page."""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        title = QLabel("⚛️ 物理模拟 & 概率实验")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {CYAN}; font-family: 'Orbitron','Microsoft YaHei';")
        root.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{ background: transparent; border: none; }}
            QTabBar::tab {{ color: {TEXT_MUTED}; padding: 8px 18px; border-bottom: 2px solid transparent; }}
            QTabBar::tab:selected {{ color: {CYAN}; border-bottom: 2px solid {CYAN}; }}
            QTabBar::tab:hover:!selected {{ color: {GREEN}; }}
        """)

        tabs.addTab(NormalDistributionWidget(), "📊 正态分布")
        tabs.addTab(CoinFlipWidget(), "🪙 硬币实验")
        tabs.addTab(DiceSimulator(), "🎲 骰子实验")

        root.addWidget(tabs, 1)
