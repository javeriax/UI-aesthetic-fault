# results.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
import random
import app_state
from final_summary import FinalSummaryScreen


class ResultsScreen(QWidget):
    def __init__(self, part_name,part_image, parent=None, flow_manager=None):
        super().__init__(parent)
        uic.loadUi("results.ui", self)

        self.part_name = part_name
        self.part_image = part_image  # Placeholder for selected part image
        self.flow_manager = flow_manager
        self.setWindowTitle(f"Results / نتائج - {part_name}")

        # next button
        if hasattr(self, "nextButton"):
            self.nextButton.clicked.connect(self.go_to_summary)
        else:
            print("⚠️ No 'nextButton' found in results.ui")
        # Supervisor button 
        if hasattr(self, "supervisorButton"):
            self.supervisorButton.clicked.connect(self.supervisor_override_clicked)
            self.supervisorButton.hide()  # hidden by default
        else:
            print("⚠️ No 'supervisorButton' found in results.ui")

        # Will populate images when the widget is shown so label sizes are available
        self._results_populated = False

    def showEvent(self, event):
        """Populate images once the widget is shown so label sizes are valid."""
        super().showEvent(event)
        if not getattr(self, '_results_populated', False):
            self.populate_results()
            self._results_populated = True

    def update_supervisor_button_visibility(self, show: bool):
        """Show/hide supervisor button based on role AND bad part condition."""
        if (app_state.current_login_state == app_state.LoginState.LOGGED_IN and
            app_state.current_user_role == app_state.Role.SUPERVISOR and
            show):
            self.supervisorButton.show()
        else:
            self.supervisorButton.hide()
        print(f"[ResultsScreen] Supervisor button visible? {self.supervisorButton.isVisible()}")

    def supervisor_override_clicked(self):
        print("Supervisor Override clicked for", self.part_name)
        # Add your supervisor functionality here

    def populate_results(self):
        """Populate images and status. Show supervisor button if bad parts detected."""
        image_labels = [
            getattr(self, f"image_{r}_{c}")
            for r in range(3)
            for c in range(6)
            if hasattr(self, f"image_{r}_{c}")
        ]
        #show error_images if there is an error and show goodpart if no error:
        error_images = ["img_error.jpg", "img_err_2.jpg"]
        good_image = ["45_upright_good_front.jpg", "angle_0_side1_good.jpg","angle_0_good_back.jpg","45_upright_side1_good.jpg","angle_0_good.jpg"]
        
        num_labels = len(image_labels)
        num_bad = random.randint(0, min(4, num_labels))
        bad_indexes = random.sample(range(num_labels), num_bad)
        #find erro percentage:
        self.error_percentage = round((num_bad / num_labels) * 100, 2) if num_labels > 0 else 0
        print(f"[ResultsScreen] Error Percentage = {self.error_percentage}%")

        for i, label in enumerate(image_labels):
             # Select the correct image based on GOOD/BAD
            if i in bad_indexes:
                img_file = random.choice(error_images)
            else:
                img_file = random.choice(good_image)
            # Load original pixmap and scale to the label's actual size so images
            # appear visually consistent with the part selection screen.
            pix = QPixmap(img_file)
            if not pix.isNull():
                target_size = label.size()
                if target_size.width() <= 0 or target_size.height() <= 0:
                      target_size = QSize(300, 240)
                pix = pix.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                )
                label.setPixmap(pix)
            else:
                label.clear()

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                "border: 3px solid #d32f2f; border-radius: 8px;" if i in bad_indexes
                else "border: 3px solid #388e3c; border-radius: 8px;"
            )

        # Update status label
        show_supervisor = False
        self.is_part_good = True # Assume good unless bad indexes found
        if hasattr(self, "statusLabel"):
            if bad_indexes:
                self.statusLabel.setText(f"🔴 BAD PART! {len(bad_indexes)} alerts detected / 🔴 خراب حصہ! {len(bad_indexes)} الرٹس کا پتہ چلا")
                self.statusLabel.setStyleSheet("color: #c62828; font-size: 18pt; font-weight: bold;")
                show_supervisor = True
                self.is_part_good = False
            else:
                self.statusLabel.setText("🟢 GOOD PART! All regions OK / 🟢 اچھا حصہ! تمام علاقے ٹھیک ہیں")
                self.statusLabel.setStyleSheet("color: #2e7d32; font-size: 18pt; font-weight: bold;")
                show_supervisor = False
                self.is_part_good = True
        if hasattr(self, "errorPercentLabel"):
            # Single bilingual line with one slash and the percentage shown once.
            # Use Urdu 'غلطی کا فیصد' and force LTR for the numeric value so '%'
            # remains after the number in RTL layouts.
            self.errorPercentLabel.setText(
                f"Error percentage / غلطی کا فیصد: \u200E{self.error_percentage}%"
            )
            self.errorPercentLabel.setStyleSheet("font-size: 16pt; font-weight: bold; color: #444;")

        # Show supervisor button only if role is supervisor AND bad parts detected
        self.update_supervisor_button_visibility(show_supervisor)

    def go_to_summary(self):
        """Passes results data to the final summary screen and displays it."""
        print("➡️ Navigating to Final Summary Screen...")
        if self.flow_manager:
            # Create the new summary screen instance
            self.summary_screen = FinalSummaryScreen(
                part_name=self.part_name,
                part_image_file=self.part_image,
                is_good=self.is_part_good,
                error_percentage=self.error_percentage,
                flow_manager=self.flow_manager
            )
            self.summary_screen.showMaximized()
            self.hide() # Hide the detailed results screen
        else:
            print("Flow Manager not available.")