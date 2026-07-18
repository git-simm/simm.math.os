"""Custom force-directed graph widget using QPainter - no WebEngine dependency."""

from __future__ import annotations

import math
import random
from typing import Any

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF, Signal, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QRadialGradient,
    QPainterPath, QMouseEvent, QWheelEvent,
)

from style import BG_DARK, CYAN, PURPLE, GREEN, ROSE, TEXT_MUTED, AMBER, EMERALD

# ── Category colors ────────────────────────────────────────────
CAT_COLORS: dict[str, str] = {
    "代数": "#a855f7",
    "几何": "#10b981",
    "分析": "#f43f5e",
    "概率": "#f59e0b",
    "数论": "#06b6d4",
    "线性代数": "#3b82f6",
}

# ── Node data ──────────────────────────────────────────────────
_NODES: list[dict[str, Any]] = [
    {"id": "center", "name": "数学", "icon": "∞", "category": None, "size": 80, "fx": 0.5, "fy": 0.5},
    {"id": "algebra", "name": "代数", "icon": "x", "category": "代数", "size": 65, "fx": 0.22, "fy": 0.25},
    {"id": "geometry", "name": "几何", "icon": "△", "category": "几何", "size": 65, "fx": 0.78, "fy": 0.25},
    {"id": "analysis", "name": "微积分", "icon": "∫", "category": "分析", "size": 65, "fx": 0.33, "fy": 0.75},
    {"id": "probability", "name": "概率论", "icon": "🎲", "category": "概率", "size": 65, "fx": 0.67, "fy": 0.75},
    {"id": "linear_algebra", "name": "线性代数", "icon": "M", "category": "线性代数", "size": 55, "fx": 0.90, "fy": 0.50},
    {"id": "num_theory", "name": "数论", "icon": "ℕ", "category": "数论", "size": 55, "fx": 0.10, "fy": 0.50},
]

_EDGES: list[tuple[str, str]] = [
    ("center", "algebra"), ("center", "geometry"), ("center", "analysis"),
    ("center", "probability"), ("center", "linear_algebra"), ("center", "num_theory"),
    ("algebra", "linear_algebra"), ("algebra", "num_theory"),
    ("analysis", "geometry"), ("analysis", "probability"),
]


class ForceGraphWidget(QWidget):
    """Interactive force-directed knowledge graph with QPainter."""

    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 400)
        self.setMouseTracking(True)

        # Node positions (relative 0..1)
        self._positions: dict[str, list[float]] = {}
        for n in _NODES:
            self._positions[n["id"]] = [n.get("fx", 0.5), n.get("fy", 0.5)]

        # Animation
        self._angle = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(50)

        # Interaction
        self._hovered_node: str | None = None
        self._dragging_node: str | None = None
        self._drag_offset = QPointF(0, 0)

    def _animate(self):
        self._angle += 0.005
        # Gentle orbital motion for satellite nodes
        center_x, center_y = self._positions["center"]
        for node in _NODES:
            nid = node["id"]
            if nid == "center":
                continue
            fx, fy = node.get("fx", 0.5), node.get("fy", 0.5)
            # Apply subtle oscillation
            ox = fx + 0.01 * math.sin(self._angle * 3 + hash(nid) % 100 * 0.1)
            oy = fy + 0.01 * math.cos(self._angle * 3 + hash(nid) % 100 * 0.1)
            self._positions[nid] = [ox, oy]
        self.update()

    def _node_at(self, pos: QPointF) -> str | None:
        """Return node ID under the given widget position."""
        w, h = self.width(), self.height()
        for node in _NODES:
            nx, ny = self._positions[node["id"]]
            px, py = nx * w, ny * h
            size = node["size"] / 2 + 10
            dx = pos.x() - px
            dy = pos.y() - py
            if dx * dx + dy * dy <= size * size:
                return node["id"]
        return None

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging_node:
            w, h = self.width(), self.height()
            self._positions[self._dragging_node] = [
                event.position().x() / w,
                event.position().y() / h,
            ]
            self.update()
            return

        prev = self._hovered_node
        self._hovered_node = self._node_at(event.position())
        if prev != self._hovered_node:
            self.setCursor(Qt.CursorShape.PointingHandCursor if self._hovered_node else Qt.CursorShape.ArrowCursor)
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        node = self._node_at(event.position())
        if node:
            self._dragging_node = node
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._dragging_node:
            node = self._dragging_node
            self._dragging_node = None
            # Check if it was a click (not a drag)
            clicked = self._node_at(event.position())
            if clicked == node:
                self.node_clicked.emit(node)
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        # Zoom could be added here
        pass

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # ── Edges ──
        for src, dst in _EDGES:
            sx, sy = self._positions[src]
            dx, dy = self._positions[dst]
            x1, y1 = sx * w, sy * h
            x2, y2 = dx * w, dy * h

            # Gradient color based on source category
            src_cat = next((n["category"] for n in _NODES if n["id"] == src), None)
            color = QColor(CAT_COLORS.get(src_cat, CYAN))
            color.setAlphaF(0.35)

            pen = QPen(color)
            pen.setWidthF(1.5)
            p.setPen(pen)
            p.drawLine(int(x1), int(y1), int(x2), int(y2))

        # ── Nodes ──
        for node in _NODES:
            nid = node["id"]
            nx, ny = self._positions[nid]
            px, py = nx * w, ny * h
            cat = node["category"]
            color_str = CAT_COLORS.get(cat, CYAN) if cat else CYAN
            color = QColor(color_str)
            radius = node["size"] / 2

            is_hovered = (self._hovered_node == nid)
            is_dragging = (self._dragging_node == nid)

            # Glow effect on hover
            if is_hovered or is_dragging:
                glow = QRadialGradient(px, py, radius + 15)
                glow.setColorAt(0, QColor(color).lighter(160))
                glow.setColorAt(1, QColor(0, 0, 0, 0))
                p.setBrush(QBrush(glow))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(int(px - radius - 15), int(py - radius - 15),
                              int(2 * radius + 30), int(2 * radius + 30))

            # Circle background
            bg = QColor(13, 17, 23, 220)
            p.setBrush(QBrush(bg))
            pen = QPen(color)
            pen.setWidthF(2.5 if is_hovered else 1.5)
            p.setPen(pen)
            p.drawEllipse(int(px - radius), int(py - radius), int(2 * radius), int(2 * radius))

            # Icon
            icon = node.get("icon", "")
            icon_font = QFont("Segoe UI Emoji", int(radius * 0.6))
            p.setFont(icon_font)
            p.setPen(color)
            p.drawText(QRectF(px - radius, py - radius * 0.6, 2 * radius, radius * 1.5),
                       Qt.AlignmentFlag.AlignCenter, icon)

            # Name
            name_font = QFont("Microsoft YaHei", 10 if nid == "center" else 9)
            name_font.setBold(True)
            p.setFont(name_font)
            p.setPen(QColor("#e2e8f0"))
            p.drawText(QRectF(px - radius - 20, py + radius * 0.3, 2 * radius + 40, 20),
                       Qt.AlignmentFlag.AlignCenter, node["name"])

        # ── Center pulse ──
        cx, cy = self._positions["center"]
        cpx, cpy = cx * w, cy * h
        pulse_r = 90 + 8 * math.sin(self._angle * 2)
        pulse = QPen(QColor(CYAN))
        pulse.setWidthF(1.0)
        pulse.setColor(QColor(CYAN).darker(200))
        p.setPen(pulse)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(int(cpx - pulse_r), int(cpy - pulse_r), int(2 * pulse_r), int(2 * pulse_r))
