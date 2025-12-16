# confirmation.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

class ConfirmationWindow(QWidget):
    def __init__(self, part_name, part_image=None, parent=None, flow_manager=None):
        super().__init__()
        uic.loadUi("confirmation.ui", self)
        
        self.part_name = part_name
        self.part_image = part_image
        self.parent_window = parent
        self.flow_manager = flow_manager
        self.setWindowTitle("Part Confirmation / حصہ کی تصدیق")
        
        if hasattr(self, "selectedPartButton"):
            self.selectedPartButton.setText(part_name)
            
            # Make non-clickable but keep visual appearance
            self.selectedPartButton.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            
            # Show image if exists
            if part_image:
                icon = QIcon(part_image)
                self.selectedPartButton.setIcon(icon)
            else:
                print(f"No image found for {part_name}")
        
        self.nextButton.clicked.connect(self.go_next)
        self.backButton.clicked.connect(self.go_back)
    
    def showEvent(self, event):
        """Override showEvent to set icon size after widget is displayed."""
        super().showEvent(event)
        
        # Set icon size once the button has its proper size
        if hasattr(self, "selectedPartButton") and self.part_image:
            button_size = self.selectedPartButton.size()
            self.selectedPartButton.setIconSize(button_size)
    
    def go_next(self):
        print(f"➡️ Next pressed for {self.part_name}")
        if self.flow_manager:
            self.flow_manager.show_top_scan(self.part_name,self.part_image)
        else:
            print("⚠️ No FlowManager found.")
    
    def go_back(self):
        print("⬅️ Going back to part selection.")
        if self.flow_manager:
            self.flow_manager.return_to_part_selection()