from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, Qt

class TopScanWindow(QWidget):
    finished = pyqtSignal(str)  # ✅ Signal emits part_name

    def __init__(self, part_name=None, parent=None):
        super().__init__(parent)
        uic.loadUi("top_scan.ui", self)

        self.part_name = part_name or "Selected Part"
        self.setWindowTitle(f"Top Scan: {self.part_name}")

        if hasattr(self, "scanLabel"):
            self.scanLabel.setText(f"Scanning Top of {self.part_name}...")

        self.progress_value = 0
        self.segment_count = 4
        self.increment = 100 // self.segment_count

        self.scanProgressBar.setValue(self.progress_value)

    def keyPressEvent(self, event):
        """Handle key press to advance progress."""
        if event.key() == Qt.Key.Key_Right:  # ✅ Correct for PyQt6
            self.advance_progress()

    def advance_progress(self):
        """Advance progress bar in segments when key is pressed."""
        if self.progress_value < 100:
            self.progress_value += self.increment
            self.scanProgressBar.setValue(self.progress_value)

            if self.progress_value >= 100:
                self.finish_scan()

    def finish_scan(self):
        print(f"✅ Top scan for {self.part_name} completed.")
        self.finished.emit(self.part_name)
        self.close()
