# app_state.py
"""
Manages the global state of the application, including both the current
UI screen/flow state and the user's authentication state (role, login status).
This file serves as the single source of truth for the application's status.
"""
from enum import Enum, auto

# ==========================================================
# SCREEN FLOW STATE
# ==========================================================
class ScreenState(Enum):
    """Enumeration for the current screen being displayed."""
    PART_SELECTION = auto()
    PART_CONFIRMATION = auto()
    LOGIN_SCREEN_OPENED = auto()
    TOP_SCAN = auto()
    # For Progress indicator:
    PROGRESS1 = auto()
    PROGRESS2 = auto()
    PROGRESS3 = auto()
    PROGRESS4 = auto()
    # --- End of New States ---
    FLIP_PART = auto()
    BOTTOM_SCAN = auto()
    SCAN_COMPLETE = auto()
    RESULTS = auto()

# ==========================================================
# AUTHENTICATION STATE
# ==========================================================
class Role(Enum):
    """Enumeration for user roles."""
    OPERATOR = auto()
    SUPERVISOR = auto()
    QUALITY = auto()

class LoginState(Enum):
    """Enumeration for login status."""
    LOGGED_OUT = auto()
    LOGGED_IN = auto()

# ==========================================================
# GLOBAL STATE VARIABLES
# ==========================================================
# Initialize the application to its default starting state.
current_screen_state = ScreenState.PART_SELECTION
current_login_state = LoginState.LOGGED_OUT
current_user_role = Role.OPERATOR
logged_in_username = None

# ==========================================================
# STATE MANAGEMENT FUNCTIONS
# ==========================================================
def set_screen_state(new_state: ScreenState):
    """Updates the global screen state."""
    global current_screen_state
    if current_screen_state != new_state:
        print(f"--- Screen state changed from {current_screen_state.name} to {new_state.name} ---")
        current_screen_state = new_state

def set_auth_state(login_state: LoginState, user_role: Role = Role.OPERATOR, username: str = None):
    """Updates the global authentication state."""
    global current_login_state, current_user_role, logged_in_username
    current_login_state = login_state
    current_user_role = user_role
    logged_in_username = username
    print(f"--- Auth state changed: {login_state.name}, Role: {user_role.name}, User: {username or 'None'} ---")