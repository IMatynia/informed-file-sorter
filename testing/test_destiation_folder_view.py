from PySide6.QtWidgets import QApplication

from src.ui.destination_folder_view import DestinationFolderView


def test_ui_styles():
    def reactant():
        print("Hello")

    app = QApplication()
    widget = DestinationFolderView("/test1/test2", True, 2)
    widget.onClickWPath.connect(reactant)
    widget.show()
    app.exec()
