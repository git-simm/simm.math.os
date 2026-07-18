# MATH路OS - Python Desktop Math Learning System

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py
```

## Project Structure

```
simm.math.os/
├── openspec/              # OpenSpec requirements management
│   ├── specs/             # Current specifications
│   ├── proposals/         # Feature proposals
│   └── archive/           # Completed specs
├── src/
│   ├── main.py            # Application entry point
│   ├── app.py             # Main window & navigation shell
│   ├── style.py           # Dark neon theme (QSS stylesheet)
│   ├── modules/
│   │   ├── home_page.py          # Knowledge graph homepage
│   │   ├── function_plotter.py   # 2D/3D function plotter
│   │   ├── formula_editor.py     # Formula editor with live preview
│   │   ├── math_history.py       # Interactive math history timeline
│   │   └── physics_simulator.py  # Physics scenario simulator
│   ├── widgets/
│   │   └── particle_canvas.py    # Reusable particle background
│   └── utils/
│       └── __init__.py
├── resources/
│   └── fonts/             # Local fonts (Orbitron, Inter)
├── math-knowledge-system/ # Original HTML mockups (reference)
├── openspec/              # Requirements & specs
├── requirements.txt
├── AGENTS.md
└── README.md
```
