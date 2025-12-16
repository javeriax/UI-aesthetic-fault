# auth.py
"""
Handles user authentication by verifying credentials against a dummy database.
In a real-world application, this module would interface with a secure
authentication service or database.
"""

# Dummy credentials for different user roles.
# Keys are usernames, values are dictionaries containing passwords and roles.
DUMMY_CREDENTIALS = {
    "supervisor": {
        "password": "123",
        "role": "supervisor"
    },
    "quality": {
        "password": "123",
        "role": "quality"
    }
}

def verify_credentials(username, password):
    """
    Verifies a username and password against the dummy credential store.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        str: The role of the user ('supervisor' or 'quality') if credentials
             are valid, otherwise None.
    """
    user_data = DUMMY_CREDENTIALS.get(username)
    if user_data and user_data["password"] == password:
        return user_data["role"]
    return None