import os.path

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget
from src.ui.ui_destination_folder import Ui_destinationFolder


class DestinationFolderView(QWidget):
    onClickWPath = QtCore.Signal(str)
    onRemoveWPath = QtCore.Signal(str)

    def __init__(self, folder_path: str, highlight: bool = False):
        super().__init__()
        self._ui = Ui_destinationFolder()
        self._ui.setupUi(self)
        self._folder_path = folder_path

        self._ui.btAdd.clicked.connect(self.on_add)
        self._ui.btRemove.clicked.connect(self.on_remove)

        if highlight:
            self._ui.btAdd.setDisabled(True)
            self._ui.lbName.setText(f" > {os.path.basename(folder_path)} < ")
        else:
            self._ui.lbName.setText(os.path.basename(folder_path))

    def on_add(self):
        self.onClickWPath.emit(self._folder_path)

    def on_remove(self):
        self.onRemoveWPath.emit(self._folder_path)
