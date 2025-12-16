# flow_manager.py
from PyQt6.QtCore import QObject
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
        self._close_current()
        app_state.set_screen_state(ScreenState.PART_CONFIRMATION)
        self.current_window = ConfirmationWindow(
            part_name=part_name,
            part_image=part_image,
            flow_manager=self
        )
        self.current_window.showMaximized()

    def show_top_scan(self, part_name, part_image):
        from top_scan import TopScanWindow
        self._close_current()
        app_state.set_screen_state(ScreenState.TOP_SCAN)
        self.current_part = part_name  # Save selected part
        print(f"[FlowManager] show_top_scan called with part_name: {part_name}")
        self.current_window = TopScanWindow(
            part_name=part_name, 
            part_image=part_image,
            parent=None, 
            flow_manager=self
        )
        self.current_window.showMaximized()
        self.current_window.activateWindow()

    def show_flip_screen(self, part_name,part_image):
        from flip_part import FlipInstructionScreen
        self._close_current()
        app_state.set_screen_state(ScreenState.FLIP_PART)
        print(f"[FlowManager] show_flip_screen called with part_name: {part_name}")
        self.current_window = FlipInstructionScreen(
            part_name=part_name,  # pass the part_name
            part_image=part_image,
            parent=None,
            flow_manager=self
        )
        self.current_window.showMaximized()


    def show_bottom_scan(self, part_name,part_image):
        from bottom_scan import BottomScanWindow
        self._close_current()
        app_state.set_screen_state(ScreenState.BOTTOM_SCAN)
        print(f"[FlowManager] show_bottom_scan called with part_name: {part_name}")
        self.current_window = BottomScanWindow(part_name, part_image=part_image, parent=None, flow_manager=self)
        self.current_window.showMaximized()

    def show_scan_completed(self, part_name, part_image):
        from scan_complete import ScanCompletedWindow
        self._close_current()
        app_state.set_screen_state(ScreenState.SCAN_COMPLETE)
        print(f"[FlowManager] show_scan_completed called with part_name: {part_name}")
        self.current_window = ScanCompletedWindow(part_name, part_image=part_image, parent=None, flow_manager=self)
        self.current_window.showMaximized()

    def show_results(self, part_name, part_image):
        from results import ResultsScreen
        self._close_current()
        app_state.set_screen_state(ScreenState.RESULTS)
        print(f"[FlowManager] show_results called with part_name: {part_name}")
        self.current_window = ResultsScreen(part_name, part_image=part_image, parent=None, flow_manager=self)
        self.current_window.showMaximized()

    def return_to_part_selection(self):
        print("[FlowManager] return_to_part_selection()")
        self._close_current()
        app_state.set_screen_state(ScreenState.PART_SELECTION)
        if self.app:
            self.app.show()
            self.app.showMaximized()

    def _close_current(self):
        if self.current_window:
            try:
                self.current_window.close()
            except Exception:
                pass
            self.current_window = None
