# app_state.py
from enum import Enum, auto

class AppState(Enum):
    PART_SELECTION_SCREEN = auto()
    SELECT_PRESSED = auto()
    LOGIN_SCREEN_OPEN = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_FAILED = auto()
    PART_CONFIRMATION_SCREEN = auto()
    NEXT_PRESSED = auto()
    TOP_SCAN_SCREEN = auto()
    FLIP_PART_SCREEN = auto()
    BOTTOM_SCAN_SCREEN = auto()
    SCAN_COMPLETE = auto()
    RESULTS_SCREEN = auto()