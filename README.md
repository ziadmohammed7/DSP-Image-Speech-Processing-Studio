<div align="center">

# Image & Speech Processing Studio

### Digital Signal Processing (DSP) Desktop Application

A PyQt5 desktop studio for demonstrating practical DSP concepts through image processing, speech/audio filtering, signal visualization, and automatic PDF report generation.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop%20GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-Signal%20Processing-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![DSP](https://img.shields.io/badge/DSP-Digital%20Signal%20Processing-7A2E8F?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-64--bit-0078D6?style=for-the-badge&logo=windows&logoColor=white)

**Course:** Digital Signal Processing (DSP)  
**Institution:** October High Institute for Engineering & Technology  
**Supervisor:** Dr. Abdullah Gad

</div>

---

## Project Overview

Image & Speech Processing Studio is an academic desktop application built to connect DSP theory with hands-on experimentation. It provides an interactive dark-themed GUI where users can load images or WAV audio, apply DSP operations, visualize before/after results, and export a structured PDF report for documentation.

The project is intended for portfolio presentation, university submission, and continued open-source improvement.

## Key Features

| Area | Implemented Capabilities |
| --- | --- |
| Image processing | Image loading, grayscale conversion, median filtering, Gaussian filtering, Sobel edge detection, Canny edge detection, histogram equalization, live preview, presets, output saving |
| Speech/audio processing | WAV loading, mono conversion, low-pass filtering, high-pass filtering, band-pass filtering, speech noise-reduction preset, 50 Hz hum-reduction preset, output saving |
| Visualization | Input/output image preview, waveform plots, spectrogram plots, processing log |
| Reporting | Automatic PDF export with selected parameters, image results, audio waveforms, and spectrograms |
| Desktop experience | Modern dark purple PyQt5 interface, splash screen, toolbar actions, audio playback controls |

## Image Processing Module

The image module uses OpenCV and NumPy to process grayscale image data through common DSP and computer vision operations:

- Load PNG, JPG, JPEG, and BMP images.
- Convert input images to grayscale for consistent processing.
- Apply median and Gaussian filters for noise reduction.
- Apply Sobel and Canny operators for edge detection.
- Apply histogram equalization for contrast enhancement.
- Adjust kernel size, Gaussian sigma, and Canny thresholds.
- Save processed output images as PNG or JPG.

## Speech Processing Module

The speech/audio module uses SciPy, SoundFile, SoundDevice, NumPy, and Matplotlib:

- Load WAV files and convert stereo audio to mono.
- Normalize audio safely before processing and playback.
- Apply Butterworth low-pass, high-pass, and band-pass filters.
- Use zero-phase filtering with `scipy.signal.filtfilt`.
- Use presets for speech noise reduction and low-frequency hum reduction.
- Compare input/output waveforms and spectrograms.
- Play input and processed audio directly from the GUI.
- Save filtered audio as WAV.

## GUI Features

- PyQt5 desktop interface with a polished dark purple theme.
- Split image preview for input and processed output.
- Live image update mode for parameter tuning.
- Compact controls for filtering modes and presets.
- Audio playback buttons for input, output, and stop.
- Built-in processing log for user feedback.
- Splash screen and application identity metadata.

## DSP Techniques Implemented

| Category | Techniques |
| --- | --- |
| Image DSP | Spatial filtering, grayscale conversion, median denoising, Gaussian smoothing, Sobel gradient magnitude, Canny edge detection, histogram equalization |
| Audio DSP | Sampling-rate aware filtering, Butterworth IIR filter design, low-pass filtering, high-pass filtering, band-pass filtering, zero-phase filtering, waveform analysis, spectrogram analysis |
| Reporting | ReportLab PDF generation, embedded processed images, embedded Matplotlib plots |

## PDF Report Generation

The application can export an automatic PDF report containing:

- Project identity, course, supervisor, and team metadata.
- Selected image processing method and parameters.
- Selected audio filter settings and order.
- Input and output image results.
- Input/output audio waveforms.
- Input/output spectrograms.

Generated report examples are available in [`docs/generated-reports`](docs/generated-reports).

## Screenshots

No final GUI screenshots were included in the original folder. The screenshot folder is ready at [`assets/screenshots`](assets/screenshots), with naming guidance in [`assets/screenshots/README.md`](assets/screenshots/README.md).

Recommended screenshot names:

- `main-window.png`
- `image-processing.png`
- `audio-processing.png`
- `pdf-report.png`

## Demo Video

No demo video file was present in the provided folder. A placeholder and publishing guidance are available in [`videos/README.md`](videos/README.md).

## Installation

Clone the repository:

```bash
git clone https://github.com/YourUsername/DSP-Image-Speech-Processing-Studio.git
cd DSP-Image-Speech-Processing-Studio
```

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## Run From Source

```powershell
python src/main.py
```

The application expects image files in common formats such as PNG/JPG/BMP and audio files in WAV format.

## Requirements

- Windows 64-bit recommended.
- Python 3.10 or newer.
- A working audio output device for playback.
- Python packages listed in [`requirements.txt`](requirements.txt).

Core libraries:

| Library | Purpose |
| --- | --- |
| PyQt5 | Desktop GUI |
| OpenCV | Image processing |
| NumPy | Array operations |
| SciPy | DSP filters and spectrograms |
| Matplotlib | Waveform and spectrogram plots |
| SoundFile | WAV loading and saving |
| SoundDevice | Audio playback |
| ReportLab | PDF report generation |

## Project Structure

```text
DSP-Image-Speech-Processing-Studio/
├── assets/
│   ├── icons/
│   ├── qr/
│   └── screenshots/
├── docs/
│   ├── generated-reports/
│   ├── legacy/
│   ├── presentation/
│   └── report/
├── releases/
│   └── RELEASE_NOTES.md
├── samples/
│   ├── audio/
│   └── images/
├── src/
│   └── main.py
├── videos/
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── requirements.txt
```

Large local-only files such as the standalone executable and PyInstaller build output are preserved under `_local_artifacts/` and ignored by Git.

## Application Access / Release Notes

The standalone Windows executable is approximately 171 MB, so it should be distributed through GitHub Releases or Google Drive instead of being committed directly to the repository.

See [`releases/RELEASE_NOTES.md`](releases/RELEASE_NOTES.md) for the v1.0 final release notes and binary distribution guidance.

The project QR code is stored in [`assets/qr/application-download-qr.png`](assets/qr/application-download-qr.png).

## Academic Deliverables

- Final report: [`docs/report/digital-signal-processing-report.pdf`](docs/report/digital-signal-processing-report.pdf)
- Editable report: [`docs/report/digital-signal-processing-report.docx`](docs/report/digital-signal-processing-report.docx)
- Presentation PDF: [`docs/presentation/image-speech-processing-studio.pdf`](docs/presentation/image-speech-processing-studio.pdf)
- Presentation deck: [`docs/presentation/image-speech-processing-studio.pptx`](docs/presentation/image-speech-processing-studio.pptx)
- Generated PDF examples: [`docs/generated-reports`](docs/generated-reports)

## Team Members

| Name |
| --- |
| Ziad Mohamed Fathy |
| Moaz Atef Gouda |
| Ibrahim Mohamed Saad |
| Mohamed Ali Rushdi |
| Mohamed Abdel-Fadil |

## Supervisor and Institution

| Field | Details |
| --- | --- |
| Course | Digital Signal Processing (DSP) |
| Supervisor | Dr. Abdullah Gad |
| Institution | October High Institute for Engineering & Technology |
| Department | Telecommunications & Electronics Engineering |

## Future Improvements

- Add average, bilateral, and Laplacian filters to expand the image-processing module.
- Add a true band-stop/notch filter mode for audio workflows.
- Add automated unit tests for filter functions and report export.
- Split the single GUI file into smaller modules for long-term maintainability.
- Add official screenshots and a short demo video.
- Add a PyInstaller build workflow and release checklist.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE).

## Academic Note

This repository was prepared as a Digital Signal Processing course project. It is intended for learning, demonstration, and portfolio use. If reused academically, cite the original team and institution appropriately.
