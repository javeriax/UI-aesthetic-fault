from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt
from imageloader import load_images_for_buttons
import app_state
from app_state import ScreenState
from login_dialog import LoginDialog

class PartSelectorApp(QWidget):
    """Main application window for part selection and login handling."""

    def __init__(self, flow_manager=None):
        super().__init__()
        uic.loadUi("part_selection.ui", self)

        self.flow_manager = flow_manager
        self.selected_part = None
        self.selected_image = None
        self.login_dialog = LoginDialog(self)

        # Configure window
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.showMaximized()

        # Load part images
        self.image_files = ["45_upright_good_front.jpg", "washing_machine.jpeg","angle_0_good_back.jpg","45_upright_side1_good.jpg","angle_0_good.jpg"]*4
        self.part_buttons = [
            getattr(self, f"partButton{i}") 
            for i in range(1, 21) 
            if hasattr(self, f"partButton{i}")
        ]
        load_images_for_buttons(self.part_buttons, self.image_files)

        # Map button → image path for later use in confirmation
        self.button_to_image = {}
        for i, button in enumerate(self.part_buttons):
            if i < len(self.image_files):
                self.button_to_image[button] = self.image_files[i]

        # Button connections
        self.selectButton.clicked.connect(self.confirm_selection)

        # Set initial screen state
        app_state.set_screen_state(ScreenState.PART_SELECTION)
        self.update_ui_for_auth_state()

    def update_ui_for_auth_state(self):
        """Updates login button and status label."""
        try:
            self.loginButton.clicked.disconnect()
        except TypeError:
            pass

        if app_state.current_login_state == app_state.LoginState.LOGGED_IN:
            self.loginButton.setText("Log Out / لاگ آوٹ")
            self.loginButton.setStyleSheet(
                "background-color: #F44336; color: white; font-size: 12pt; "
                "font-weight: bold; padding: 10px 20px; border-radius: 8px; border: none;"
            )
            self.loginButton.clicked.connect(self.logout_action)
            self.show_login_status(app_state.logged_in_username)
        else:
            self.loginButton.setText("Login / لاگ ان")
            self.loginButton.setStyleSheet("")
            self.loginButton.clicked.connect(self.login_action)
            self.hide_login_status()

    def confirm_selection(self):
        """Confirm selected part and continue."""
        selected_button = self.partButtonGroup.checkedButton()
        if selected_button:
            self.selected_part = selected_button.text()
            self.selected_image = self.button_to_image.get(selected_button, None)
            if self.flow_manager:
                # DON'T hide here - let flow_manager handle it after new window is shown
                self.flow_manager.start_flow(self.selected_part, self.selected_image)
        else:
            print("No part selected.")

    # Login/logout functions
    def login_action(self):
        app_state.set_screen_state(ScreenState.LOGIN_SCREEN_OPENED)
        self.login_dialog.reset_fields()
        result = self.login_dialog.exec()

        if result and self.login_dialog.user_role:
            app_state.set_auth_state(
                login_state=app_state.LoginState.LOGGED_IN,
                user_role=self.login_dialog.user_role,
                username=self.login_dialog.username
            )
        else:
            app_state.set_auth_state(app_state.LoginState.LOGGED_OUT)

        app_state.set_screen_state(ScreenState.PART_SELECTION)
        self.update_ui_for_auth_state()

    def logout_action(self):
        app_state.set_auth_state(app_state.LoginState.LOGGED_OUT)
        print("User logged out.")
        self.update_ui_for_auth_state()

    def show_login_status(self, username):
        if hasattr(self, "loginStatusLabel"):
            self.loginStatusLabel.setText(f"Logged in as: {username} / کے طور پر لاگ ان: {username}")
            self.loginStatusLabel.setStyleSheet(
                "font-size: 11pt; font-weight: bold; color: white; padding: 8px;"
            )
            self.loginStatusLabel.show()

    def hide_login_status(self):
        if hasattr(self, "loginStatusLabel"):
            self.loginStatusLabel.hide()