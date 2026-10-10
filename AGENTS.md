# AGENTS.md — Permanent Rules & Project Guidelines

## 1. Project Overview
A single-page website that presents an **Adaptive Traffic Signals** project featuring:
- One simulated 4-way intersection / junction.
- Comparison between a **Fixed-time controller** and an **Adaptive controller**.
- Measured comparative results and performance metrics.

---

## 2. Hard Architectural Constraints
- **Single File Delivery:** The entire web app must reside in a single `index.html` file containing inline CSS (`<style>`) and vanilla JavaScript (`<script>`).
- **No External Dependencies:**
  - Zero frameworks (no React, Vue, Svelte, Tailwind, etc.).
  - No npm, build tools, bundlers, or package managers.
  - No CDNs (no external libraries like Bootstrap, FontAwesome, D3, etc.).
  - No external fonts (no Google Fonts; rely exclusively on system font stacks).
  - No external images (all icons and visual assets must be drawn inline using SVG, CSS, or HTML5 Canvas).
- **Execution Environment:** Must run cleanly on a local live server (Antigravity preview / local HTTP server), not via double-clicked `file://` protocol.
- **Data Ground Truth:** Every number, measurement, and metric shown on the page must be sourced directly and hardcoded from `DATA.md` and nowhere else.
- **Persistence & State:** UI state (selected controller mode, scenario, and reduced-motion toggle) must persist in `localStorage`.
- **Project Structure:**
  - Specifications and design documents go in the `spec/` directory.
  - Baseline dataset lives in `DATA.md`.
  - Main app lives in `index.html`.

---

## 3. Honesty & Scientific Integrity Rules
- **Explicit Simulation Labelling:** All results, metrics, and comparisons must be clearly labeled as **simulated**, never presented as real-world or field-tested.
- **Strict Metric Derivation:** Never display a percentage, ratio, or metric that is not explicitly defined in or computed from `DATA.md`.
- **Unbiased Reporting:** Show regressions, trade-offs, and failure cases alongside gains (do not cherry-pick only favorable outcomes).
- **Scope Demarcation:** Never state or imply that this software interfaces with, controls, or deploys to physical traffic signals.

---

## 4. Animation & Visual Presentation Rules
- **Permitted Technologies:** Animations must use CSS transitions/keyframes, `requestAnimationFrame`, or inline SVG animation only.
- **Accessibility & Motion Control:**
  - Full support for `prefers-reduced-motion` media queries.
  - A visible UI toggle to pause/disable all animations manually.
  - When reduced-motion or the pause toggle is active, all dynamic movement must halt cleanly without breaking state display.
- **Performance Targets:** Must maintain a rock-solid 60 FPS on a standard laptop. Avoid layout thrashing and expensive reflows.
- **Data-Driven Visuals:** The visual state and timings of the animated 4-way junction must be strictly driven by the scenarios and numbers in `DATA.md`, never by invented or arbitrary variables.
