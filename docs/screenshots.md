# Screenshots Guide

This guide defines the screenshot set needed for a polished GitHub, LinkedIn, CV, and academic portfolio presentation.

No real GUI screenshots were found in the provided repository. The paths below are ready for future real captures from the running PyQt5 application. Until those images are added, keep README references as tables or placeholder snippets so the project does not display fake UI output.

## Screenshot Checklist

| Screenshot Name | Recommended File Path | What It Should Show | README Usage |
| --- | --- | --- | --- |
| Main GUI | `assets/screenshots/gui/main-gui.png` | Full application window with the dark purple PyQt5 interface, tabs, controls, and preview panels. | Project Preview, Screenshots Gallery |
| Splash Screen | `assets/screenshots/gui/splash-screen.png` | Startup splash screen with project identity. | Screenshots Gallery |
| Image Processing Tab | `assets/screenshots/image-processing/image-tab.png` | Image tab with loaded input image and controls. | Screenshots Gallery |
| Image Noise Reduction | `assets/screenshots/image-processing/noise-reduction.png` | Before/after result using Gaussian or median filtering. | Image Processing Module |
| Edge Detection | `assets/screenshots/image-processing/edge-detection.png` | Sobel or Canny output with clear edges. | DSP Techniques, Screenshots Gallery |
| Histogram Equalization | `assets/screenshots/image-processing/histogram-equalization.png` | Contrast-enhancement before/after result. | Screenshots Gallery |
| Audio Processing Tab | `assets/screenshots/audio-processing/audio-tab.png` | Loaded WAV file with audio controls visible. | Screenshots Gallery |
| Waveform Visualization | `assets/screenshots/audio-processing/waveform-visualization.png` | Input and output waveform plots. | Speech Processing Module |
| Spectrogram Analysis | `assets/screenshots/audio-processing/spectrogram-analysis.png` | Input and output spectrograms before/after filtering. | Visualization Use Cases |
| Filter Controls | `assets/screenshots/audio-processing/filter-controls.png` | Cutoff frequency, band range, order, and playback controls. | Screenshots Gallery |
| PDF Export | `assets/screenshots/reports/pdf-export.png` | Export action or save dialog for the generated PDF report. | Report Generation |
| Generated Report Page | `assets/screenshots/reports/generated-report-page-1.png` | First page of generated PDF report. | Report Generation |
| Audio Report Page | `assets/screenshots/reports/generated-report-audio.png` | Report page with waveform/spectrogram plots. | Report Generation |
| Release Download | `assets/screenshots/reports/release-download.png` | GitHub Release or download page with executable asset. | Release Download |
| Project Folder Structure | `assets/screenshots/workflow/project-structure.png` | Clean repository folder layout on GitHub or locally. | Project Structure |
| Workflow Overview | `assets/screenshots/workflow/workflow-overview.png` | End-to-end process from input to report export. | Workflow Diagram |

## Placeholder Markdown Snippets

Use these snippets after the real screenshots are captured and saved at the listed paths:

```markdown
![Main GUI](../assets/screenshots/gui/main-gui.png)
![Image Processing Tab](../assets/screenshots/image-processing/image-tab.png)
![Image Noise Reduction](../assets/screenshots/image-processing/noise-reduction.png)
![Edge Detection](../assets/screenshots/image-processing/edge-detection.png)
![Audio Processing Tab](../assets/screenshots/audio-processing/audio-tab.png)
![Waveform Visualization](../assets/screenshots/audio-processing/waveform-visualization.png)
![Spectrogram Analysis](../assets/screenshots/audio-processing/spectrogram-analysis.png)
![PDF Report Export](../assets/screenshots/reports/pdf-export.png)
![Release Download](../assets/screenshots/reports/release-download.png)
![Project Folder Structure](../assets/screenshots/workflow/project-structure.png)
```

For the root `README.md`, remove the leading `../` from each path:

```markdown
![Main GUI](assets/screenshots/gui/main-gui.png)
```

## Capture Quality Guidelines

- Capture on Windows with 125 percent scaling or lower for crisp UI text.
- Use the same sample image/audio files across screenshots for consistency.
- Crop only if it improves clarity; keep enough UI context to prove the screenshot is from the actual app.
- Avoid personal usernames, private folders, browser tabs, or unrelated desktop icons.
- Export images as PNG for UI screenshots.
- Keep filenames lowercase and kebab-case.
