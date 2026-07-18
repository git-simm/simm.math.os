# Spec: Python Desktop Math Learning System

**Status**: accepted
**Created**: 2026-07-18
**Author**: Codex

## Summary

Port the existing HTML-based math knowledge system (`math-knowledge-system/`) into a Python desktop application. The original design was created as Figma high-fidelity mockups exported to HTML/Tailwind. The Python version should faithfully reproduce the dark sci-fi visual style while adding native desktop capabilities.

## Motivation

- The current HTML version depends on CDN-hosted dependencies (Tailwind, Iconify, ECharts) and cannot work offline.
- A desktop app provides better performance, local file access, and a more integrated user experience.
- Python's scientific ecosystem (NumPy, SciPy, SymPy, Matplotlib) enables real computation beyond static mockups.

## Requirements

### Functional

1. **Navigation Shell** - Persistent top navbar with logo "MATH·OS", links to all 5 modules, and active-state highlighting.
2. **Home (Knowledge Graph)** - Immersive landing page with particle background canvas, knowledge node graph, and quick navigation cards.
3. **Function Plotter** - 2D/3D function plotting with equation input, parameter sliders, and real-time graph updates.
4. **Formula Editor** - Geometry-linked formula editor with LaTeX rendering, interactive parameter adjustment, and live preview.
5. **Math History Timeline** - Interactive vertical timeline of mathematical discoveries with expandable detail cards.
6. **Physics Simulator** - Physics scenario simulator (projectile, pendulum, orbit) with tab switching, parameter controls, and canvas animation.

### Non-Functional

- **Visual Style**: Dark background (#0a0e1a), cyan neon accents (#00d4ff), glassmorphism panels, Orbitron/Inter fonts.
- **Performance**: 60fps for canvas animations; graphs update within 100ms of parameter change.
- **Offline**: No CDN dependencies; bundle all fonts and icons locally.
- **Responsive**: Window should be resizable; minimum size 1024x768.

## Tech Stack

- **GUI Framework**: PySide6 (Qt for Python)
- **Plotting**: matplotlib + Qt backend for 2D/3D graphs
- **Math Engine**: NumPy, SymPy (symbolic computation), SciPy
- **LaTeX Rendering**: matplotlib built-in mathtext or QtMath
- **Animation**: QTimer + QPainter for canvas animations

## Module Mapping

| HTML Source | Python Module | Key Widgets |
|---|---|---|
| home.html | `modules/home_page.py` | ParticleCanvas, KnowledgeGraph, NavCards |
| function-plotter.html | `modules/function_plotter.py` | EquationInput, PlotCanvas2D/3D, Sliders |
| formula-editor.html | `modules/formula_editor.py` | LatexRenderer, GeometryCanvas, ParamSliders |
| math-history.html | `modules/math_history.py` | TimelineWidget, DetailCards |
| physics-simulator.html | `modules/physics_simulator.py` | SimulationCanvas, ControlPanel, TabBar |

## Acceptance Criteria

- [ ] All 5 modules launch and display correctly in a PySide6 window
- [ ] Navigation bar switches between modules without window reload
- [ ] Dark neon visual style matches the original HTML design
- [ ] Function plotter renders sin/cos/polynomial graphs from user input
- [ ] Physics simulator animates at least one scenario (e.g., projectile motion)
- [ ] Application works offline with no CDN requests
- [ ] Window resizes gracefully down to 1024x768

## Dependencies

- PySide6 >= 6.5
- matplotlib >= 3.7
- numpy >= 1.24
- sympy >= 1.12
- scipy >= 1.10
