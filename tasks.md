# Implementation Tasks Specification

This plan specifies the implementation roadmap for the Adaptive Traffic Signals single-page application (`index.html`) across **exactly 3 phases**. Each task maps directly to the requirement number(s) in [spec/requirements.md](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md) that it fulfills. Each phase concludes with a concrete verification milestone executable in the browser.

---

## Phase 1: Foundation, Hero Presentation & Animated 4-Way Junction (Visible Milestone)

### Goal
Deliver a fully functional visual foundation: the single `index.html` structure, top bar controls, hero section with simulation notices, and the live 60 FPS HTML5 Canvas animated 4-way intersection driven strictly by parameters from `DATA.md`.

### Tasks
- [x] **Task 1.1: Single HTML Document Scaffolding & Design System Tokens**
  - Implement the single-file boilerplate in `index.html` with inline `<style>` and `<script>`.
  - Establish CSS custom property palette (curated dark slate theme, signal greens/ambers/reds, typography using system stacks).
  - Implements: [REQ-001](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L11).
- [x] **Task 1.2: Hardcoded Ground Truth Data Object**
  - Embed the complete, immutable `SIMULATION_DATA` object into the script, hardcoded exclusively from `DATA.md` (metadata, scenarios, signal timings, arrival rates, comparative outcomes, and seed runs).
  - Implements: [REQ-007](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L21), [REQ-010](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L24), [REQ-022](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L40).
- [x] **Task 1.3: Hero Section & Scientific Demarcation Badges**
  - Render the hero header with clear statements that all results are simulated and not connected to physical traffic controllers.
  - Render the hero intro SVG micro-animation depicting stylized traffic flow.
  - Implements: [REQ-001](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L11), [REQ-002](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L12), [REQ-003](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L13), [REQ-026](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L48).
- [x] **Task 1.4: 4-Way Junction Canvas & Roadway Geometry**
  - Draw the 4-way intersection on `<canvas id="junction-canvas">`: dual-lane approaches (North, South, East, West), center cross intersection, stop lines, pedestrian crosswalk markings, and lane divider dashes.
  - Ensure retina/HiDPI device pixel ratio scaling for crisp rendering.
  - Implements: [REQ-007](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L21).
- [x] **Task 1.5: Delta-Time Animation Engine & Signal Phase Machine**
  - Implement the centralized `requestAnimationFrame` simulation loop with delta-time advancement.
  - Implement the signal controller state machine cycling through North-South Green -> Yellow -> All-Red -> East-West Green -> Yellow -> All-Red with timings sourced strictly from `SIMULATION_DATA`.
  - Draw illuminated traffic signal heads and directional arrows on the canvas with phase states.
  - Implements: [REQ-007](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L21), [REQ-010](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L24).
- [x] **Task 1.6: Vehicle Generation, Deceleration, Queuing, and Discharge**
  - Implement vehicle objects generated according to scenario arrival rates.
  - Implement vehicle motion physics: cruising speed, smooth deceleration behind stop lines when signal is red, queue spacing behind preceding cars, and acceleration through green lights.
  - Implements: [REQ-007](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L21), [REQ-008](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L22), [REQ-009](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L23).

### Phase 1 Verification Milestone
Open `index.html` in the local live server preview. The page immediately loads with the hero section, scientific simulation badges, and an actively running, silky-smooth 60 FPS 4-way intersection where cars arrive, queue at red lights, and proceed through green signals.

---

## Phase 2: Controller Switching, Live HUD & Motion State Persistence

### Goal
Introduce interactive control over the simulation: toggling between Fixed and Adaptive controllers, switching traffic scenarios, displaying real-time HUD telemetry, and persisting all user choices in `localStorage` while fully honoring reduced-motion settings.

### Tasks
- [x] **Task 2.1: LocalStorage State Manager & Reduced-Motion Handlers**
  - Implement state persistence reading and storing `ats_controller_mode`, `ats_selected_scenario`, and `ats_reduced_motion`.
  - Wire the visible UI motion toggle button to pause/resume motion and toggle the `.reduced-motion` root class.
  - Attach listener for system `(prefers-reduced-motion: reduce)` changes.
  - Implements: [REQ-004](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L16), [REQ-005](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L17), [REQ-006](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L18), [REQ-011](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L25).
- [x] **Task 2.2: Adaptive Controller Logic & Dynamic Green Extension**
  - Implement adaptive algorithm in the simulation loop: monitors waiting queue lengths and vehicle gaps, dynamically extending green time between `minGreenSec` and `maxGreenSec` as configured in `SIMULATION_DATA`.
  - Implements: [REQ-012](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L26).
- [x] **Task 2.3: Controller Mode Switcher & Replay Logic**
  - Add interactive toggle/tabs for "Fixed-Time" vs "Adaptive Controller".
  - When switched, reset the simulation timeline to tick 0, clear active queues, and replay the scenario from the beginning under the selected controller mode.
  - Implements: [REQ-012](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L26).
- [x] **Task 2.4: Traffic Scenario Selector & Parameter Loading**
  - Implement scenario switcher UI (Balanced Flow, Unbalanced Arterial Peak, Saturated Over-Capacity).
  - Loading a scenario updates vehicle arrival distributions and resets simulation replay.
  - Implements: [REQ-013](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L27).
- [x] **Task 2.5: Live Intersection Status Panel (HUD)**
  - Build the status panel overlay/aside displaying current phase name, live countdown timer for the active phase, and live queue count badges for North, South, East, and West approaches.
  - Implements: [REQ-014](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L30), [REQ-015](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L31), [REQ-016](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L32).

### Phase 2 Verification Milestone
Open `index.html`. Switch between Fixed and Adaptive modes to observe the junction immediately reset and replay with visibly different signal timings (e.g. adaptive green extending for heavy approaches). Observe the live HUD showing changing phase countdowns and vehicle queue counts. Toggle the motion pause button: all vehicle movement and signal timers freeze instantly. Refresh the browser: all selected modes, scenarios, and motion settings remain intact.

---

## Phase 3: Results Analytics, Animated SVG Charts, Seed Table & Limitations

### Goal
Present the comprehensive comparative analytics, animated count-up metrics, responsive inline SVG charts, honest trade-off disclosures, the per-seed breakdown table, and the scientific limitations section.

### Tasks
- [x] **Task 3.1: Animated Count-Up Headline Performance Cards**
  - Render metric cards for Average Wait Time, Average Queue Length, and Maximum Queue Length.
  - Implement smooth count-up numerical tweening when visible; when reduced motion is active, display final values statically.
  - Implements: [REQ-017](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L35), [REQ-018](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L36), [REQ-021](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L39), [REQ-022](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L40).
- [x] **Task 3.2: Inline SVG Comparative Charts (Fixed vs Adaptive)**
  - Construct responsive inline SVG charts (no external libraries) for Average Wait Time, Average Queue Length, and Max Queue Length across scenarios.
  - Animate bar heights and line data points on load; display statically if reduced motion is enabled.
  - Implements: [REQ-019](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L37), [REQ-020](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L38), [REQ-021](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L39).
- [x] **Task 3.3: Honest Reporting & Regression/Trade-off Callouts**
  - Highlight the "Saturated / Over-Capacity" scenario showing neutral or regressed metrics under adaptive control (+1.33% wait time regression) as defined in `SIMULATION_DATA`.
  - Implements: [REQ-021](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L39), [REQ-022](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L40).
- [x] **Task 3.4: Per-Seed Simulation Breakdown Table**
  - Build the comprehensive benchmark table rendering metrics for each random seed run from `SIMULATION_DATA`.
  - Provide sorting or scenario filtering.
  - Implements: [REQ-023](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L43), [REQ-024](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L44).
- [x] **Task 3.5: Scientific Limitations & Scope Demarcation Section**
  - Author the Limitations section covering simulated modeling boundaries, discrete car-following rules, absence of emergency preemptions, and explicit demarcation against physical controller deployment.
  - Implements: [REQ-025](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L47), [REQ-026](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/spec/requirements.md#L48).

### Phase 3 Verification Milestone
Open `index.html`. Scroll down to view the animated count-up cards and SVG bar charts illustrating Fixed vs Adaptive comparisons. Inspect the honest trade-off card showing saturated conditions. Verify that every single number in the charts, cards, and per-seed table matches `DATA.md` exactly. Toggle reduced-motion: confirm count-ups and chart bar transitions halt immediately. Review the full limitations text confirming clear scientific demarcation.
