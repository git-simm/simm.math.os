"""Application entry point - launches the MATH路OS desktop application."""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Ensure src/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import MainWindow
from style import apply_style


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MATH路OS")
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    apply_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
