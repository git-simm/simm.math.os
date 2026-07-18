"""MATH infOS - Dark neon theme stylesheet and color constants."""

# -- Color Palette ----------------------------------------------
BG_DARK = "#0a0e1a"
BG_PANEL = "rgba(13, 17, 23, 0.7)"
CYAN = "#00d4ff"
PURPLE = "#7c3aed"
GREEN = "#00ff88"
ROSE = "#f43f5e"
AMBER = "#f59e0b"
EMERALD = "#10b981"
BLUE = "#3b82f6"
TEXT_PRIMARY = "#e2e8f0"
TEXT_MUTED = "#94a3b8"
BORDER_SUBTLE = "rgba(255, 255, 255, 0.1)"
BORDER_CYAN = "rgba(0, 212, 255, 0.3)"

# -- Global QSS Stylesheet --------------------------------------
STYLESHEET = """
/* -- Base ----------------------------------- */
QMainWindow {
    background-color: #0a0e1a;
}

QWidget {
    color: #e2e8f0;
    font-family: "Inter", "Microsoft YaHei", sans-serif;
    font-size: 13px;
}

/* -- Navigation Bar ------------------------- */
#navbar {
    background: rgba(13, 17, 23, 0.85);
    border-bottom: 1px solid rgba(0, 212, 255, 0.25);
    min-height: 56px;
}

/* -- Navigation Button ---------------------- */
.nav-link {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 13px;
    padding: 8px 16px;
    border-bottom: 2px solid transparent;
    border-radius: 0px;
    font-family: "Microsoft YaHei", sans-serif;
}

.nav-link:hover {
    color: #00d4ff;
}

.nav-link[checked="true"], 
.nav-link[nav-active="true"] {
    color: #00d4ff;
    border-bottom: 2px solid #00d4ff;
}

/* -- Glass Panel ---------------------------- */
#glass-panel, .glass-panel, QFrame#glass-panel {
    background: rgba(13, 17, 23, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
}

/* -- Scroll Areas --------------------------- */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: rgba(148, 163, 184, 0.3);
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 212, 255, 0.5);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* -- Tooltips ------------------------------- */
QToolTip {
    background: #1e293b;
    color: #00d4ff;
    border: 1px solid #00d4ff;
    padding: 4px 8px;
    border-radius: 4px;
}
"""


def apply_style(app: "QApplication") -> None:
    """Apply the MATH?OS dark neon stylesheet to the application."""
    app.setStyleSheet(STYLESHEET)
