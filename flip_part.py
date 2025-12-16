from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal

class FlipInstructionScreen(QWidget):
    next_clicked = pyqtSignal(str)  # emit part name

    def __init__(self, part_name, part_image, parent=None, flow_manager=None):
        super().__init__()
        uic.loadUi("flip_part.ui", self)

        self.flow_manager = flow_manager
        self.part_name = part_name  # store current part
        self.part_image = part_image
        self.setWindowTitle("Flip the Part / حصہ کو پلٹ دیں")

        if hasattr(self, "nextButton"):
            self.nextButton.clicked.connect(self.next_pressed)

    def next_pressed(self):
        print(f"↩️ User flipped the part and pressed Next for {self.part_name}")
        if self.flow_manager:
            self.flow_manager.show_bottom_scan(self.part_name, self.part_image)
        else:
            print("⚠️ No FlowManager found.")
