"""Interactive math history timeline with key milestones, era filtering, and detail cards."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QTimer, Signal, QRectF, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient,
    QPainterPath,
)

from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED, AMBER, EMERALD

# ── Era Colors ─────────────────────────────────────────────────
ERA_COLORS = {
    "ancient": "#f59e0b",       # amber
    "classical": "#a855f7",     # purple
    "medieval": "#06b6d4",      # cyan
    "renaissance": "#10b981",   # emerald
    "modern": "#f43f5e",        # rose
    "contemporary": "#3b82f6",  # blue
}

ERA_LABELS = {
    "ancient": "古代 (前3000-500)",
    "classical": "古典 (前500-500)",
    "medieval": "中世纪 (500-1400)",
    "renaissance": "文艺复兴 (1400-1700)",
    "modern": "近代 (1700-1900)",
    "contemporary": "现代 (1900-至今)",
}

# ── History Events ─────────────────────────────────────────────
HISTORY_EVENTS: list[dict] = [
    {"year": "-3000", "era": "ancient", "title": "古埃及数学", "description": "使用十进制计数，解决简单方程，计算金字塔体积", "icon": "🏛️"},
    {"year": "-2000", "era": "ancient", "title": "巴比伦数学", "description": "六十进制，二次方程求解，普林顿322号泥板", "icon": "🧱"},
    {"year": "-500", "era": "classical", "title": "毕达哥拉斯学派", "description": "万物皆数，勾股定理证明，无理数的发现", "icon": "🔺"},
    {"year": "-300", "era": "classical", "title": "欧几里得《几何原本》", "description": "五大公设，465个命题，公理化体系奠基", "icon": "📐"},
    {"year": "-200", "era": "classical", "title": "阿基米德", "description": "浮力定律，π的近似值，穷竭法", "icon": "⚖️"},
    {"year": "628", "era": "medieval", "title": "婆罗摩笈多", "description": "零的运算规则，负数概念，二次方程通解", "icon": "🕉️"},
    {"year": "820", "era": "medieval", "title": "花拉子米《代数学》", "description": "二次方程系统解法，Algebra词源", "icon": "📖"},
    {"year": "1202", "era": "medieval", "title": "斐波那契《算盘书》", "description": "印度-阿拉伯数字传入欧洲，斐波那契数列", "icon": "🐇"},
    {"year": "1637", "era": "renaissance", "title": "笛卡尔《几何学》", "description": "解析几何，笛卡尔坐标系，x²+y²=r²", "icon": "📊"},
    {"year": "1665", "era": "renaissance", "title": "牛顿微积分", "description": "流数法，万有引力，自然哲学的数学原理", "icon": "🍎"},
    {"year": "1687", "era": "renaissance", "title": "莱布尼茨微积分", "description": "积分符号∫，微分符号dx/dy", "icon": "∫"},
    {"year": "1736", "era": "modern", "title": "欧拉", "description": "e^(iπ)+1=0，图论七桥问题，数论突破", "icon": "🌀"},
    {"year": "1822", "era": "modern", "title": "傅里叶分析", "description": "傅里叶级数，热的解析理论", "icon": "🌊"},
    {"year": "1854", "era": "modern", "title": "黎曼几何", "description": "弯曲空间，黎曼猜想，广义相对论基础", "icon": "🌐"},
    {"year": "1874", "era": "modern", "title": "康托尔集合论", "description": "无穷集合，对角线法，连续统假设", "icon": "♾️"},
    {"year": "1931", "era": "contemporary", "title": "哥德尔不完备定理", "description": "任何一致的形式系统存在不可证命题", "icon": "⚡"},
    {"year": "1936", "era": "contemporary", "title": "图灵机", "description": "可计算性理论，停机问题，计算机科学奠基", "icon": "💻"},
    {"year": "1948", "era": "contemporary", "title": "香农信息论", "description": "信息熵，通信的数学理论", "icon": "📡"},
    {"year": "1994", "era": "contemporary", "title": "怀尔斯证明费马大定理", "description": "xⁿ+yⁿ=zⁿ (n>2)无整数解，350年难题", "icon": "🏆"},
    {"year": "2003", "era": "contemporary", "title": "佩雷尔曼证明庞加莱猜想", "description": "三维球面是唯一的单连通紧致三维流形", "icon": "🔮"},
]


class TimelineEventCard(QWidget):
    """Single event card on the timeline."""

    def __init__(self, event: dict, parent=None):
        super().__init__(parent)
        self._event = event
        self._expanded = False
        self._hovered = False
        self.setMinimumHeight(64)
        self.setMaximumHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self._expanded = not self._expanded
        self.setMaximumHeight(180 if self._expanded else 64)
        self.update()
        self.updateGeometry()
        QTimer.singleShot(0, lambda: self.parent().parent().parent().updateGeometry())

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = QRectF(4, 2, w - 8, h - 4)
        era_color = ERA_COLORS.get(self._event["era"], CYAN)

        # Card background
        path = QPainterPath()
        path.addRoundedRect(r, 8, 8)
        bg = QColor(13, 17, 23, 200) if not self._hovered else QColor(17, 28, 48, 220)
        p.fillPath(path, bg)

        # Left era accent
        accent = QRectF(r.x(), r.y() + 8, 3, r.height() - 16)
        p.fillRect(accent, QColor(era_color))

        # Year badge
        year_font = QFont("Orbitron", 12)
        year_font.setBold(True)
        p.setFont(year_font)
        p.setPen(QColor(era_color))
        year = self._event["year"]
        p.drawText(QRectF(r.x() + 16, r.y() + 8, 80, 20), Qt.AlignmentFlag.AlignLeft, year)

        # Icon
        icon_font = QFont("Segoe UI Emoji", 20)
        p.setFont(icon_font)
        p.drawText(QRectF(r.x() + 80, r.y() + 4, 40, 32), Qt.AlignmentFlag.AlignCenter, self._event["icon"])

        # Title
        title_font = QFont("Microsoft YaHei", 14)
        title_font.setBold(True)
        p.setFont(title_font)
        p.setPen(QColor("#e2e8f0"))
        p.drawText(QRectF(r.x() + 130, r.y() + 6, w - 180, 24), Qt.AlignmentFlag.AlignLeft, self._event["title"])

        # Description
        desc_font = QFont("Microsoft YaHei", 10)
        p.setFont(desc_font)
        p.setPen(QColor(TEXT_MUTED))
        desc = self._event["description"]
        if not self._expanded:
            if len(desc) > 60:
                desc = desc[:57] + "..."
        p.drawText(QRectF(r.x() + 130, r.y() + 32, w - 150, 24), Qt.AlignmentFlag.AlignLeft, desc)

        # Expanded: extra info
        if self._expanded:
            p.setPen(QColor(era_color))
            p.setFont(QFont("Microsoft YaHei", 10))
            p.drawText(QRectF(r.x() + 20, r.y() + 62, 120, 18), Qt.AlignmentFlag.AlignLeft, f"时代: {ERA_LABELS.get(self._event['era'], '')}")

            p.setPen(QColor(GREEN))
            p.drawText(QRectF(r.x() + 20, r.y() + 82, w - 40, 18), Qt.AlignmentFlag.AlignLeft, "💡 影响: " + self._event["description"])

        # Border
        pen = QPen(QColor(era_color))
        pen.setWidthF(1.0 if self._hovered else 0.5)
        p.setPen(pen)
        p.drawRoundedRect(r, 8, 8)


class TimelineAxis(QWidget):
    """Vertical timeline axis with era markers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        self._active_era: str | None = None

    def set_active_era(self, era: str | None):
        self._active_era = era
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Vertical line
        pen = QPen(QColor("#334155"))
        pen.setWidthF(2)
        p.setPen(pen)
        x = w - 30
        p.drawLine(x, 20, x, h - 20)

        # Era markers
        eras = list(ERA_LABELS.keys())
        for i, era in enumerate(eras):
            y = 30 + i * (h - 60) / (len(eras) - 1)
            color = ERA_COLORS[era]
            is_active = (self._active_era == era)

            # Dot
            dot_radius = 8 if is_active else 5
            p.setBrush(QBrush(QColor(color)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(x - dot_radius), int(y - dot_radius), int(2 * dot_radius), int(2 * dot_radius))

            # Label
            lbl_font = QFont("Microsoft YaHei", 9 if is_active else 8)
            lbl_font.setBold(is_active)
            p.setFont(lbl_font)
            p.setPen(QColor(color))
            p.drawText(QRectF(4, y - 10, x - 16, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, ERA_LABELS[era].split(" ")[0])


class MathHistoryPage(QWidget):
    """Main math history timeline page."""

    def __init__(self):
        super().__init__()
        self._active_era: str | None = None
        self._init_ui()

    def _init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(0)

        # ── Timeline Axis ──
        self._axis = TimelineAxis()
        root.addWidget(self._axis)

        # ── Right Content ──
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(12, 0, 12, 0)
        right_layout.setSpacing(8)

        # Title
        title = QLabel("📜 数学史时间轴")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {CYAN}; font-family: 'Orbitron','Microsoft YaHei';")
        right_layout.addWidget(title)

        # Era filter buttons
        filter_row = QHBoxLayout()
        filter_row.setSpacing(6)
        all_btn = QPushButton("全部")
        all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        all_btn.setStyleSheet(self._filter_btn_style(not self._active_era))
        all_btn.clicked.connect(lambda: self._set_era_filter(None))
        filter_row.addWidget(all_btn)

        self._filter_buttons: dict[str, QPushButton] = {}
        for era_code, era_label in ERA_LABELS.items():
            short = era_label.split(" ")[0]
            btn = QPushButton(short)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, e=era_code: self._set_era_filter(e))
            filter_row.addWidget(btn)
            self._filter_buttons[era_code] = btn
        self._update_filter_buttons()
        filter_row.addStretch()
        right_layout.addLayout(filter_row)

        # Scroll area with event cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(6)
        self._content_layout.addStretch()
        scroll.setWidget(self._content_widget)
        right_layout.addWidget(scroll, 1)

        self._rebuild_cards()
        root.addWidget(right, 1)

    def _filter_btn_style(self, active: bool) -> str:
        if active:
            return f"QPushButton {{ background: {CYAN}20; border: 1px solid {CYAN}; color: {CYAN}; border-radius: 6px; padding: 5px 14px; font-size: 11px; font-weight: 700; }}"
        return f"QPushButton {{ background: transparent; border: 1px solid {TEXT_MUTED}40; color: {TEXT_MUTED}; border-radius: 6px; padding: 5px 14px; font-size: 11px; }} QPushButton:hover {{ border-color: {CYAN}; color: {CYAN}; }}"

    def _set_era_filter(self, era: str | None):
        self._active_era = era
        self._axis.set_active_era(era)
        self._update_filter_buttons()
        self._rebuild_cards()

    def _update_filter_buttons(self):
        for era_code, btn in self._filter_buttons.items():
            btn.setStyleSheet(self._filter_btn_style(self._active_era == era_code))

    def _rebuild_cards(self):
        # Clear
        while self._content_layout.count() > 1:
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        events = HISTORY_EVENTS
        if self._active_era:
            events = [e for e in events if e["era"] == self._active_era]

        for event in events:
            card = TimelineEventCard(event)
            self._content_layout.insertWidget(self._content_layout.count() - 1, card)
