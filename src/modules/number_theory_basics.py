"""Number theory basics module - pyramid-style knowledge cards with search and navigation."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QFrame,
    QSizePolicy, QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient,
    QRadialGradient, QPainterPath, QMouseEvent,
)

from knowledge_base import (
    KNOWLEDGE_NODES, PYRAMID_LEVELS, SEARCH_INDEX, HELP_TEXT,
)
from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED

# ── Color mapping for pyramid levels ───────────────────────────
LEVEL_COLORS = {
    1: "#06b6d4",  # cyan
    2: "#a855f7",  # purple
    3: "#f59e0b",  # amber
    4: "#94a3b8",  # slate
}


class PyramidLevelHeader(QWidget):
    """Clickable pyramid tier header that expands/collapses child nodes."""

    clicked = Signal(int)

    def __init__(self, level: int, name: str, description: str, parent=None):
        super().__init__(parent)
        self._level = level
        self._expanded = True
        self._hovered = False
        self.setFixedHeight(56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._level_name = name
        self._level_descr = description

    def mousePressEvent(self, event: QMouseEvent):
        self._expanded = not self._expanded
        self.clicked.emit(self._level)
        self.update()

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
        r = QRectF(4, 4, w - 8, h - 8)
        color = LEVEL_COLORS.get(self._level, CYAN)

        # Background
        path = QPainterPath()
        path.addRoundedRect(r, 12, 12)
        bg = QColor("#0d1523") if not self._hovered else QColor("#111d33")
        p.fillPath(path, bg)

        # Left accent bar
        accent = QRectF(r.x(), r.y() + 10, 4, r.height() - 20)
        p.fillRect(accent, QColor(color))

        # Level number circle
        cx, cy = r.x() + 30, r.center().y()
        p.setBrush(QBrush(QColor(color)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(int(cx - 12), int(cy - 12), 24, 24)

        # Level number text
        num_font = QFont("Orbitron", 11)
        num_font.setBold(True)
        p.setFont(num_font)
        p.setPen(QColor("#0a0e1a"))
        p.drawText(QRectF(cx - 12, cy - 12, 24, 24), Qt.AlignmentFlag.AlignCenter, str(self._level))

        # Title
        title_font = QFont("Microsoft YaHei", 14)
        title_font.setBold(True)
        p.setFont(title_font)
        p.setPen(QColor(color))
        p.drawText(QRectF(r.x() + 52, r.y() + 8, 200, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._level_name)

        # Description
        desc_font = QFont("Microsoft YaHei", 10)
        p.setFont(desc_font)
        p.setPen(QColor(TEXT_MUTED))
        p.drawText(QRectF(r.x() + 52, r.y() + 28, 400, 18), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._level_descr)

        # Expand/collapse indicator
        arrow_font = QFont("Segoe UI", 12)
        p.setFont(arrow_font)
        p.setPen(QColor(color))
        arrow = "v" if self._expanded else ">"
        p.drawText(QRectF(r.right() - 36, r.y(), 32, r.height()), Qt.AlignmentFlag.AlignCenter, arrow)

        # Border
        pen = QPen(QColor(color))
        pen.setWidthF(1.0)
        p.setPen(pen)
        p.drawRoundedRect(r, 12, 12)


class KnowledgeCard(QWidget):
    """Single knowledge card with glass effect, icon, definition, principles, and examples."""

    clicked_card = Signal(str)

    def __init__(self, node: dict, parent=None):
        super().__init__(parent)
        self._node = node
        self._hovered = False
        self._expanded = False
        self.setMinimumHeight(80)
        self.setMaximumHeight(80 if not self._expanded else 400)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent):
        self._expanded = not self._expanded
        self.setMaximumHeight(80 if not self._expanded else 400)
        self.update()
        self.updateGeometry()
        QTimer.singleShot(0, self.parent().parent().parent().adjustSize)

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
        color = self._node.get("color", CYAN)

        # Glass panel background
        path = QPainterPath()
        path.addRoundedRect(r, 10, 10)
        bg = QColor(13, 17, 23, 200) if not self._hovered else QColor(17, 28, 48, 220)
        p.fillPath(path, bg)

        # Colored top accent line
        accent = QRectF(r.x() + 10, r.y(), r.width() - 20, 3)
        p.fillRect(accent, QColor(color))

        # Icon
        icon_font = QFont("Segoe UI Emoji", 18)
        p.setFont(icon_font)
        p.setPen(QColor(color))
        icon = self._node.get("icon", "")
        p.drawText(QRectF(r.x() + 14, r.y() + 12, 36, 32), Qt.AlignmentFlag.AlignCenter, icon)

        # Title
        title_font = QFont("Microsoft YaHei", 13)
        title_font.setBold(True)
        p.setFont(title_font)
        p.setPen(QColor("#e2e8f0"))
        title = self._node.get("title", "")
        p.drawText(QRectF(r.x() + 56, r.y() + 12, w - 120, 22), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, title)

        # Category badge
        cat_font = QFont("Microsoft YaHei", 9)
        p.setFont(cat_font)
        cat = self._node.get("category", "")
        cat_w = len(cat) * 13 + 16
        cat_r = QRectF(r.right() - cat_w - 10, r.y() + 14, cat_w, 18)
        cat_path = QPainterPath()
        cat_path.addRoundedRect(cat_r, 5, 5)
        p.fillPath(cat_path, QColor(color).darker(300))
        p.setPen(QColor(color))
        p.drawText(cat_r, Qt.AlignmentFlag.AlignCenter, cat)

        # Definition (shown always)
        if not self._expanded:
            def_font = QFont("Microsoft YaHei", 10)
            p.setFont(def_font)
            p.setPen(QColor(TEXT_MUTED))
            definition = self._node.get("definition", "")
            # Truncate if too long
            if len(definition) > 80:
                definition = definition[:77] + "..."
            p.drawText(QRectF(r.x() + 56, r.y() + 38, w - 120, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, definition)

        # Expanded content
        if self._expanded:
            y_off = 70
            # Full definition
            def_font = QFont("Microsoft YaHei", 10)
            p.setFont(def_font)
            p.setPen(QColor(TEXT_MUTED))
            definition = self._node.get("definition", "")
            p.drawText(QRectF(r.x() + 20, r.y() + y_off, w - 40, 24), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "馃搵 " + definition)
            y_off += 30

            # Principles
            principles = self._node.get("principles", [])
            if principles:
                p.setPen(QColor(color))
                p.drawText(QRectF(r.x() + 20, r.y() + y_off, 100, 20), Qt.AlignmentFlag.AlignLeft, "馃洜 閫氬垯:")
                y_off += 22
                p.setFont(QFont("Microsoft YaHei", 9))
                for pr in principles:
                    p.setPen(QColor("#cbd5e1"))
                    p.drawText(QRectF(r.x() + 32, r.y() + y_off, w - 52, 18), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "鈥? " + pr)
                    y_off += 18

            # Examples
            examples = self._node.get("examples", [])
            if examples:
                y_off += 8
                p.setFont(QFont("Microsoft YaHei", 10))
                p.setPen(QColor(color))
                p.drawText(QRectF(r.x() + 20, r.y() + y_off, 100, 20), Qt.AlignmentFlag.AlignLeft, "馃搵 渚嬪瓙:")
                y_off += 22
                for ex in examples:
                    p.setFont(QFont("Fira Code", 9))
                    p.setPen(QColor("#10b981"))
                    p.drawText(QRectF(r.x() + 32, r.y() + y_off, w - 52, 18), Qt.AlignmentFlag.AlignLeft, "鈥? " + ex["title"])
                    y_off += 16
                    p.setFont(QFont("Microsoft YaHei", 9))
                    p.setPen(QColor("#94a3b8"))
                    p.drawText(QRectF(r.x() + 44, r.y() + y_off, w - 64, 18), Qt.AlignmentFlag.AlignLeft, ex["content"])
                    y_off += 18

            # Links to related topics
            links = self._node.get("links_to", [])
            if links:
                y_off += 8
                p.setFont(QFont("Microsoft YaHei", 9))
                p.setPen(QColor("#64748b"))
                p.drawText(QRectF(r.x() + 20, r.y() + y_off, w - 40, 20), Qt.AlignmentFlag.AlignLeft, "馃攧 鍏宠仈: " + ", ".join(links))

            # Update height
            needed = int(y_off + 30)
            if self.maximumHeight() != needed:
                self.setMaximumHeight(needed)

        # Border
        pen = QPen(QColor(color))
        pen.setWidthF(1.0 if self._hovered else 0.5)
        p.setPen(pen)
        p.drawRoundedRect(r, 10, 10)


class NumberTheoryBasicsPage(QWidget):
    """Full page: search bar + pyramid levels + knowledge cards."""

    def __init__(self):
        super().__init__()
        self._search_text = ""
        self._filtered_nodes: list[dict] = list(KNOWLEDGE_NODES)
        self._expanded_levels: set[int] = {1, 2, 3, 4}
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # ── Title ──
        title = QLabel("Number Systems and Algebra Foundation - Knowledge Pyramid")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {CYAN}; font-family: 'Orbitron','Microsoft YaHei';")
        root.addWidget(title)

        # ── Search Bar ──
        search_panel = QFrame()
        search_panel.setObjectName("glass-panel")
        search_layout = QHBoxLayout(search_panel)
        search_layout.setContentsMargins(16, 10, 16, 10)

        search_icon = QLabel("馃攳")
        search_icon.setStyleSheet("font-size: 18px;")
        search_layout.addWidget(search_icon)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("鎼滅储鐭ヨ瘑鍗＄墖... 渚嬪: 鏈夌悊鏁般€丼姹傛牴鍏紡銆乮虏=-1銆佸垽鍒紡...")
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {CYAN};
                font-size: 14px;
                padding: 6px;
            }}
        """)
        search_layout.addWidget(self._search_input, 1)

        clear_btn = QPushButton("娓呴櫎")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_search)
        clear_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: 1px solid {TEXT_MUTED}; color: {TEXT_MUTED}; border-radius: 6px; padding: 6px 16px; }}
            QPushButton:hover {{ border-color: {CYAN}; color: {CYAN}; }}
        """)
        search_layout.addWidget(clear_btn)

        root.addWidget(search_panel)

        # ── Results count ──
        self._results_label = QLabel(f"鏄剧ず {len(self._filtered_nodes)} 寮犵煡璇嗗崱鐗?")
        self._results_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        root.addWidget(self._results_label)

        # ── Scroll Area ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(10)
        self._content_layout.addStretch()
        scroll.setWidget(self._content_widget)
        root.addWidget(scroll, 1)

        self._rebuild_cards()

    def _on_search(self, text: str):
        self._search_text = text.strip().lower()
        if not self._search_text:
            self._filtered_nodes = list(KNOWLEDGE_NODES)
        else:
            # Search in SEARCH_INDEX
            matched_ids: set[str] = set()
            for entry in SEARCH_INDEX:
                if self._search_text in entry["query"]:
                    matched_ids.add(entry["node_id"])
            self._filtered_nodes = [n for n in KNOWLEDGE_NODES if n["id"] in matched_ids]

        self._rebuild_cards()

    def _clear_search(self):
        self._search_input.clear()
        self._on_search("")

    def _rebuild_cards(self):
        # Clear existing items (except stretch)
        while self._content_layout.count() > 1:
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._results_label.setText(f"鏄剧ず {len(self._filtered_nodes)} 寮犵煡璇嗗崱鐗? | 鎼滅储: {self._search_text or '鍏ㄩ儴'}")

        # Group by level
        grouped: dict[int, list[dict]] = {}
        for node in self._filtered_nodes:
            lvl = node["level"]
            grouped.setdefault(lvl, []).append(node)

        for level in sorted(grouped.keys()):
            lvl_info = PYRAMID_LEVELS.get(level, {"name": f"Level {level}", "descr": ""})
            header = PyramidLevelHeader(level, lvl_info["name"], lvl_info["descr"])
            header.clicked.connect(self._on_level_toggle)
            self._content_layout.insertWidget(self._content_layout.count() - 1, header)

            if level in self._expanded_levels:
                for node in grouped[level]:
                    card = KnowledgeCard(node)
                    self._content_layout.insertWidget(self._content_layout.count() - 1, card)

    def _on_level_toggle(self, level: int):
        if level in self._expanded_levels:
            self._expanded_levels.discard(level)
        else:
            self._expanded_levels.add(level)
        self._rebuild_cards()


