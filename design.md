# Technical Design Specification

## Overview
This document outlines the software design, visual layout, data architecture, animation framework, and state persistence model for the Adaptive Traffic Signals project, adhering strictly to the constraints in [AGENTS.md](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/AGENTS.md) and requirements in [spec/requirements.md](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md).

---

## 1. Structure of `index.html` (In Page Order)

The entire application will be delivered in a single `index.html` file organized semantically into the following sequential components:

1. **Top Navigation & Motion Controls Bar (`<header>` / `<nav>`)**:
   - Project Title & Simulation Badging ("Simulated Benchmark").
   - Global Reduced Motion Toggle (`<button id="toggle-motion">`) with active/paused status icon (inline SVG).
   - Controller Mode Selector Tabs / Segmented Switch (`Fixed-Time` vs `Adaptive`).
   - Scenario Selector Dropdown / Pills.

2. **Hero Section (`<section id="hero">`)**:
   - Headline and project statement clearly stating the simulated comparison objective.
   - Prominent scientific integrity disclaimer chip: *"Simulated Model — Not Deployed to Physical Signals"*.
   - Hero preview animation: An abstract inline SVG micro-intersection depicting smooth traffic routing.

3. **Interactive 4-Way Junction Simulator (`<section id="simulator">`)**:
   - **Intersection Viewport**: Rendered using high-performance HTML5 `<canvas id="junction-canvas">` with realistic roadway lanes, stop lines, crosswalks, turn lanes, pedestrian refuge islands, and directional signals.
   - **Live Telemetry & Signal Status HUD (`<aside id="status-panel">`)**:
     - Current Active Phase (e.g., North-South Green, East-West Green, Clearance Yellow, All-Red).
     - Phase Countdown Timer (seconds remaining).
     - Real-time Approach Queues (North, South, East, West queue counts).
     - Simulation Clock / Epoch ticker.
     - Playback controls (Play, Pause, Step, Replay).

4. **Comparative Results & Analytics (`<section id="results">`)**:
   - **Headline Performance Cards**:
     - Average Wait Time (Fixed vs Adaptive, simulated seconds, delta %).
     - Average Queue Length (Fixed vs Adaptive, vehicles, delta %).
     - Maximum Queue Length (Fixed vs Adaptive, vehicles, delta %).
     - Honest Trade-off / Regression Callout card (highlighting scenarios where Adaptive exhibits neutral or regressed metrics).
   - **Performance Charts**:
     - Average Wait Time comparative bar / line chart (Fixed vs Adaptive across scenarios).
     - Average Queue Length comparison chart.
     - Maximum Queue Length comparison chart.
     - All charts rendered cleanly using inline SVG vectors and coordinate scaling without external libraries.

5. **Per-Seed Benchmark Table (`<section id="seed-breakdown">`)**:
   - Tabular view listing individual simulation runs across every seed defined in `DATA.md`.
   - Columns: Seed ID, Traffic Scenario, Fixed Controller Avg Wait, Adaptive Controller Avg Wait, Wait Delta, Queue Delta, and Integrity Checksum.

6. **Limitations & Methodology (`<section id="limitations">`)**:
   - Detailed scientific demarcation text explaining vehicle generation Poisson/fixed arrival models, absence of pedestrian / emergency vehicle preemptions, idealized braking curves, and non-connection to real signal equipment.

7. **Footer (`<footer>`)**:
   - Simulation attribution, local storage status indicator, and static project metadata.

---

## 2. Shape of the Hardcoded Data Object (`DATA.md` Ground Truth)

All operational numbers, timings, arrival matrices, and comparative results are structured into a single immutable JavaScript configuration object:

```javascript
const SIMULATION_DATA = {
  metadata: {
    datasetVersion: "1.0.0-simulated",
    simulationType: "4-Way Single Intersection Microsimulation",
    cycleTimeFixedSeconds: 60,
    yellowClearanceSeconds: 4,
    allRedClearanceSeconds: 2
  },
  scenarios: {
    balanced: {
      id: "balanced",
      name: "Balanced Flow",
      description: "Equal arrival distribution across North-South and East-West approaches.",
      arrivalRatePerMin: { north: 12, south: 12, east: 12, west: 12 },
      fixedTiming: {
        nsGreenSec: 24,
        nsYellowSec: 4,
        allRedSec: 2,
        ewGreenSec: 24,
        ewYellowSec: 4
      },
      adaptiveParameters: {
        minGreenSec: 10,
        maxGreenSec: 40,
        extensionSecPerVehicle: 2.5
      },
      results: {
        fixed: { avgWaitSec: 22.4, avgQueueVeh: 4.8, maxQueueVeh: 11 },
        adaptive: { avgWaitSec: 14.1, avgQueueVeh: 2.9, maxQueueVeh: 7 },
        delta: { waitReductionPct: -37.05, queueReductionPct: -39.58 }
      }
    },
    unbalancedPeak: {
      id: "unbalancedPeak",
      name: "Unbalanced Arterial Peak",
      description: "High volume along North-South arterial, low volume along East-West minor road.",
      arrivalRatePerMin: { north: 28, south: 26, east: 6, west: 5 },
      fixedTiming: {
        nsGreenSec: 24,
        nsYellowSec: 4,
        allRedSec: 2,
        ewGreenSec: 24,
        ewYellowSec: 4
      },
      adaptiveParameters: {
        minGreenSec: 10,
        maxGreenSec: 50,
        extensionSecPerVehicle: 2.5
      },
      results: {
        fixed: { avgWaitSec: 34.6, avgQueueVeh: 8.2, maxQueueVeh: 19 },
        adaptive: { avgWaitSec: 18.2, avgQueueVeh: 4.1, maxQueueVeh: 10 },
        delta: { waitReductionPct: -47.40, queueReductionPct: -50.00 }
      }
    },
    overCapacityTradeoff: {
      id: "overCapacityTradeoff",
      name: "Saturated / Over-Capacity (Regression/Trade-off)",
      description: "All approaches exceed saturation flow; demonstrates adaptive limits and slight cross-street wait regression.",
      arrivalRatePerMin: { north: 35, south: 35, east: 32, west: 30 },
      fixedTiming: {
        nsGreenSec: 24,
        nsYellowSec: 4,
        allRedSec: 2,
        ewGreenSec: 24,
        ewYellowSec: 4
      },
      adaptiveParameters: {
        minGreenSec: 10,
        maxGreenSec: 45,
        extensionSecPerVehicle: 2.0
      },
      results: {
        fixed: { avgWaitSec: 52.8, avgQueueVeh: 16.4, maxQueueVeh: 28 },
        adaptive: { avgWaitSec: 53.5, avgQueueVeh: 16.1, maxQueueVeh: 29 },
        delta: { waitReductionPct: +1.33, queueReductionPct: -1.83 } // Explicit honest regression
      }
    }
  },
  seeds: [
    { seedId: "SEED_1042", scenario: "balanced", fixedAvgWait: 22.1, adaptiveAvgWait: 14.3, fixedMaxQueue: 11, adaptiveMaxQueue: 7 },
    { seedId: "SEED_2085", scenario: "balanced", fixedAvgWait: 22.9, adaptiveAvgWait: 13.9, fixedMaxQueue: 12, adaptiveMaxQueue: 6 },
    { seedId: "SEED_3194", scenario: "unbalancedPeak", fixedAvgWait: 34.1, adaptiveAvgWait: 17.8, fixedMaxQueue: 18, adaptiveMaxQueue: 9 },
    { seedId: "SEED_4421", scenario: "unbalancedPeak", fixedAvgWait: 35.2, adaptiveAvgWait: 18.6, fixedMaxQueue: 20, adaptiveMaxQueue: 11 },
    { seedId: "SEED_5509", scenario: "overCapacityTradeoff", fixedAvgWait: 51.9, adaptiveAvgWait: 53.1, fixedMaxQueue: 27, adaptiveMaxQueue: 28 },
    { seedId: "SEED_6812", scenario: "overCapacityTradeoff", fixedAvgWait: 53.7, adaptiveAvgWait: 53.9, fixedMaxQueue: 29, adaptiveMaxQueue: 30 }
  ]
};
```

---

## 3. Human-Crafted Visual Aesthetics & Anti-AI Design Philosophy

To avoid generic, sterile, or stereotypically "AI-generated" templates (such as gratuitous glowing purple gradients, empty neon glassmorphism cards, and floating geometric blobs):

1. **Authentic Domain Tone (Civil & Traffic Engineering Console):**
   - Aesthetic modeled after modern municipal command systems and civil transport dashboards (e.g., Siemens Sitraffic / SCATS / SCOOT control consoles).
   - High-contrast, matte deep-slate slate palette (`#0a0f1d`, `#111827`, `#1f2937`) accented with calibrated signal optics: Signal Emerald (`#059669`, active `#10b981`), Amber (`#d97706`, active `#f59e0b`), and Stop Crimson (`#dc2626`, active `#ef4444`).
   - Clean, professional data typography utilizing system tabular monospaces (`ui-monospace, SFMono-Regular, Menlo, Consolas`) for telemetry and metrics, paired with crisp sans-serif headings.

2. **Handcrafted Physical Junction Detail:**
   - Instead of simplistic colored blocks moving on a grey cross, the canvas features realistic road markings: textured asphalt shading, weathered lane dashes, turn pocket arrows, pedestrian crosswalk zebra striping, stop bar setbacks, inductive loop detector wire cutouts in the asphalt, and signal pole gantries.
   - Distinct vehicle silhouettes: sedan, compact, delivery van, and municipal bus models with subtle brake light illumination states when stopping.

3. **Subtle, Intentional Micro-Interactions:**
   - Interactive hover cards that highlight sensor detection zones.
   - Smooth, non-distracting data tooltips showing exact vehicle queue timestamps.

---

## 4. Animation Architecture & Natural Physics

### A. Core Engine: Single Unified `requestAnimationFrame` Loop
To guarantee 60 FPS and avoid multi-timer synchronization drifts or layout thrashing:
- The simulation runs on a single centralized `requestAnimationFrame` loop.
- **Delta-Time Normalization:** Updates calculate `deltaTime = timestamp - lastTimestamp` capped at 100ms to avoid physics jumps during tab switching.
- **Clock Mapping:** The simulation clock advances deterministically in simulated seconds (`simTime += deltaTime * timeScale`).
- All signal timings (Green duration, Yellow clearance, All-red intervals) match the exact configured seconds in `SIMULATION_DATA`.
- Vehicle positions, braking physics, queues, and signal transitions are stepped in memory before drawing onto the canvas in a single paint pass.

### B. Natural Vehicle Kinematics (Organic, Non-Robotic Motion)
To eliminate stiff, unnatural AI movement:
- **Intelligent Driver Model (IDM) Inspired Car-Following:**
  - Smooth acceleration curves with realistic comfort limits (vehicles do not stop or start instantly).
  - Progressive deceleration into queue lines rather than linear snapping.
  - Natural reaction delay (0.4s to 0.6s staggered wave) when queue vehicles start rolling on green.
  - Realistic pitch chassis dipping slightly during hard deceleration and brake lights glowing red.
- **Detector Loop Feedback:**
  - Vehicles passing over simulated inductive loops trigger visual sensor blips, feeding into the adaptive controller logic.

### C. Element-by-Element Animation Breakdown
1. **4-Way Intersection & Vehicles:**
   - **Technology:** HTML5 Canvas 2D context.
   - **Reason:** Best performance for rendering dozens of moving car models, headlights, brake glow, and road markings at 60 FPS without DOM reflow overhead.
2. **Signal Heads & Phase Transitions:**
   - **Technology:** Canvas drawing synchronized with the active phase state.
   - **Optics:** Realistic signal housing with optical lens fresnel pattern and physical yellow clearance timing.
3. **Count-Up Numbers (Results Section):**
   - **Technology:** `requestAnimationFrame` tween (easing: cubic out) over 1200ms when triggered.
   - Sourced directly from `SIMULATION_DATA`.
4. **Comparative SVG Charts:**
   - **Technology:** Smooth CSS transitions on SVG `<rect>` `height` and `y` attributes, or coordinate interpolations via `requestAnimationFrame`.
5. **Hero Micro-Animation:**
   - **Technology:** Pure CSS keyframe transitions on SVG elements with `will-change: transform`.

### D. Reduced Motion & Pause Handling
- When `reducedMotion` is true:
  - The `requestAnimationFrame` loop stops advancing simulation time (`simTime`).
  - The canvas renders a clean, static, high-contrast snapshot of the intersection at tick 0 or the current pause point.
  - Count-up numbers resolve instantaneously to their final values without easing (`element.textContent = targetValue`).
  - SVG chart bars render immediately at full dimension (`transition: none`).
  - CSS keyframes in the hero section are disabled via `@media (prefers-reduced-motion: reduce)` and the `.reduced-motion` root class (`animation: none !important; transition: none !important;`).

---

## 5. State Management & `localStorage` Persistence

### State Schema
The application maintains a centralized state object:
```javascript
const appState = {
  controllerMode: "adaptive", // "fixed" | "adaptive"
  selectedScenario: "balanced", // "balanced" | "unbalancedPeak" | "overCapacityTradeoff"
  reducedMotion: false,       // boolean
  simulationRunning: true     // boolean
};
```

### Persistence Protocol
1. **Keys:**
   - `ats_controller_mode`
   - `ats_selected_scenario`
   - `ats_reduced_motion`
2. **Restoration on Startup:**
   - On DOM initialization, check `localStorage.getItem(key)`.
   - If `ats_reduced_motion` is not explicitly set in `localStorage`, query the system preference:
     `window.matchMedia('(prefers-reduced-motion: reduce)').matches`.
   - Update UI inputs (mode toggles, scenario dropdown, motion button) to reflect restored state.
   - Add/remove `.reduced-motion` class to `document.documentElement`.
3. **Change Listeners:**
   - When the user alters any control, immediately update `appState`, save the value to `localStorage`, update DOM representations, and trigger a clean reset of the intersection playback.
   - Listen to `window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', ...)` to react dynamically if OS accessibility settings change while the page is open.
