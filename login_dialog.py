from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt

# Import the credential verifier and Role enum
from auth import verify_credentials
from app_state import Role

class LoginDialog(QDialog):
    """Dialog window for Supervisor/Quality Team login."""

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("login_dialog.ui", self)
        
        # These will be set upon successful login
        self.user_role = None
        self.username = None
        
        self.loginButton.clicked.connect(self.check_credentials)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        print("LoginDialog initialized.")

    def reset_fields(self):
        """Clears input fields and resets internal state."""
        self.usernameEdit.clear()
        self.passwordEdit.clear()
        self.user_role = None
        self.username = None
        print("LoginDialog fields reset.")

    def check_credentials(self):
        """
        Validates user input against the dummy credentials.
        On success, it sets the user's role and accepts the dialog.
        """
        username_input = self.usernameEdit.text().strip()
        password_input = self.passwordEdit.text().strip()

        # Verify credentials using the auth module
        role_str = verify_credentials(username_input, password_input)

        if role_str:
            # Convert the role string to a Role enum member
            if role_str == 'supervisor':
                self.user_role = Role.SUPERVISOR
            elif role_str == 'quality':
                self.user_role = Role.QUALITY
            
            self.username = username_input
            # ✅ Removed the Login Success / Welcome popup
            self.accept()  # Close the dialog with an Accepted status
        else:
            # Keep only the Invalid Login dialog
            QMessageBox.critical(self, "Login Failed / لاگ ان ناکام", "Invalid Username or Password. / غلط صارف نام یا پاس ورڈ۔")
            self.passwordEdit.clear()
            self.user_role = None
            self.username = None
