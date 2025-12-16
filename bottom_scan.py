import os
import re
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
from app_state import ScreenState, set_screen_state

class BottomScanWindow(QWidget):
    def __init__(self, part_name, part_image, parent=None, flow_manager=None):
        super().__init__(parent)
        uic.loadUi("bottom_scan.ui", self)

        self.part_name = part_name
        self.part_image = part_image
        self.flow_manager = flow_manager
        # Use concise window title; header contains bilingual label
        self.setWindowTitle(f"Bottom Scan - {part_name}")

        # -----------------------------
        # Progress bar setup
        # -----------------------------
        self.progress_value = 0
        self.current_progress_step = 0
        self.segment_count = 4
        self.increment = 100 // self.segment_count
        if hasattr(self, "scanProgressBar"):
            self.scanProgressBar.setValue(self.progress_value)

        # -----------------------------
        # Optional buttons
        # -----------------------------
        if hasattr(self, "scanButton"):
            self.scanButton.clicked.connect(self.start_scan)
        if hasattr(self, "nextButton"):
            self.nextButton.clicked.connect(self.finish_scan)

        # -----------------------------
        # Scan label
        # -----------------------------
        if hasattr(self, "scanLabel"):
            # Build a single bilingual line with one slash and clean Urdu phrasing.
            # If `part_name` contains a bilingual form like 'Part 9 / حصہ 9',
            # strip the Urdu part for the English text to avoid duplication.
            english_name = self.part_name.split('/') [0].strip()
            m = re.search(r"\d+", self.part_name)
            part_id = m.group(0) if m else english_name
            english = f"Processing... Scanning bottom of {english_name}"
            urdu = f"کاروائی جاری ہے... حصہ {part_id} کے نچلے حصے کی اسکیننگ"
            self.scanLabel.setText(f"{english} / {urdu}")
            self.scanLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scanLabel.setVisible(True)
            self.scanLabel.repaint()  # Force immediate redraw

        self.show()

    # -----------------------------
    # Keyboard shortcut for progress
    # -----------------------------
    def keyPressEvent(self, event):
        """Handle Right Arrow key to advance progress."""
        if event.key() == Qt.Key.Key_Right:
            self.advance_progress()

    # -----------------------------
    # Advance progress step
    # -----------------------------
    def advance_progress(self):
        """Advance progress bar and update application state step-by-step."""
        if self.current_progress_step < self.segment_count:
            self.current_progress_step += 1
            self.progress_value = self.current_progress_step * self.increment
            if hasattr(self, "scanProgressBar"):
                self.scanProgressBar.setValue(self.progress_value)

            # Update global screen state
            if self.current_progress_step == 1:
                set_screen_state(ScreenState.PROGRESS1)
            elif self.current_progress_step == 2:
                set_screen_state(ScreenState.PROGRESS2)
            elif self.current_progress_step == 3:
                set_screen_state(ScreenState.PROGRESS3)
            elif self.current_progress_step == 4:
                set_screen_state(ScreenState.PROGRESS4)

            if self.progress_value >= 100:
                self.finish_scan()

    # -----------------------------
    # Scan control flow
    # -----------------------------
    def start_scan(self):
        print(f"Starting bottom scan for {self.part_name}...")

    def finish_scan(self):
        print(f" Bottom scan complete for {self.part_name}")
        if self.flow_manager:
            self.flow_manager.show_scan_completed(self.part_name, self.part_image)
        self.close()
