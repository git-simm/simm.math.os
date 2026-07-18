# Repository Guidelines

## Project Structure & Module Organization

`
simm.math.os/
├── math-knowledge-system/   # Standalone page modules
│   ├── home.html            # Knowledge graph (entry page)
│   ├── function-plotter.html
│   ├── formula-editor.html
│   ├── math-history.html
│   └── physics-simulator.html
├── *.html                   # Root copies of the same pages
└── README.md
`

This is a flat, client-side math knowledge system. Every .html file is self-contained: HTML, inline <style>, and inline <script> all live in one file. There is no build step, bundler, or backend. Dependencies (Tailwind, Iconify, ECharts) are loaded from CDN.

Root-level .html files and math-knowledge-system/ duplicates must stay in sync—every change to one should be mirrored to the other.

## Build, Test, and Development Commands

None required. Open any .html file directly in a browser to run it:

`
start math-knowledge-system/home.html
`

Validate HTML (optional, requires Node.js):

`
npx html-validate math-knowledge-system/*.html
`

## Coding Style & Naming Conventions

- **Language:** Simplified Chinese (zh-CN) for UI labels; English for code identifiers.
- **Indentation:** 4 spaces for HTML/CSS/JS.
- **CSS:** Inline <style> block in <head>. Use the existing utility classes (glass-panel, 
eon-text, ont-tech, 
av-link) before adding new ones.
- **JS:** Inline <script> at end of <body>. Prefer const and let over ar. Use camelCase for function names.
- **Naming:** HTML files use kebab-case. New pages should follow the noun-descriptor pattern (e.g., data-analyzer.html).
- **Dependencies:** Do not add new CDN dependencies without noting the reason in a comment.

## Testing Guidelines

No automated test suite exists. Manual testing checklist:

1. Open each .html file in at least one modern browser (Chrome/Edge).
2. Verify all navigation links work and highlight correctly.
3. Resize the viewport—the layout should remain usable at mobile widths.
4. Check the browser console for errors.

## Commit & Pull Request Guidelines

- **Commits:** Use concise imperative summaries. The existing convention: Initial commit. Future commits should follow a similar plain-English style, e.g., Add calculus module, Fix navigation highlight on mobile.
- **PRs:** Each PR should describe the change and list which pages were touched. Attach a screenshot if the change is visual. Link any related issue.
- Keep the two file locations (root and math-knowledge-system/) synchronized in the same commit.

## Security & Configuration

- All dependencies are loaded from external CDNs. If offline access is needed, vendor them into a endor/ directory and update the <script> and <style> references accordingly.
- No environment variables or secrets are required.
