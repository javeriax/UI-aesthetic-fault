# main.py
import sys
from PyQt6.QtWidgets import QApplication
from part_selection import PartSelectorApp
from flow_manager import FlowManager

def main():
    app = QApplication(sys.argv)
    # create part selection screen
    selector = PartSelectorApp()
    selector.showMaximized()

    # attach flowmanager to selector
    flow_manager = FlowManager(parent_app=selector)
    selector.flow_manager = flow_manager  #  Give selector access

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
