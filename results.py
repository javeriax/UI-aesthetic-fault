from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import random
from app_state import AppState


class ResultsScreen(QWidget):
    def __init__(self, part_name, parent=None):
        super().__init__(parent)
        uic.loadUi("results.ui", self)

        self.part_name = part_name
        self.parent_window = parent  # ✅ Reference to PartSelectorApp
        self.setWindowTitle(f"Results - {part_name}")

        # Connect Back button
        if hasattr(self, "backButton"):
            self.backButton.clicked.connect(self.go_back)
        else:
            print("⚠️ No backButton found in results.ui")

        # Populate dummy scan results
        self.populate_results()

    # ---------------------------------------------------------
    # POPULATE RESULTS MATRIX (dummy system)
    # ---------------------------------------------------------
    def populate_results(self):
        image_labels = [getattr(self, f"image_{r}_{c}") for r in range(3) for c in range(4)]
        image_files = ["meow.jpeg", "image1.jpeg", "image2.jpeg"]

        # Randomly mark some cells as 'bad'
        bad_indexes = random.sample(range(12), random.randint(0, 5))

        for i, label in enumerate(image_labels):
            pixmap = QPixmap(random.choice(image_files)).scaled(
                150, 120, Qt.AspectRatioMode.KeepAspectRatio
            )
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Red border if bad, green if good
            label.setStyleSheet(
                "border: 3px solid #d32f2f; border-radius: 8px;"
                if i in bad_indexes
                else "border: 3px solid #388e3c; border-radius: 8px;"
            )

        # Update result label
        if bad_indexes:
            self.statusLabel.setText(f"🔴 BAD PART! {len(bad_indexes)} alerts detected")
            self.statusLabel.setStyleSheet(
                "color: #c62828; font-size: 18pt; font-weight: bold;"
            )
        else:
            self.statusLabel.setText("🟢 GOOD PART! All regions OK")
            self.statusLabel.setStyleSheet(
                "color: #2e7d32; font-size: 18pt; font-weight: bold;"
            )

    # ---------------------------------------------------------
    # BACK BUTTON → Return to Part Selection
    # ---------------------------------------------------------
    def go_back(self):
        print("⬅️ Returning to Part Selection screen...")

        # Close results window
        self.close()

        # ✅ Make sure we have a valid parent reference
        if not self.parent_window:
            print("⚠️ No parent window found — cannot go back.")
            return

        # ✅ Show parent window again
        self.parent_window.show()
        self.parent_window.showMaximized()
        self.parent_window.raise_()
        self.parent_window.activateWindow()

        # ✅ Restore correct app state (logged in or guest)
        if hasattr(self.parent_window, "login_dialog") and self.parent_window.login_dialog.is_logged_in:
            print("Restoring logged-in state...")
            self.parent_window.set_state(AppState.LOGIN_SUCCESS)
        else:
            print("Restoring guest state...")
            self.parent_window.set_state(AppState.PART_SELECTION_SCREEN)
