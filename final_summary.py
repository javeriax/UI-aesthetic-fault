# final_summary_screen.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QSize, QUrl


class FinalSummaryScreen(QWidget):
    """
    Shows the final, simplified GOOD/BAD status and part image.
    Provides the primary way to return to Part Selection.
    """

    def __init__(self, part_name, part_image_file, is_good, error_percentage, flow_manager=None, parent=None):
        super().__init__(parent)
        uic.loadUi("final_summary.ui", self)  # Load the new UI file

        self.flow_manager = flow_manager
        # Keep the window title stable and localized once (UI already provides a title)
        self.setWindowTitle("Part Summary / حصہ کا خلاصہ")
        
        # Connect the back button to the flow manager
        if hasattr(self, "backButton"):
            self.backButton.clicked.connect(self.return_to_selection)
        
        # Populate the summary details
        self.populate_summary(part_name, part_image_file, is_good, error_percentage)

    def populate_summary(self, part_name, part_image_file, is_good, error_percentage):
        """Sets the part info, status text, and colors."""

        # 1. Part Name Label
        # Show only the part number (no 'Part Name:' prefix)
        self.partNameLabel.setText(f"{part_name}")

        # 2. Part Image Label
        pix = QPixmap(part_image_file)
        if not pix.isNull():
            # Scale image down for the summary view
            target_size = QSize(250, 250)
            pix = pix.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.partImageLabel.setPixmap(pix)
        
        # 3. Status and Styling - keep English and Urdu single occurrences
        if is_good:
            status_text = "GOOD PART / اچھا حصہ"
            color_code = "#2e7d32"  # Green
        else:
            status_text = "BAD PART / برا حصہ"
            color_code = "#c62828"  # Red

        # Show error percentage once, English and Urdu separated by a single slash.
        # Use Urdu translation 'غلطی کا فیصد' and force LTR for the numeric value so
        # the percent sign appears after the number in mixed RTL/LTR text.
        detail_text = f"Error percentage / غلطی کا فیصد: \u200E{error_percentage}%"

        # Apply status text and styling
        self.finalStatusLabel.setText(status_text)
        self.finalStatusLabel.setStyleSheet(
            f"font-size: 36pt; font-weight: bold; padding: 20px; border-radius: 10px; "
            f"border: 5px solid {color_code}; color: {color_code}; background-color: #ffffff;"
        )

        self.resultDetailLabel.setText(detail_text)

    def return_to_selection(self):
        """Navigates back to the initial part selection screen."""
        print("⬅️ Returning to part selection screen from summary...")
        if self.flow_manager:
            self.flow_manager.return_to_part_selection()
        self.close()