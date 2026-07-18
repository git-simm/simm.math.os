"""Particle background canvas widget - animated starfield effect."""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QPointF, Qt
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
import random
import math


class Particle:
    def __init__(self, w, h):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.size = random.uniform(1.0, 3.0)
        self.speed = random.uniform(0.2, 1.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.opacity = random.uniform(0.3, 0.9)
        self.speed_x = math.cos(self.angle) * self.speed
        self.speed_y = math.sin(self.angle) * self.speed


class ParticleCanvas(QWidget):
    """Animated particle background that fills the parent widget."""

    def __init__(self, parent=None, particle_count=80):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._particles = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.setInterval(33)  # ~30 fps
        self._count = particle_count

    def showEvent(self, event):
        super().showEvent(event)
        self._particles = [
            Particle(self.width(), self.height())
            for _ in range(self._count)
        ]
        self._timer.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._particles = [
            Particle(self.width(), self.height())
            for _ in range(self._count)
        ]

    def _tick(self):
        w, h = self.width(), self.height()
        for p in self._particles:
            p.x += p.speed_x
            p.y += p.speed_y
            # Reset particle that goes off screen; blink opacity
            if p.x < 0 or p.x > w:
                p.speed_x = -p.speed_x
                p.x = max(0, min(p.x, w))
            if p.y < 0 or p.y > h:
                p.speed_y = -p.speed_y
                p.y = max(0, min(p.y, h))
            # Subtle opacity drift
            p.opacity += random.uniform(-0.02, 0.02)
            p.opacity = max(0.2, min(1.0, p.opacity))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for p in self._particles:
            alpha = int(255 * p.opacity)
            color = QColor(0, 212, 255, alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(p.x, p.y), p.size, p.size)
        painter.end()
