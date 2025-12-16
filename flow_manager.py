# flow_manager.py
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QApplication
import app_state
from app_state import ScreenState

class FlowManager(QObject):
    def __init__(self, parent_app=None):
        super().__init__()
        self.app = parent_app   # should be PartSelectorApp instance
        self.current_window = None
        self.current_part = None  # Track currently selected part
        print(f"[FlowManager] created!")

    def start_flow(self, part_name, part_image=None):
        print(f"[FlowManager] start_flow({part_name}, {part_image})")
        self.current_part = part_name
        self.show_confirmation(part_name, part_image)

    def show_confirmation(self, part_name, part_image=None):
        from confirmation import ConfirmationWindow
        app_state.set_screen_state(ScreenState.PART_CONFIRMATION)
        
        new_window = ConfirmationWindow(
            part_name=part_name,
            part_image=part_image,
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def show_top_scan(self, part_name, part_image):
        from top_scan import TopScanWindow
        app_state.set_screen_state(ScreenState.TOP_SCAN)
        self.current_part = part_name
        print(f"[FlowManager] show_top_scan called with part_name: {part_name}")
        
        new_window = TopScanWindow(
            part_name=part_name, 
            part_image=part_image,
            parent=None, 
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def show_flip_screen(self, part_name, part_image):
        from flip_part import FlipInstructionScreen
        app_state.set_screen_state(ScreenState.FLIP_PART)
        print(f"[FlowManager] show_flip_screen called with part_name: {part_name}")
        
        new_window = FlipInstructionScreen(
            part_name=part_name,
            part_image=part_image,
            parent=None,
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def show_bottom_scan(self, part_name, part_image):
        from bottom_scan import BottomScanWindow
        app_state.set_screen_state(ScreenState.BOTTOM_SCAN)
        print(f"[FlowManager] show_bottom_scan called with part_name: {part_name}")
        
        new_window = BottomScanWindow(
            part_name, 
            part_image=part_image, 
            parent=None, 
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def show_scan_completed(self, part_name, part_image):
        from scan_complete import ScanCompletedWindow
        app_state.set_screen_state(ScreenState.SCAN_COMPLETE)
        print(f"[FlowManager] show_scan_completed called with part_name: {part_name}")
        
        new_window = ScanCompletedWindow(
            part_name, 
            part_image=part_image, 
            parent=None, 
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def show_results(self, part_name, part_image):
        from results import ResultsScreen
        app_state.set_screen_state(ScreenState.RESULTS)
        print(f"[FlowManager] show_results called with part_name: {part_name}")
        
        new_window = ResultsScreen(
            part_name, 
            part_image=part_image, 
            parent=None, 
            flow_manager=self
        )
        self._transition_to_window(new_window)

    def return_to_part_selection(self):
        print("[FlowManager] return_to_part_selection()")
        app_state.set_screen_state(ScreenState.PART_SELECTION)
        
        if self.app:
            # Create new window and show it first
            self.app.showMaximized()
            self.app.raise_()
            self.app.activateWindow()
            
            # Process events to ensure new window is rendered
            QApplication.processEvents()
            
            # Then close the current window
            old_window = self.current_window
            self.current_window = None
            
            if old_window:
                old_window.close()
                old_window.deleteLater()

    def _transition_to_window(self, new_window):
        """
        Seamless transition: show new window, process events, then close old.
        """
        # Show and maximize the new window first
        new_window.showMaximized()
        new_window.raise_()
        new_window.activateWindow()
        
        # CRITICAL: Force Qt to process and render the new window immediately
        QApplication.processEvents()
        
        # Keep reference to old window
        old_window = self.current_window
        
        # Update current window reference
        self.current_window = new_window
        
        # Now close and cleanup the old window
        if old_window:
            old_window.close()
            old_window.deleteLater()
        
        # Hide the main app if it's still visible
        if self.app and self.app.isVisible():
            self.app.hide()

    def _close_current(self):
        """Legacy method - kept for compatibility but no longer used internally"""
        if self.current_window:
            try:
                self.current_window.close()
            except Exception:
                pass
            self.current_window = None