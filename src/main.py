import sys
import os
import io
import time
import numpy as np
import cv2

from scipy import signal
import soundfile as sf
import sounddevice as sd  # playback

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog,
    QComboBox, QSlider, QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
    QMessageBox, QSplitter, QTabWidget, QAction, QToolBar, QStatusBar,
    QTextEdit, QSplashScreen, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QFont, QColor

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# =========================
# PROJECT IDENTITY
# =========================
PROJECT_TITLE = "Image & Speech Processing Studio"
COURSE_NAME = "Digital Signal Processing (DSP)"
INSTRUCTOR_NAME = "Dr. Abdullah Gad"
INSTITUTE_NAME = "October High Institute for Engineering & Technology"

GROUP_INFO = (
    "Group Members: "
    "Ziad Mohamed, Moaz Atef, Ibrahim Mohamed, "
    "Mohamed Ali, Mohamed Abdel-Fadil"
)

UNIVERSITY_INFO = "Telecommunications & Electronics Engineering"
VERSION = "v1.0 — Professional Edition"

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = getattr(sys, "_MEIPASS", os.path.dirname(SOURCE_DIR))


def resource_path(*parts: str) -> str:
    return os.path.join(PROJECT_ROOT, *parts)


APP_ICON_ICO = resource_path("assets", "icons", "app_icon.ico")


# =========================
# THEME COLORS
# =========================
PURPLE = "#bb86fc"          # main accent
PURPLE_SOFT = "#d7b7ff"     # lighter accent
BG_MAIN = "#14102a"
BG_AX = "#100c22"
GRID_COL = (0.73, 0.52, 0.99, 0.18)  # rgba-like
TEXT_COL = "#ffffff"
TICK_COL = (1, 1, 1, 0.75)


# ----------------------------
# Glow Button (real glow effect on hover)
# ----------------------------
class GlowButton(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)
        self._glow = QGraphicsDropShadowEffect(self)
        self._glow.setBlurRadius(0)
        self._glow.setOffset(0, 0)
        self._glow.setColor(QColor(PURPLE))
        self.setGraphicsEffect(self._glow)

    def enterEvent(self, event):
        # subtle tech glow
        self._glow.setBlurRadius(18)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._glow.setBlurRadius(0)
        super().leaveEvent(event)


# ----------------------------
# Matplotlib canvas (Purple Theme)
# ----------------------------
def style_axes_purple(ax):
    ax.set_facecolor(BG_AX)

    # spines
    for s in ax.spines.values():
        s.set_color((1, 1, 1, 0.18))

    # ticks/labels
    ax.tick_params(colors=TICK_COL)
    ax.xaxis.label.set_color(TICK_COL)
    ax.yaxis.label.set_color(TICK_COL)
    ax.title.set_color(PURPLE_SOFT)

    # grid
    ax.grid(True, alpha=0.18)

def apply_matplotlib_global_purple():
    matplotlib.rcParams["figure.facecolor"] = BG_MAIN
    matplotlib.rcParams["axes.facecolor"] = BG_AX
    matplotlib.rcParams["savefig.facecolor"] = BG_MAIN
    matplotlib.rcParams["text.color"] = TEXT_COL
    matplotlib.rcParams["axes.labelcolor"] = TEXT_COL
    matplotlib.rcParams["xtick.color"] = TEXT_COL
    matplotlib.rcParams["ytick.color"] = TEXT_COL
    matplotlib.rcParams["axes.edgecolor"] = (1, 1, 1, 0.18)
    matplotlib.rcParams["grid.color"] = GRID_COL
    matplotlib.rcParams["grid.alpha"] = 0.18
    matplotlib.rcParams["axes.titlecolor"] = PURPLE_SOFT
    matplotlib.rcParams["font.size"] = 10

apply_matplotlib_global_purple()

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor(BG_MAIN)

        self.ax = fig.add_subplot(111)
        style_axes_purple(self.ax)

        super().__init__(fig)
        fig.tight_layout()

    def to_png_bytes(self, dpi=140):
        buf = io.BytesIO()
        self.figure.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
        buf.seek(0)
        return buf


# ----------------------------
# DSP: Image Processing
# ----------------------------
def to_gray(img_bgr: np.ndarray) -> np.ndarray:
    if img_bgr is None:
        return None
    if len(img_bgr.shape) == 2:
        return img_bgr
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

def apply_median_filter(gray: np.ndarray, ksize: int) -> np.ndarray:
    k = max(3, int(ksize) | 1)
    return cv2.medianBlur(gray, k)

def apply_gaussian_filter(gray: np.ndarray, ksize: int, sigma: float) -> np.ndarray:
    k = max(3, int(ksize) | 1)
    return cv2.GaussianBlur(gray, (k, k), sigmaX=sigma)

def apply_sobel(gray: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    mag = np.uint8(np.clip(mag / (mag.max() + 1e-9) * 255, 0, 255))
    return mag

def apply_canny(gray: np.ndarray, t1: int, t2: int) -> np.ndarray:
    return cv2.Canny(gray, threshold1=t1, threshold2=t2)

def apply_hist_equalization(gray: np.ndarray) -> np.ndarray:
    return cv2.equalizeHist(gray)


# ----------------------------
# DSP: Speech Filtering
# ----------------------------
def read_audio(path: str):
    x, fs = sf.read(path)
    if x.ndim > 1:
        x = np.mean(x, axis=1)
    return x.astype(np.float32), int(fs)

def normalize_audio(x: np.ndarray) -> np.ndarray:
    m = np.max(np.abs(x)) + 1e-9
    return (x / m).astype(np.float32)

def butter_filter(
    x: np.ndarray,
    fs: int,
    ftype: str,
    cutoff_hz: float,
    order: int = 6,
    band_low_hz: float = None,
    band_high_hz: float = None
) -> np.ndarray:
    nyq = fs / 2.0

    if ftype == "lowpass":
        cutoff = np.clip(cutoff_hz / nyq, 1e-6, 0.999999)
        b, a = signal.butter(order, cutoff, btype="low")

    elif ftype == "highpass":
        cutoff = np.clip(cutoff_hz / nyq, 1e-6, 0.999999)
        b, a = signal.butter(order, cutoff, btype="high")

    elif ftype == "bandpass":
        if band_low_hz is None or band_high_hz is None:
            raise ValueError("Bandpass requires band_low_hz and band_high_hz")

        low = np.clip(band_low_hz / nyq, 1e-6, 0.999999)
        high = np.clip(band_high_hz / nyq, 1e-6, 0.999999)
        if high <= low:
            high = min(0.999999, low + 0.01)

        b, a = signal.butter(order, [low, high], btype="band")

    else:
        raise ValueError("Unknown filter type")

    y = signal.filtfilt(b, a, x)  # zero-phase
    return y.astype(np.float32)


# ----------------------------
# Main Window
# ----------------------------
class DSPPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PROJECT_TITLE} | {COURSE_NAME} — {INSTRUCTOR_NAME}")
        self.setMinimumSize(1400, 820)

        if os.path.exists(APP_ICON_ICO):
            self.setWindowIcon(QIcon(APP_ICON_ICO))

        self.img_bgr = None
        self.img_gray = None
        self.img_out = None
        self.img_path = None

        self.audio_path = None
        self.x = None
        self.fs = None
        self.y = None

        self.live_timer = QTimer()
        self.live_timer.setSingleShot(True)
        self.live_timer.timeout.connect(lambda: self.apply_image_method(silent=True))

        self._build_ui()
        self._build_menu_toolbar()
        self._build_statusbar()
        self.log("Ready ✅ Load an image or a WAV file to start.")

    # ---------- UI ----------
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        main = QVBoxLayout(root)
        main.setContentsMargins(12, 12, 12, 12)
        main.setSpacing(12)

        header = QLabel(
            f"""
            <div style="font-size:21px; font-weight:750; color:#d7b7ff;">
                {PROJECT_TITLE}
            </div>

            <div style="margin-top:6px; font-size:13px; color:rgba(255,255,255,0.92);">
                {COURSE_NAME}
                <span style="
                    background: rgba(187,134,252,0.22);
                    border: 1px solid rgba(187,134,252,0.55);
                    padding: 3px 10px;
                    border-radius: 999px;
                    margin-left: 10px;
                    color: #f2e9ff;
                    font-weight: 600;
                ">
                    Supervisor: {INSTRUCTOR_NAME}
                </span>
            </div>

            <div style="font-size:12px; color:rgba(255,255,255,0.78); margin-top:6px;">
                {INSTITUTE_NAME}
            </div>

            <div style="font-size:12px; color:rgba(255,255,255,0.70); margin-top:4px;">
                {GROUP_INFO}
            </div>
            """
        )
        header.setStyleSheet("""
            QLabel {
                padding: 18px;
                border-radius: 18px;
                background-color: rgba(255,255,255,0.06);
                border: 1px solid rgba(187,134,252,0.22);
            }
        """)
        main.addWidget(header)

        splitter = QSplitter(Qt.Horizontal)

        self.tabs = QTabWidget()
        self.tab_image = QWidget()
        self.tab_audio = QWidget()
        self.tabs.addTab(self.tab_image, "🖼 Image")
        self.tabs.addTab(self.tab_audio, "🎧 Audio")
        splitter.addWidget(self.tabs)

        right = QWidget()
        rp = QVBoxLayout(right)
        rp.setContentsMargins(8, 8, 8, 8)
        rp.setSpacing(12)

        img_group = QGroupBox("Image Viewer — Input vs Output")
        iv = QHBoxLayout(img_group)
        self.lbl_img_in = QLabel("Load an image to preview it here.")
        self.lbl_img_out = QLabel("Processed output will appear here.")
        for lab in (self.lbl_img_in, self.lbl_img_out):
            lab.setAlignment(Qt.AlignCenter)
            lab.setMinimumHeight(300)
            lab.setStyleSheet("""
                QLabel{
                    border: 1px solid rgba(255,255,255,0.14);
                    border-radius: 16px;
                    padding: 10px;
                    background: rgba(0,0,0,0.18);
                    color: rgba(255,255,255,0.92);
                }
            """)
        iv.addWidget(self.lbl_img_in, 1)
        iv.addWidget(self.lbl_img_out, 1)

        aud_group = QGroupBox("Audio Viewer — Waveform & Spectrogram")
        ag = QGridLayout(aud_group)
        ag.setContentsMargins(10, 10, 10, 10)

        self.canvas_wave_in = MplCanvas(width=5, height=2.3)
        self.canvas_wave_out = MplCanvas(width=5, height=2.3)
        self.canvas_spec_in = MplCanvas(width=10, height=2.2)
        self.canvas_spec_out = MplCanvas(width=10, height=2.2)

        self.canvas_wave_in.ax.set_title("Input Waveform")
        self.canvas_wave_out.ax.set_title("Output Waveform")
        self.canvas_spec_in.ax.set_title("Spectrogram (Input)")
        self.canvas_spec_out.ax.set_title("Spectrogram (Output)")

        ag.addWidget(self.canvas_wave_in, 0, 0)
        ag.addWidget(self.canvas_wave_out, 0, 1)
        ag.addWidget(self.canvas_spec_in, 1, 0)
        ag.addWidget(self.canvas_spec_out, 1, 1)

        rp.addWidget(img_group, 2)
        rp.addWidget(aud_group, 2)

        splitter.addWidget(right)
        splitter.setSizes([470, 930])

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(150)

        main.addWidget(splitter, 1)
        main.addWidget(self.log_box, 0)

        self._build_image_tab()
        self._build_audio_tab()

    def _btn(self, text: str) -> GlowButton:
        b = GlowButton(text)
        b.setMinimumHeight(44)
        return b

    def _btn_small(self, text: str) -> GlowButton:
        b = GlowButton(text)
        b.setMinimumHeight(38)
        return b

    def _build_image_tab(self):
        layout = QVBoxLayout(self.tab_image)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        row = QHBoxLayout()
        self.btn_load_img = self._btn("Load Image")
        self.btn_apply_img = self._btn("Apply")
        self.btn_save_img = self._btn("Save Output")
        self.btn_reset_img = self._btn("Reset")
        row.addWidget(self.btn_load_img)
        row.addWidget(self.btn_apply_img)
        row.addWidget(self.btn_save_img)
        row.addWidget(self.btn_reset_img)
        layout.addLayout(row)

        preset_row = QHBoxLayout()
        self.btn_soft = self._btn_small("Soft Denoise")
        self.btn_strong = self._btn_small("Strong Denoise")
        self.btn_edges = self._btn_small("Edge Highlight")
        preset_row.addWidget(self.btn_soft)
        preset_row.addWidget(self.btn_strong)
        preset_row.addWidget(self.btn_edges)
        layout.addLayout(preset_row)

        self.cmb_img_method = QComboBox()
        self.cmb_img_method.addItems([
            "Noise Reduction — Median Filter",
            "Noise Reduction — Gaussian Filter",
            "Edge Detection — Sobel",
            "Edge Detection — Canny",
            "Contrast Enhancement — Histogram Equalization"
        ])
        layout.addWidget(self._card("Method", self.cmb_img_method))

        live_row = QHBoxLayout()
        self.btn_live = GlowButton("Live Update: ON ✅")
        self.btn_live.setCheckable(True)
        self.btn_live.setChecked(True)
        self.btn_live.clicked.connect(self._toggle_live)
        self.btn_live.setMinimumHeight(38)
        live_row.addWidget(self.btn_live)
        layout.addLayout(live_row)

        self.sld_img_ksize = QSlider(Qt.Horizontal)
        self.sld_img_ksize.setMinimum(3)
        self.sld_img_ksize.setMaximum(31)
        self.sld_img_ksize.setValue(7)
        self.lbl_img_ksize = QLabel("Kernel Size: 7")

        self.sld_gauss_sigma = QSlider(Qt.Horizontal)
        self.sld_gauss_sigma.setMinimum(1)
        self.sld_gauss_sigma.setMaximum(50)
        self.sld_gauss_sigma.setValue(10)
        self.lbl_gauss_sigma = QLabel("Gaussian Sigma: 1.0")

        self.sld_canny_t1 = QSlider(Qt.Horizontal)
        self.sld_canny_t1.setMinimum(0)
        self.sld_canny_t1.setMaximum(255)
        self.sld_canny_t1.setValue(60)
        self.lbl_canny_t1 = QLabel("Canny T1: 60")

        self.sld_canny_t2 = QSlider(Qt.Horizontal)
        self.sld_canny_t2.setMinimum(0)
        self.sld_canny_t2.setMaximum(255)
        self.sld_canny_t2.setValue(150)
        self.lbl_canny_t2 = QLabel("Canny T2: 150")

        params = QWidget()
        g = QGridLayout(params)
        g.setContentsMargins(0, 0, 0, 0)
        g.setHorizontalSpacing(12)
        g.setVerticalSpacing(10)

        g.addWidget(self.lbl_img_ksize, 0, 0)
        g.addWidget(self.sld_img_ksize, 0, 1)
        g.addWidget(self.lbl_gauss_sigma, 1, 0)
        g.addWidget(self.sld_gauss_sigma, 1, 1)
        g.addWidget(self.lbl_canny_t1, 2, 0)
        g.addWidget(self.sld_canny_t1, 2, 1)
        g.addWidget(self.lbl_canny_t2, 3, 0)
        g.addWidget(self.sld_canny_t2, 3, 1)

        layout.addWidget(self._card("Parameters", params))
        layout.addStretch(1)

        self.btn_load_img.clicked.connect(self.load_image)
        self.btn_apply_img.clicked.connect(lambda: self.apply_image_method(silent=False))
        self.btn_reset_img.clicked.connect(self.reset_image)
        self.btn_save_img.clicked.connect(self.save_image)

        self.sld_img_ksize.valueChanged.connect(self._sync_img_labels)
        self.sld_gauss_sigma.valueChanged.connect(self._sync_img_labels)
        self.sld_canny_t1.valueChanged.connect(self._sync_img_labels)
        self.sld_canny_t2.valueChanged.connect(self._sync_img_labels)

        for sld in (self.sld_img_ksize, self.sld_gauss_sigma, self.sld_canny_t1, self.sld_canny_t2):
            sld.valueChanged.connect(self._schedule_live_update)

        self.cmb_img_method.currentTextChanged.connect(self._sync_img_param_visibility)
        self.cmb_img_method.currentTextChanged.connect(self._schedule_live_update)

        self.btn_soft.clicked.connect(lambda: self._apply_preset("soft"))
        self.btn_strong.clicked.connect(lambda: self._apply_preset("strong"))
        self.btn_edges.clicked.connect(lambda: self._apply_preset("edges"))

        self._sync_img_labels()
        self._sync_img_param_visibility()

    def _build_audio_tab(self):
        layout = QVBoxLayout(self.tab_audio)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        row = QHBoxLayout()
        self.btn_load_audio = self._btn("Load WAV")
        self.btn_apply_audio = self._btn("Apply Filter")
        self.btn_save_audio = self._btn("Save Output WAV")
        row.addWidget(self.btn_load_audio)
        row.addWidget(self.btn_apply_audio)
        row.addWidget(self.btn_save_audio)
        layout.addLayout(row)

        play_row = QHBoxLayout()
        self.btn_play_in = self._btn_small("▶ Play Input")
        self.btn_play_out = self._btn_small("▶ Play Output")
        self.btn_stop = self._btn_small("■ Stop")
        self.btn_play_in.setEnabled(False)
        self.btn_play_out.setEnabled(False)
        self.btn_stop.setEnabled(False)
        play_row.addWidget(self.btn_play_in)
        play_row.addWidget(self.btn_play_out)
        play_row.addWidget(self.btn_stop)
        layout.addLayout(play_row)

        preset_row = QHBoxLayout()
        self.btn_speech = self._btn_small("Speech Noise Removal")
        self.btn_hum = self._btn_small("Remove 50Hz Hum")
        preset_row.addWidget(self.btn_speech)
        preset_row.addWidget(self.btn_hum)
        layout.addLayout(preset_row)

        self.cmb_audio_method = QComboBox()
        self.cmb_audio_method.addItems([
            "Low-Pass Filter (Noise Reduction)",
            "High-Pass Filter (Remove Low-Freq Hum)",
            "Band-Pass Filter (Keep Frequency Band)"
        ])
        layout.addWidget(self._card("Filter Type", self.cmb_audio_method))

        self.sld_cutoff = QSlider(Qt.Horizontal)
        self.sld_cutoff.setMinimum(50)
        self.sld_cutoff.setMaximum(8000)
        self.sld_cutoff.setValue(1200)
        self.lbl_cutoff = QLabel("Cutoff Frequency: 1200 Hz")

        self.sld_band_low = QSlider(Qt.Horizontal)
        self.sld_band_low.setMinimum(50)
        self.sld_band_low.setMaximum(8000)
        self.sld_band_low.setValue(300)
        self.lbl_band_low = QLabel("Band Low: 300 Hz")

        self.sld_band_high = QSlider(Qt.Horizontal)
        self.sld_band_high.setMinimum(50)
        self.sld_band_high.setMaximum(8000)
        self.sld_band_high.setValue(3000)
        self.lbl_band_high = QLabel("Band High: 3000 Hz")

        self.sld_order = QSlider(Qt.Horizontal)
        self.sld_order.setMinimum(2)
        self.sld_order.setMaximum(10)
        self.sld_order.setValue(6)
        self.lbl_order = QLabel("Filter Order: 6")

        params = QWidget()
        g = QGridLayout(params)
        g.setContentsMargins(0, 0, 0, 0)
        g.setHorizontalSpacing(12)
        g.setVerticalSpacing(10)

        g.addWidget(self.lbl_cutoff, 0, 0)
        g.addWidget(self.sld_cutoff, 0, 1)

        g.addWidget(self.lbl_band_low, 1, 0)
        g.addWidget(self.sld_band_low, 1, 1)

        g.addWidget(self.lbl_band_high, 2, 0)
        g.addWidget(self.sld_band_high, 2, 1)

        g.addWidget(self.lbl_order, 3, 0)
        g.addWidget(self.sld_order, 3, 1)

        layout.addWidget(self._card("Parameters", params))

        self.btn_export_pdf = self._btn("Export PDF Report")
        self.btn_export_pdf.setMinimumHeight(46)
        layout.addWidget(self.btn_export_pdf)

        layout.addStretch(1)

        self.btn_load_audio.clicked.connect(self.load_audio)
        self.btn_apply_audio.clicked.connect(self.apply_audio_filter)
        self.btn_save_audio.clicked.connect(self.save_audio)

        self.btn_play_in.clicked.connect(self.play_input_audio)
        self.btn_play_out.clicked.connect(self.play_output_audio)
        self.btn_stop.clicked.connect(self.stop_audio)

        self.btn_export_pdf.clicked.connect(self.export_pdf_report)

        self.sld_cutoff.valueChanged.connect(self._sync_audio_labels)
        self.sld_band_low.valueChanged.connect(self._sync_audio_labels)
        self.sld_band_high.valueChanged.connect(self._sync_audio_labels)
        self.sld_order.valueChanged.connect(self._sync_audio_labels)

        self.btn_speech.clicked.connect(lambda: self._audio_preset("speech"))
        self.btn_hum.clicked.connect(lambda: self._audio_preset("hum"))

        self.cmb_audio_method.currentTextChanged.connect(self._sync_audio_param_visibility)

        self._sync_audio_labels()
        self._sync_audio_param_visibility()

    def _card(self, title: str, widget: QWidget) -> QWidget:
        box = QGroupBox(title)
        v = QVBoxLayout(box)
        v.setContentsMargins(10, 10, 10, 10)
        v.addWidget(widget)
        return box

    # ---------- Menu / Toolbar ----------
    def _build_menu_toolbar(self):
        act_open_img = QAction("Open Image", self)
        act_open_img.triggered.connect(self.load_image)
        act_open_audio = QAction("Open WAV", self)
        act_open_audio.triggered.connect(self.load_audio)

        act_save_img = QAction("Save Output Image", self)
        act_save_img.triggered.connect(self.save_image)
        act_save_audio = QAction("Save Output WAV", self)
        act_save_audio.triggered.connect(self.save_audio)

        act_pdf = QAction("Export PDF Report", self)
        act_pdf.triggered.connect(self.export_pdf_report)

        act_exit = QAction("Exit", self)
        act_exit.triggered.connect(self.close)

        m = self.menuBar()
        file_menu = m.addMenu("File")
        file_menu.addAction(act_open_img)
        file_menu.addAction(act_open_audio)
        file_menu.addSeparator()
        file_menu.addAction(act_save_img)
        file_menu.addAction(act_save_audio)
        file_menu.addSeparator()
        file_menu.addAction(act_pdf)
        file_menu.addSeparator()
        file_menu.addAction(act_exit)

        help_menu = m.addMenu("Help")
        act_about = QAction("About", self)
        act_about.triggered.connect(lambda: self.info(
            f"{PROJECT_TITLE}\n\n"
            f"Institute: {INSTITUTE_NAME}\n"
            f"Course: {COURSE_NAME}\n"
            f"Supervisor: {INSTRUCTOR_NAME}\n"
            f"{GROUP_INFO}\n"
            f"{UNIVERSITY_INFO}\n"
            f"Version: {VERSION}\n\n"
            "Features:\n"
            "- Image DSP: Median / Gaussian / Sobel / Canny / Histogram EQ\n"
            "- Audio DSP: Butterworth LP/HP/BP (zero-phase) + Spectrogram\n"
            "- Playback (Input/Output), Live Update\n"
            "- Auto PDF Report Export\n"
        ))
        help_menu.addAction(act_about)

        tb = QToolBar("Main")
        tb.setIconSize(QSize(18, 18))
        self.addToolBar(tb)
        tb.addAction(act_open_img)
        tb.addAction(act_open_audio)
        tb.addSeparator()
        tb.addAction(act_save_img)
        tb.addAction(act_save_audio)
        tb.addSeparator()
        tb.addAction(act_pdf)

    def _build_statusbar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.statusBar().showMessage(
            f"{INSTITUTE_NAME} | {COURSE_NAME} | Supervisor: {INSTRUCTOR_NAME} | {VERSION}"
        )

    # ---------- UX helpers ----------
    def log(self, msg: str):
        self.log_box.append(msg)

    def error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)
        self.log(f"❌ {msg}")

    def info(self, msg: str):
        QMessageBox.information(self, "Info", msg)
        self.log(f"ℹ️ {msg}")

    # ---------- Pixmap ----------
    def _set_pixmap(self, label: QLabel, img_gray: np.ndarray):
        if img_gray is None:
            return
        if len(img_gray.shape) == 2:
            h, w = img_gray.shape
            qimg = QImage(img_gray.data, w, h, w, QImage.Format_Grayscale8)
        else:
            h, w, _ = img_gray.shape
            rgb = cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)
            qimg = QImage(rgb.data, w, h, 3*w, QImage.Format_RGB888)

        pix = QPixmap.fromImage(qimg)
        label.setPixmap(pix.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.img_gray is not None:
            self._set_pixmap(self.lbl_img_in, self.img_gray)
        if self.img_out is not None:
            self._set_pixmap(self.lbl_img_out, self.img_out)

    # ---------- Live Update ----------
    def _toggle_live(self):
        self.btn_live.setText("Live Update: ON ✅" if self.btn_live.isChecked() else "Live Update: OFF")
        if self.btn_live.isChecked():
            self._schedule_live_update()

    def _schedule_live_update(self):
        if not self.btn_live.isChecked():
            return
        if self.img_gray is None:
            return
        self.live_timer.start(180)

    # ---------- Image ----------
    def _sync_img_labels(self):
        k = int(self.sld_img_ksize.value()) | 1
        self.lbl_img_ksize.setText(f"Kernel Size: {k}")
        sigma = self.sld_gauss_sigma.value() / 10.0
        self.lbl_gauss_sigma.setText(f"Gaussian Sigma: {sigma:.1f}")

        t1 = int(self.sld_canny_t1.value())
        t2 = int(self.sld_canny_t2.value())
        if t2 <= t1:
            t2 = t1 + 1
            self.sld_canny_t2.setValue(t2)
        self.lbl_canny_t1.setText(f"Canny T1: {t1}")
        self.lbl_canny_t2.setText(f"Canny T2: {t2}")

    def _sync_img_param_visibility(self):
        method = self.cmb_img_method.currentText()
        show_ksize = ("Median" in method) or ("Gaussian" in method)
        show_sigma = ("Gaussian" in method)
        show_canny = ("Canny" in method)

        self.lbl_img_ksize.setVisible(show_ksize)
        self.sld_img_ksize.setVisible(show_ksize)
        self.lbl_gauss_sigma.setVisible(show_sigma)
        self.sld_gauss_sigma.setVisible(show_sigma)
        self.lbl_canny_t1.setVisible(show_canny)
        self.sld_canny_t1.setVisible(show_canny)
        self.lbl_canny_t2.setVisible(show_canny)
        self.sld_canny_t2.setVisible(show_canny)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            self.error("Failed to load image.")
            return

        self.img_path = path
        self.img_bgr = img
        self.img_gray = to_gray(img)
        self.img_out = None

        self._set_pixmap(self.lbl_img_in, self.img_gray)
        self.lbl_img_out.setPixmap(QPixmap())
        self.lbl_img_out.setText("Processed output will appear here.")
        self.log(f"🖼 Loaded image: {path}")
        self._schedule_live_update()

    def apply_image_method(self, silent=False):
        if self.img_gray is None:
            if not silent:
                self.error("Load an image first.")
            return

        method = self.cmb_img_method.currentText()
        k = int(self.sld_img_ksize.value()) | 1
        sigma = self.sld_gauss_sigma.value() / 10.0
        t1 = int(self.sld_canny_t1.value())
        t2 = int(self.sld_canny_t2.value())

        try:
            if "Median" in method:
                out = apply_median_filter(self.img_gray, k)
            elif "Gaussian" in method:
                out = apply_gaussian_filter(self.img_gray, k, sigma)
            elif "Sobel" in method:
                out = apply_sobel(self.img_gray)
            elif "Canny" in method:
                out = apply_canny(self.img_gray, t1, t2)
            elif "Histogram" in method:
                out = apply_hist_equalization(self.img_gray)
            else:
                return
        except Exception as e:
            if not silent:
                self.error(f"Image processing failed:\n{e}")
            return

        self.img_out = out
        self._set_pixmap(self.lbl_img_out, self.img_out)
        if not silent:
            self.log(f"✅ Image processed: {method}")

    def reset_image(self):
        if self.img_gray is None:
            return
        self.img_out = None
        self.lbl_img_out.setPixmap(QPixmap())
        self.lbl_img_out.setText("Processed output will appear here.")
        self.log("↩️ Image reset")

    def save_image(self):
        if self.img_out is None:
            self.error("No processed image to save. Apply a method first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Output Image", "processed.png", "PNG (*.png);;JPG (*.jpg)")
        if not path:
            return
        try:
            cv2.imwrite(path, self.img_out)
            self.log(f"💾 Saved processed image: {path}")
        except Exception as e:
            self.error(f"Failed to save image:\n{e}")

    def _apply_preset(self, mode):
        if self.img_gray is None:
            self.error("Load an image first.")
            return
        if mode == "soft":
            self.cmb_img_method.setCurrentText("Noise Reduction — Gaussian Filter")
            self.sld_img_ksize.setValue(7)
            self.sld_gauss_sigma.setValue(10)
        elif mode == "strong":
            self.cmb_img_method.setCurrentText("Noise Reduction — Median Filter")
            self.sld_img_ksize.setValue(15)
        elif mode == "edges":
            self.cmb_img_method.setCurrentText("Edge Detection — Canny")
            self.sld_canny_t1.setValue(60)
            self.sld_canny_t2.setValue(160)
        self.apply_image_method()

    # ---------- Audio ----------
    def _sync_audio_labels(self):
        self.lbl_cutoff.setText(f"Cutoff Frequency: {self.sld_cutoff.value()} Hz")

        low = int(self.sld_band_low.value())
        high = int(self.sld_band_high.value())
        if high <= low:
            high = low + 50
            if high > self.sld_band_high.maximum():
                high = self.sld_band_high.maximum()
                low = max(self.sld_band_low.minimum(), high - 50)
                self.sld_band_low.setValue(low)
            self.sld_band_high.setValue(high)

        self.lbl_band_low.setText(f"Band Low: {low} Hz")
        self.lbl_band_high.setText(f"Band High: {high} Hz")

        self.lbl_order.setText(f"Filter Order: {self.sld_order.value()}")

    def _sync_audio_param_visibility(self):
        method = self.cmb_audio_method.currentText()
        is_band = "Band-Pass" in method

        self.lbl_cutoff.setVisible(not is_band)
        self.sld_cutoff.setVisible(not is_band)

        self.lbl_band_low.setVisible(is_band)
        self.sld_band_low.setVisible(is_band)
        self.lbl_band_high.setVisible(is_band)
        self.sld_band_high.setVisible(is_band)

    def load_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select WAV Audio", "", "WAV Files (*.wav)")
        if not path:
            return
        try:
            x, fs = read_audio(path)
            self.audio_path = path
            self.x = normalize_audio(x)
            self.fs = fs
            self.y = None
            self.plot_audio()

            self.btn_play_in.setEnabled(True)
            self.btn_play_out.setEnabled(False)
            self.btn_stop.setEnabled(True)

            self.log(f"🎧 Loaded WAV: {path} | fs={fs} Hz | duration={len(self.x)/fs:.2f}s")
        except Exception as e:
            self.error(f"Failed to read audio:\n{e}")

    def apply_audio_filter(self):
        if self.x is None:
            self.error("Load a WAV file first.")
            return

        order = int(self.sld_order.value())
        method = self.cmb_audio_method.currentText()

        try:
            if "Low-Pass" in method:
                cutoff = float(self.sld_cutoff.value())
                y = butter_filter(self.x, self.fs, "lowpass", cutoff, order)

            elif "High-Pass" in method:
                cutoff = float(self.sld_cutoff.value())
                y = butter_filter(self.x, self.fs, "highpass", cutoff, order)

            else:
                low = float(self.sld_band_low.value())
                high = float(self.sld_band_high.value())
                y = butter_filter(self.x, self.fs, "bandpass", cutoff_hz=0.0, order=order,
                                  band_low_hz=low, band_high_hz=high)

            self.y = normalize_audio(y)
            self.plot_audio()
            self.btn_play_out.setEnabled(True)

            if "Band-Pass" in method:
                self.log(f"✅ Audio filtered: {method} | band={int(self.sld_band_low.value())}-{int(self.sld_band_high.value())}Hz | order={order}")
            else:
                self.log(f"✅ Audio filtered: {method} | cutoff={int(self.sld_cutoff.value())}Hz | order={order}")

        except Exception as e:
            self.error(f"Audio filtering failed:\n{e}")

    def save_audio(self):
        if self.y is None:
            self.error("No output audio to save. Apply a filter first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Output WAV", "output_filtered.wav", "WAV Files (*.wav)")
        if not path:
            return
        try:
            sf.write(path, self.y, self.fs)
            self.log(f"💾 Saved filtered WAV: {path}")
        except Exception as e:
            self.error(f"Failed to save audio:\n{e}")

    def play_input_audio(self):
        if self.x is None:
            self.error("Load WAV first.")
            return
        self.stop_audio()
        try:
            sd.play(self.x, self.fs)
            self.log("▶ Playing INPUT audio")
        except Exception as e:
            self.error(f"Audio play failed:\n{e}")

    def play_output_audio(self):
        if self.y is None:
            self.error("Apply filter first to generate output audio.")
            return
        self.stop_audio()
        try:
            sd.play(self.y, self.fs)
            self.log("▶ Playing OUTPUT audio")
        except Exception as e:
            self.error(f"Audio play failed:\n{e}")

    def stop_audio(self):
        try:
            sd.stop()
            self.log("■ Stop audio")
        except Exception:
            pass

    def _audio_preset(self, mode):
        if self.x is None:
            self.error("Load WAV first.")
            return
        if mode == "speech":
            self.cmb_audio_method.setCurrentText("Low-Pass Filter (Noise Reduction)")
            self.sld_cutoff.setValue(3000)
            self.sld_order.setValue(6)
        elif mode == "hum":
            self.cmb_audio_method.setCurrentText("High-Pass Filter (Remove Low-Freq Hum)")
            self.sld_cutoff.setValue(100)
            self.sld_order.setValue(6)
        self.apply_audio_filter()

    def plot_audio(self):
        # Input waveform
        self.canvas_wave_in.ax.clear()
        style_axes_purple(self.canvas_wave_in.ax)
        self.canvas_wave_in.ax.set_title("Input Waveform")
        if self.x is not None:
            t = np.arange(len(self.x)) / self.fs
            self.canvas_wave_in.ax.plot(t, self.x, color=PURPLE, linewidth=1.2)
            self.canvas_wave_in.ax.set_xlabel("Time (s)")
            self.canvas_wave_in.ax.set_ylabel("Amp")
        self.canvas_wave_in.draw()

        # Output waveform
        self.canvas_wave_out.ax.clear()
        style_axes_purple(self.canvas_wave_out.ax)
        self.canvas_wave_out.ax.set_title("Output Waveform")
        if self.y is not None:
            t = np.arange(len(self.y)) / self.fs
            self.canvas_wave_out.ax.plot(t, self.y, color=PURPLE, linewidth=1.2)
            self.canvas_wave_out.ax.set_xlabel("Time (s)")
            self.canvas_wave_out.ax.set_ylabel("Amp")
        else:
            self.canvas_wave_out.ax.text(0.5, 0.5, "Apply a filter to see output",
                                         ha="center", va="center", color=PURPLE_SOFT)
        self.canvas_wave_out.draw()

        # Spectrogram input
        self.canvas_spec_in.ax.clear()
        style_axes_purple(self.canvas_spec_in.ax)
        self.canvas_spec_in.ax.set_title("Spectrogram (Input)")
        if self.x is not None:
            f, tt, Sxx = signal.spectrogram(self.x, self.fs, nperseg=1024, noverlap=512)
            self.canvas_spec_in.ax.pcolormesh(
                tt, f, 10*np.log10(Sxx + 1e-12),
                shading="gouraud",
                cmap="Purples"   # ✅ purple spectrogram
            )
            self.canvas_spec_in.ax.set_ylabel("Hz")
            self.canvas_spec_in.ax.set_xlabel("Time (s)")
            self.canvas_spec_in.ax.set_ylim(0, min(8000, self.fs/2))
        self.canvas_spec_in.draw()

        # Spectrogram output
        self.canvas_spec_out.ax.clear()
        style_axes_purple(self.canvas_spec_out.ax)
        self.canvas_spec_out.ax.set_title("Spectrogram (Output)")
        if self.y is not None:
            f, tt, Sxx = signal.spectrogram(self.y, self.fs, nperseg=1024, noverlap=512)
            self.canvas_spec_out.ax.pcolormesh(
                tt, f, 10*np.log10(Sxx + 1e-12),
                shading="gouraud",
                cmap="Purples"   # ✅ purple spectrogram
            )
            self.canvas_spec_out.ax.set_ylabel("Hz")
            self.canvas_spec_out.ax.set_xlabel("Time (s)")
            self.canvas_spec_out.ax.set_ylim(0, min(8000, self.fs/2))
        else:
            self.canvas_spec_out.ax.text(0.5, 0.5, "No output yet",
                                         ha="center", va="center", color=PURPLE_SOFT)
        self.canvas_spec_out.draw()

    # ---------- PDF Export ----------
    def export_pdf_report(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF Report", "DSP_Report.pdf", "PDF (*.pdf)")
        if not path:
            return

        img_method = self.cmb_img_method.currentText()
        k = int(self.sld_img_ksize.value()) | 1
        sigma = self.sld_gauss_sigma.value() / 10.0
        t1 = int(self.sld_canny_t1.value())
        t2 = int(self.sld_canny_t2.value())

        aud_method = self.cmb_audio_method.currentText()
        cutoff = int(self.sld_cutoff.value())
        order = int(self.sld_order.value())
        band_low = int(self.sld_band_low.value())
        band_high = int(self.sld_band_high.value())

        try:
            c = pdf_canvas.Canvas(path, pagesize=A4)
            W, H = A4

            def title(txt, y):
                c.setFont("Helvetica-Bold", 16)
                c.drawString(40, y, txt)

            def line(txt, y):
                c.setFont("Helvetica", 11)
                c.drawString(40, y, txt)

            def add_img(img_reader, x, y, w, h):
                c.drawImage(img_reader, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')

            title(f"{PROJECT_TITLE} — Report", H - 50)
            c.setFont("Helvetica", 10)
            c.drawString(40, H - 70, f"Institute: {INSTITUTE_NAME}")
            c.drawString(40, H - 84, f"Course: {COURSE_NAME} | Supervisor: {INSTRUCTOR_NAME}")
            c.drawString(40, H - 98, GROUP_INFO)
            c.drawString(40, H - 112, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            c.line(40, H - 120, W - 40, H - 120)

            y = H - 145
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, "1) Current Settings")
            y -= 18
            line(f"Image Method: {img_method}", y); y -= 14
            line(f"Kernel Size: {k} | Gaussian Sigma: {sigma:.1f} | Canny T1/T2: {t1}/{t2}", y); y -= 14

            if "Band-Pass" in aud_method:
                line(f"Audio Filter: {aud_method} | Band: {band_low}-{band_high} Hz | Order: {order}", y); y -= 18
            else:
                line(f"Audio Filter: {aud_method} | Cutoff: {cutoff} Hz | Order: {order}", y); y -= 18

            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, "2) Image Results"); y -= 10

            if self.img_gray is not None:
                inp = ImageReader(self._np_to_png_bytes(self.img_gray))
                out = ImageReader(self._np_to_png_bytes(self.img_out)) if self.img_out is not None else None
                add_img(inp, 40, y - 220, 250, 200)
                c.setFont("Helvetica", 10)
                c.drawString(40, y - 235, "Input Image")
                if out:
                    add_img(out, 320, y - 220, 250, 200)
                    c.drawString(320, y - 235, "Output Image")
            else:
                line("No image loaded.", y)

            c.showPage()

            title("Audio Results — Waveforms & Spectrograms", H - 50)
            c.setFont("Helvetica", 10)
            c.drawString(40, H - 70, f"Institute: {INSTITUTE_NAME}")
            c.drawString(40, H - 84, f"Course: {COURSE_NAME} | Supervisor: {INSTRUCTOR_NAME}")
            c.drawString(40, H - 98, f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            c.line(40, H - 106, W - 40, H - 106)

            y = H - 130
            if self.x is not None:
                w1 = ImageReader(self.canvas_wave_in.to_png_bytes())
                w2 = ImageReader(self.canvas_wave_out.to_png_bytes())
                s1 = ImageReader(self.canvas_spec_in.to_png_bytes())
                s2 = ImageReader(self.canvas_spec_out.to_png_bytes())

                add_img(w1, 40, y - 170, 250, 150)
                add_img(w2, 320, y - 170, 250, 150)
                c.setFont("Helvetica", 10)
                c.drawString(40, y - 185, "Input Waveform")
                c.drawString(320, y - 185, "Output Waveform")
                y -= 220

                add_img(s1, 40, y - 180, 250, 160)
                add_img(s2, 320, y - 180, 250, 160)
                c.drawString(40, y - 195, "Spectrogram (Input)")
                c.drawString(320, y - 195, "Spectrogram (Output)")
            else:
                line("No audio loaded.", y)

            c.save()
            self.log(f"📄 PDF exported: {path}")
            self.info(f"PDF saved:\n{path}")

        except Exception as e:
            self.error(f"PDF export failed:\n{e}")

    def _np_to_png_bytes(self, img_gray: np.ndarray):
        if img_gray is None:
            return io.BytesIO()
        ok, enc = cv2.imencode(".png", img_gray)
        if not ok:
            return io.BytesIO()
        return io.BytesIO(enc.tobytes())


# ----------------------------
# Splash Screen
# ----------------------------
def build_splash_pixmap(w=900, h=520):
    pix = QPixmap(w, h)
    pix.fill(QColor(BG_MAIN))

    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    p.setBrush(QColor(187, 134, 252, 45))
    p.setPen(Qt.NoPen)
    p.drawRoundedRect(40, 50, w-80, h-150, 28, 28)

    p.setPen(QColor(PURPLE_SOFT))
    p.setFont(QFont("Segoe UI", 26, QFont.Bold))
    p.drawText(70, 130, PROJECT_TITLE)

    p.setPen(QColor("#ffffff"))
    p.setFont(QFont("Segoe UI", 13, QFont.Medium))
    p.drawText(70, 175, f"{COURSE_NAME} — Supervisor: {INSTRUCTOR_NAME}")

    p.setPen(QColor(255, 255, 255, 210))
    p.setFont(QFont("Segoe UI", 12))
    p.drawText(70, 210, INSTITUTE_NAME)

    p.setPen(QColor(255, 255, 255, 185))
    p.drawText(70, 240, GROUP_INFO)

    p.setPen(QColor(187, 134, 252, 230))
    p.setFont(QFont("Consolas", 12))
    p.drawText(70, h-85, "Loading modules... Please wait")

    p.end()
    return pix


def apply_purple_theme(app: QApplication):
    app.setStyleSheet("""
    QMainWindow {
        background-color: #14102a;
        color: #ffffff;
        font-family: Segoe UI;
    }

    QWidget {
        color: rgba(255,255,255,0.92);
    }

    QGroupBox {
        border: 1px solid rgba(187, 134, 252, 0.30);
        border-radius: 16px;
        margin-top: 14px;
        font-size: 13px;
        background: rgba(0,0,0,0.10);
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 8px;
        color: #e6d6ff;
        font-weight: 700;
    }

    QPushButton {
        background-color: rgba(25,18,45,0.92);
        border: 1px solid rgba(230,214,255,0.55);
        border-radius: 12px;
        padding: 9px 14px;
        color: #ffffff;
        font-weight: 700;
    }
    QPushButton:hover {
        background-color: rgba(44,31,79,0.95);
        border: 1px solid rgba(187,134,252,0.95);
    }
    QPushButton:pressed {
        background-color: rgba(58,42,106,0.95);
    }

    QComboBox {
        background-color: rgba(18,12,36,0.92);
        border: 1px solid rgba(230,214,255,0.35);
        border-radius: 10px;
        padding: 7px;
    }
    QComboBox QAbstractItemView {
        background-color: rgba(18,12,36,1);
        selection-background-color: rgba(187,134,252,0.95);
        selection-color: #0b0620;
        color: #ffffff;
    }

    QSlider::groove:horizontal {
        height: 7px;
        background: rgba(255,255,255,0.16);
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #bb86fc;
        width: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }

    QTabWidget::pane {
        border: 1px solid rgba(187,134,252,0.30);
        border-radius: 14px;
        background: rgba(0,0,0,0.10);
    }
    QTabBar::tab {
        background: rgba(18,12,36,0.92);
        color: rgba(255,255,255,0.92);
        padding: 9px 16px;
        border-radius: 10px;
        margin: 4px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    QTabBar::tab:selected {
        background: rgba(187,134,252,0.95);
        color: #130a2a;
        border: 1px solid rgba(255,255,255,0.20);
        font-weight: 800;
    }

    QStatusBar {
        background-color: rgba(18,12,36,0.95);
        color: #e6d6ff;
        padding: 7px;
        border-top: 1px solid rgba(255,255,255,0.10);
    }

    QTextEdit {
        background-color: rgba(18,12,36,0.92);
        border-radius: 14px;
        padding: 10px;
        font-family: Consolas;
        color: rgba(255,255,255,0.95);
        border: 1px solid rgba(255,255,255,0.10);
    }
    """)


def main():
    app = QApplication(sys.argv)

    if os.path.exists(APP_ICON_ICO):
        app.setWindowIcon(QIcon(APP_ICON_ICO))

    apply_purple_theme(app)

    splash = QSplashScreen(build_splash_pixmap())
    splash.show()
    app.processEvents()

    w = DSPPro()
    w.show()

    splash.finish(w)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
