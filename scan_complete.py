# scan_complete.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
from app_state import AppState


class ScanCompletedWindow(QWidget):
    def __init__(self, part_name, parent=None):
        super().__init__(parent)
        uic.loadUi("scan_complete.ui", self)
        self.part_name = part_name
        self.parent_window = parent

        self.setWindowTitle("Scan Completed")

        # ✅ Update labels safely
        if hasattr(self, "statusLabel"):
            self.statusLabel.setText(f"✅ Scanning for '{part_name}' completed successfully!")

        if hasattr(self, "partLabel"):
            self.partLabel.setText(f"Part: {part_name}")

        # ✅ Connect “Go to Results” button
        if hasattr(self, "resultsButton"):
            self.resultsButton.clicked.connect(self.go_to_results)
        else:
            print("⚠️ No 'resultsButton' found in UI — check UI object name.")

        # ✅ Update app state
        if self.parent_window:
            self.parent_window.set_state(AppState.SCAN_COMPLETE_SCREEN)

        # ✅ Keep ResultsScreen reference so it doesn’t get deleted
        self.results_screen = None

    def go_to_results(self):
        """Open the Results screen after scan completion."""
        print("➡️ Opening Results screen...")

        from results import ResultsScreen  # import here to avoid circular import

        self.results_screen = ResultsScreen(self.part_name, parent=self.parent_window)
        self.results_screen.showMaximized()

        # ✅ Hide current screen
        self.hide()
