from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, Qt

class BottomScanWindow(QWidget):
    scan_complete = pyqtSignal(str)

    def __init__(self, part_name, parent=None):
        super().__init__(parent)
        uic.loadUi("bottom_scan.ui", self)

        self.part_name = part_name
        self.setWindowTitle(f"Bottom Scan: {part_name}")

        if hasattr(self, "scanLabel"):
            self.scanLabel.setText(f"Scanning Bottom of {part_name}...")

        self.progress_value = 0
        self.segment_count = 4
        self.increment = 100 // self.segment_count

        self.scanProgressBar.setValue(self.progress_value)

    def keyPressEvent(self, event):
        """Handle key press to advance progress."""
        if event.key() == Qt.Key.Key_Right:  # ▶️ Forward arrow key (PyQt6 syntax)
            self.advance_progress()

    def advance_progress(self):
        """Advance progress bar in 4 segments."""
        if self.progress_value < 100:
            self.progress_value += self.increment
            self.scanProgressBar.setValue(self.progress_value)

            if self.progress_value >= 100:
                self.finish_scan()

    def finish_scan(self):
        print(f"✅ Bottom scan for {self.part_name} completed.")
        self.scan_complete.emit(self.part_name)
        self.close()
