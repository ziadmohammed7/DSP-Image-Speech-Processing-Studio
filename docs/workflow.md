# Project Workflow

The application follows a clear DSP workflow: load an input, preprocess it, apply DSP operations, visualize the result, save outputs, and export a report.

![Application Workflow](../assets/diagrams/workflow-diagram.png)

## End-to-End Flow

```mermaid
flowchart LR
    A["User Input"] --> B{"Input Type"}
    B --> C["Image Module"]
    B --> D["Audio Module"]
    C --> E["Preprocessing: grayscale conversion"]
    D --> F["Preprocessing: WAV read, mono conversion, normalization"]
    E --> G["DSP Algorithms: median, Gaussian, Sobel, Canny, histogram equalization"]
    F --> H["DSP Algorithms: low-pass, high-pass, band-pass filtering"]
    G --> I["Visualization: input/output image preview"]
    H --> J["Visualization: waveform and spectrogram plots"]
    I --> K["Save Processed Output"]
    J --> K
    K --> L["Export PDF Report"]
```

## Workflow Stages

| Stage | Image Workflow | Audio Workflow | Output |
| --- | --- | --- | --- |
| Input | Load PNG, JPG, JPEG, or BMP image | Load WAV audio file | Raw user-selected signal |
| Preprocessing | Convert to grayscale | Convert stereo to mono and normalize | Standardized signal for processing |
| DSP Processing | Apply denoising, edge detection, or contrast enhancement | Apply low-pass, high-pass, or band-pass filter | Processed image or audio |
| Visualization | Show input and output image previews | Plot waveform and spectrogram views | Before/after visual comparison |
| Save Output | Save processed PNG/JPG | Save filtered WAV | Reusable result file |
| Export | Generate PDF report | Embed audio visualizations in PDF | Academic-ready report |

## Portfolio Narrative

This workflow is valuable because it shows the complete engineering path from raw data to documented output. The project is not only a filter demo; it includes user interaction, DSP computation, visualization, file export, and release planning.
