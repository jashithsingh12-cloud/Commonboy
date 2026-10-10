# Functional Requirements Specification

## Overview
This document specifies the functional and animation requirements for the single-page Adaptive Traffic Signals simulation website, strictly adhering to [AGENTS.md](file:///c:/Users/Paresh%20Asher/OneDrive/Desktop/commonboysui/AGENTS.md). All requirements are formulated using the Easy Approach to Requirements Syntax (EARS): `WHEN <trigger> THE SYSTEM SHALL <behaviour>`.

---

## Requirements List

### 1. Hero Section & Initial Presentation
1. **REQ-001:** WHEN the page loads, THE SYSTEM SHALL display a hero section introducing the Adaptive Traffic Signals project with explicit labels denoting all presented data and models as simulated.
2. **REQ-002:** WHEN the hero section renders and reduced motion is inactive, THE SYSTEM SHALL execute a short animated junction intro sequence displaying miniature vehicles traversing a crossroads.
3. **REQ-003:** WHEN the hero section renders and reduced motion is active (via OS setting or UI toggle), THE SYSTEM SHALL halt all introductory vehicle movement and display a static junction overview instead.

### 2. State Persistence & Motion Preferences
4. **REQ-004:** WHEN the page loads, THE SYSTEM SHALL read and restore the previously persisted controller mode, active scenario, and reduced-motion toggle state from `localStorage` (falling back to predefined defaults if uninitialized).
5. **REQ-005:** WHEN the user clicks the visible reduced-motion toggle in the UI, THE SYSTEM SHALL toggle the reduced-motion state, persist the new state in `localStorage`, and apply or remove reduced-motion styling and animation execution immediately.
6. **REQ-006:** WHEN the user's operating system signals a change in the `prefers-reduced-motion` media query, THE SYSTEM SHALL update the motion state accordingly, halting or enabling motion unless explicitly overridden by user UI selection.

### 3. Junction Simulation & Replay
7. **REQ-007:** WHEN the simulation loop executes and reduced motion is inactive, THE SYSTEM SHALL animate the approach of vehicles toward the 4-way junction from each approach direction based on arrival rates defined in `DATA.md`.
8. **REQ-008:** WHEN the approach signal is red and reduced motion is inactive, THE SYSTEM SHALL animate arriving vehicles decelerating and coming to a stop in a queue behind the stop line.
9. **REQ-009:** WHEN the approach signal turns green and reduced motion is inactive, THE SYSTEM SHALL animate queued vehicles accelerating and discharging through the intersection.
10. **REQ-010:** WHEN signal phase transitions occur and reduced motion is inactive, THE SYSTEM SHALL animate the traffic signal heads transitioning in order through Green, Yellow, and All-Red clearance states according to timings defined in `DATA.md`.
11. **REQ-011:** WHEN reduced motion is active (via OS preference or UI toggle), THE SYSTEM SHALL immediately freeze or halt all vehicle translations and transition light colors instantaneously without cross-fades or motion effects, maintaining accurate static position and queue displays.
12. **REQ-012:** WHEN the user switches the controller mode between Fixed and Adaptive, THE SYSTEM SHALL persist the selection to `localStorage`, reset the junction simulation timeline to the beginning of the selected scenario, and replay the simulation from tick zero under the newly selected controller logic.
13. **REQ-013:** WHEN the user selects a different traffic scenario, THE SYSTEM SHALL persist the selection to `localStorage`, load the scenario parameters strictly from `DATA.md`, and replay the simulation under the active controller mode.

### 4. Live Intersection Status Panel
14. **REQ-014:** WHEN the simulation advances, THE SYSTEM SHALL display a live status panel indicating the active signal phase name, active green direction, and controller type.
15. **REQ-015:** WHEN the simulation timer advances, THE SYSTEM SHALL display a live countdown timer showing the remaining seconds in the active phase as calculated from `DATA.md`.
16. **REQ-016:** WHEN vehicle counts update at each approach, THE SYSTEM SHALL update the live status panel with the instantaneous queue length (in vehicles) for the North, South, East, and West approaches.

### 5. Results & Comparative Performance Metrics
17. **REQ-017:** WHEN the results section scrolls into viewport or controller mode is switched and reduced motion is inactive, THE SYSTEM SHALL trigger count-up animations for aggregate performance numbers (average wait time, average queue length, max queue length) transitioning smoothly from zero to the exact values sourced from `DATA.md`.
18. **REQ-018:** WHEN the results section renders and reduced motion is active, THE SYSTEM SHALL render final numerical values immediately without count-up easing.
19. **REQ-019:** WHEN comparative charts for average wait time, average queue length, and max queue length enter viewport and reduced motion is inactive, THE SYSTEM SHALL animate the chart bars and line series growing from base levels to the target values derived from `DATA.md`.
20. **REQ-020:** WHEN comparative charts render and reduced motion is active, THE SYSTEM SHALL render the chart bars and line series statically at their full computed heights and coordinates without animation.
21. **REQ-021:** WHEN the results section renders, THE SYSTEM SHALL present side-by-side comparative metrics for both Fixed and Adaptive controllers, explicitly reporting observed regressions or trade-offs alongside observed gains as documented in `DATA.md`.
22. **REQ-022:** WHEN displaying any comparative metric, percentage, or delta ratio, THE SYSTEM SHALL compute the value strictly from the raw data in `DATA.md` without presenting any ungrounded figures.

### 6. Per-Seed Simulation Breakdown
23. **REQ-023:** WHEN viewing the results section, THE SYSTEM SHALL render a per-seed breakdown table displaying individual simulation run metrics across each random seed defined in `DATA.md`.
24. **REQ-024:** WHEN displaying the per-seed table, THE SYSTEM SHALL display seed identifier, arrival pattern, Fixed controller performance metrics, and Adaptive controller performance metrics directly matching `DATA.md`.

### 7. Limitations & Scientific Demarcation
25. **REQ-025:** WHEN the user navigates through the page, THE SYSTEM SHALL display a dedicated Limitations section detailing the simulation boundaries, assumptions, lack of physical hardware integration, and synthetic vehicle generation constraints.
26. **REQ-026:** WHEN any performance metric or graph is visible, THE SYSTEM SHALL maintain clear textual disclaimers that all data points reflect simulated benchmark scenarios and do not represent physical road deployments.
