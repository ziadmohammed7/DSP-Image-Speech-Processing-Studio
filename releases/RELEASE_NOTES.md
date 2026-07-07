# v1.0 Final Release

## Release Summary

Image & Speech Processing Studio v1.0 is the final academic release prepared for the Digital Signal Processing (DSP) course submission.

## Features Completed

- PyQt5 desktop application with dark purple GUI.
- Splash screen and project identity metadata.
- Image loading and grayscale preview.
- Median filter and Gaussian filter for image denoising.
- Sobel and Canny edge detection.
- Histogram equalization.
- Live image preview and image output saving.
- WAV audio loading.
- Low-pass, high-pass, and band-pass Butterworth filtering.
- Speech noise-reduction preset.
- 50 Hz hum-reduction preset.
- Input and output audio playback.
- Waveform visualization.
- Spectrogram visualization.
- Filter cutoff, band range, and order controls.
- Automatic PDF report export.
- Academic report, presentation, generated report examples, datasets, and sample images organized for GitHub.

## Known Requirements

- Windows 64-bit is recommended for the executable build.
- WAV is the supported audio input format.
- A working audio output device is required for playback.
- Running from source requires Python and the dependencies in `requirements.txt`.

## Executable Distribution

The standalone executable is approximately 171 MB. To keep the GitHub repository clean, do not commit the executable directly.

Recommended distribution options:

- Upload `DSP_Image_Speech_Studio.exe` to GitHub Releases under tag `v1.0`.
- Upload the executable to Google Drive and place the public download link in the GitHub release description.
- Keep the local executable copy in `_local_artifacts/executable/`; this folder is ignored by Git.

## How To Run The Executable

1. Download `DSP_Image_Speech_Studio.exe` from the release page or shared drive link.
2. Use a Windows 64-bit computer.
3. Double-click the executable.
4. If Windows SmartScreen appears, choose the option to run the file only if you trust the source.

## Academic Submission Note

This release was prepared for the Digital Signal Processing (DSP) course at October High Institute for Engineering & Technology under the supervision of Dr. Abdullah Gad.
