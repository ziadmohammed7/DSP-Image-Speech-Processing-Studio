# Contributing

Thank you for your interest in improving Image & Speech Processing Studio.

This repository began as an academic DSP course project, so contributions should preserve the educational clarity of the application while improving reliability, maintainability, and documentation.

## Good Contribution Areas

- Add missing DSP operations such as average filtering, bilateral filtering, Laplacian edge detection, and band-stop/notch audio filtering.
- Improve the GUI without changing the project identity or core workflow.
- Add tests for image filters, audio filters, and report export helpers.
- Improve packaging and release automation.
- Add screenshots, demo videos, or clearer academic documentation.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python src/main.py
```

## Guidelines

- Keep source changes focused and easy to review.
- Do not commit generated PyInstaller output, local executables, Python caches, or temporary reports.
- Keep README feature claims aligned with implemented source behavior.
- Prefer clear DSP explanations over decorative complexity.
- Test manually with at least one sample image and one WAV file before opening a pull request.

## Academic Integrity

If you reuse this project in coursework, cite the original team members, supervisor, and institution. Do not submit this repository as your own unauthored work.
