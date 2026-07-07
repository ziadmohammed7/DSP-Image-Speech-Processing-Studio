# Visual Branding Guide

This guide keeps the repository visually consistent across README sections, screenshots, diagrams, release notes, and social previews.

## Color Palette

| Role | Hex | Usage |
| --- | --- | --- |
| Main background | `#100c22` | README visuals, diagrams, app screenshots. |
| Deep panel | `#1f1835` | Diagram cards and dark UI panels. |
| Secondary panel | `#2a2045` | Highlighted architecture layers. |
| Primary accent | `#bb86fc` | Badges, arrows, key highlights. |
| Soft accent | `#d7b7ff` | Section subtitles and secondary headings. |
| Text | `#ffffff` | Main diagram text. |
| Muted text | `#d8cdef` | Supporting diagram text. |
| Success accent | `#45d483` | Positive status and output paths. |
| Blue accent | `#69b7ff` | Visualization and workflow links. |

## Screenshot Style Rules

- Use real screenshots from the running PyQt5 app only.
- Capture the full application window when showing workflow context.
- Use cropped screenshots only when a feature needs close inspection.
- Avoid personal folders, private file paths, browser tabs, and desktop clutter.
- Prefer PNG for UI screenshots.
- Keep the dark purple theme visible in all application captures.

## Naming Conventions

- Use lowercase kebab-case filenames.
- Use category folders under `assets/screenshots/`.
- Prefer descriptive names such as `noise-reduction.png`, `spectrogram-analysis.png`, and `generated-report-page-1.png`.

## GitHub Social Preview

Recommended social preview:

- Use `assets/diagrams/architecture-diagram.png` for a technical preview, or a cropped composite of `main-gui.png` and `workflow-diagram.png`.
- Keep the title readable at small sizes.
- Avoid using QR codes or raw report pages as the main social preview.

## README Consistency Rules

- Keep the README visual and scannable.
- Put deeper explanations in `docs/` and link to them.
- Reference only images that exist.
- Keep future or unavailable screenshots as checklist rows, not broken image embeds.
- Keep feature claims aligned with the current source code.
