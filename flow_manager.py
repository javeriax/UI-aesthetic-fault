# flow_manager.py
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QApplication
import app_state
from app_state import ScreenState
from PyQt6.QtCore import Qt

class FlowManager(QObject):
    def __init__(self, parent_app=None):
        super().__init__()
        self.app = parent_app          # PartSelectorApp
        self.current_window = None
        self.current_part = None
        print("[FlowManager] created")

    # -------------------------
    # Flow entry
    # -------------------------
    def start_flow(self, part_name, part_image=None):
        self.current_part = part_name
        self.show_confirmation(part_name, part_image)

    # -------------------------
    # Screens
    # -------------------------
    def show_confirmation(self, part_name, part_image=None):
        from confirmation import ConfirmationWindow
        app_state.set_screen_state(ScreenState.PART_CONFIRMATION)

        self._transition(
            ConfirmationWindow(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    def show_top_scan(self, part_name, part_image):
        from top_scan import TopScanWindow
        app_state.set_screen_state(ScreenState.TOP_SCAN)

        self._transition(
            TopScanWindow(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    def show_flip_screen(self, part_name, part_image):
        from flip_part import FlipInstructionScreen
        app_state.set_screen_state(ScreenState.FLIP_PART)

        self._transition(
            FlipInstructionScreen(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    def show_bottom_scan(self, part_name, part_image):
        from bottom_scan import BottomScanWindow
        app_state.set_screen_state(ScreenState.BOTTOM_SCAN)

        self._transition(
            BottomScanWindow(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    def show_scan_completed(self, part_name, part_image):
        from scan_complete import ScanCompletedWindow
        app_state.set_screen_state(ScreenState.SCAN_COMPLETE)

        self._transition(
            ScanCompletedWindow(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    def show_results(self, part_name, part_image):
        from results import ResultsScreen
        app_state.set_screen_state(ScreenState.RESULTS)

        self._transition(
            ResultsScreen(
                part_name=part_name,
                part_image=part_image,
                flow_manager=self
            )
        )

    # -------------------------
    # Return to part selection
    # (already smooth – kept intact)
    # -------------------------
    def return_to_part_selection(self):
        app_state.set_screen_state(ScreenState.PART_SELECTION)

        if self.current_window:
            self.current_window.hide()

        if self.app:
            self.app.showMaximized()
            self.app.raise_()
            self.app.activateWindow()

        # Cleanup after UI stabilizes
        QTimer.singleShot(50, self._cleanup_current)

    # -------------------------
    # Core transition logic
    # -------------------------
    from PyQt6.QtCore import Qt

    def _transition(self, new_window):
        """
        Flicker-free transition:
        - Window is maximized BEFORE showing
        - Old window hidden immediately
        """

        # 1. Prepare window state BEFORE showing
        new_window.setWindowState(Qt.WindowState.WindowMaximized)

        # 2. Show ONCE
        new_window.show()
        new_window.raise_()
        new_window.activateWindow()

        # 3. Hide main app
        if self.app and self.app.isVisible():
            self.app.hide()

        # 4. Hide old window immediately
        old_window = self.current_window
        self.current_window = new_window

        if old_window:
            old_window.hide()
            QTimer.singleShot(50, old_window.deleteLater)


    # -------------------------
    # Cleanup helper
    # -------------------------
    def _cleanup_current(self):
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
            self.current_window = None
