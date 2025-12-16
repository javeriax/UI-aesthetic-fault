import os
from PyQt6.QtGui import QIcon

def load_images_for_buttons(buttons, image_files):
    """
    Assign images to given buttons.
    Only sets the icon; text stays as part name.
    
    :param buttons: List of QPushButton/QToolButton objects
    :param image_files: List of image file paths corresponding to buttons
    """
    for i, button in enumerate(buttons):
        if i >= len(image_files):
            break
        image_path = image_files[i]
        if os.path.exists(image_path):
            icon = QIcon(image_path)
            button.setIcon(icon)
            button.setIconSize(button.size())
