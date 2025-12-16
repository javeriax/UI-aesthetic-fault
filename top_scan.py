# Simplify the scan label to a single bilingual line separated by one slash
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
import re
# --- MODIFIED: Import set_screen_state directly from app_state ---
from app_state import ScreenState, set_screen_state

class TopScanWindow(QWidget):
    def __init__(self, part_name, part_image, parent=None, flow_manager=None):
        super().__init__(parent)
        print(f"[TopScanWindow] Created for {part_name}")
        uic.loadUi("top_scan.ui", self)

        self.part_name = part_name
        self.flow_manager = flow_manager
        self.part_image = part_image
        # Use a concise window title; header contains bilingual label
        self.setWindowTitle(f"Top Scan - {part_name}")

        # --- Progress bar setup ---
        self.progress_value = 0
        self.current_progress_step = 0
        self.segment_count = 4
        self.increment = 100 // self.segment_count
        if hasattr(self, "scanProgressBar"):
            self.scanProgressBar.setValue(self.progress_value)

        # --- Optional buttons ---
        if hasattr(self, "scanButton"):
            self.scanButton.clicked.connect(self.start_scan)
        if hasattr(self, "nextButton"):
            self.nextButton.clicked.connect(self.finish_scan)

        # --- Optional label ---
        if hasattr(self, "scanLabel"):
            # Build a clear bilingual line with a single slash separator.
            # If `part_name` already contains a bilingual form like 'Part 9 / حصہ 9',
            # use only the English portion for the English text so the Urdu part isn't duplicated.
            english_name = part_name.split('/') [0].strip()
            m = re.search(r"\d+", part_name)
            part_id = m.group(0) if m else english_name
            english = f"Processing... Scanning top of {english_name}"
            # Include 'حصہ' before the numeric id for natural Urdu phrasing (e.g., 'حصہ 9')
            urdu = f"کاروائی جاری ہے... حصہ {part_id} کے اوپری حصے کی اسکیننگ"
            self.scanLabel.setText(f"{english} / {urdu}")
        self.show()

    # -------------------------------
    # Keyboard shortcut for progress
    # -------------------------------
    def keyPressEvent(self, event):
        """Handle Right Arrow key to advance progress."""
        if event.key() == Qt.Key.Key_Right:
            self.advance_progress()

    def advance_progress(self):
        """Advance progress bar and update application state step-by-step."""
        if self.current_progress_step < self.segment_count:
            self.current_progress_step += 1
            self.progress_value = self.current_progress_step * self.increment
            self.scanProgressBar.setValue(self.progress_value)

            # --- MODIFIED: Call the global set_screen_state function directly ---
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

    # -------------------------------
    # Scan control flow
    # -------------------------------
    def start_scan(self):
        print(f"🔍 Starting top scan for {self.part_name}...")

    def finish_scan(self):
        print(f"✅ Top scan complete for {self.part_name}")
        if self.flow_manager:
            self.flow_manager.show_flip_screen(self.part_name, self.part_image)
        self.close()