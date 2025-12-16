# scan_complete.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
# The old import is no longer needed, so we remove it:
# from app_state import AppState


class ScanCompletedWindow(QWidget):
    def __init__(self, part_name, part_image, parent=None, flow_manager=None):
        super().__init__(parent)
        uic.loadUi("scan_complete.ui", self)

        self.part_name = part_name
        self.part_image = part_image
        self.flow_manager = flow_manager
        self.setWindowTitle("Scan Completed / اسکین مکمل")

        if hasattr(self, "statusLabel"):
            self.statusLabel.setText(f"✅ Scanning for '{part_name}' completed successfully! / ✅ '{part_name}' کے لیے اسکیننگ کامیابی سے مکمل ہو گئی!")

        if hasattr(self, "partLabel"):
            self.partLabel.setText(f"Part: {part_name} / حصہ: {part_name}")

        if hasattr(self, "resultsButton"):
            self.resultsButton.clicked.connect(self.go_to_results)
        else:
            print("⚠️ No 'resultsButton' found in UI — check UI object name in Qt Designer.")


    def go_to_results(self):
        """Tell FlowManager to open the Results screen."""
        print(f"➡️ Opening Results screen for {self.part_name}")

        if self.flow_manager:
            # This correctly tells the FlowManager to handle the next step.
            # The FlowManager will also update the app_state.
            self.flow_manager.show_results(self.part_name, self.part_image)
        else:
            print("⚠️ FlowManager not found.")

        self.close()