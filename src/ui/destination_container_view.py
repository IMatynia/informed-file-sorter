from PySide6 import QtCore
from PySide6.QtWidgets import QHBoxLayout, QWidget


class DestinationContainerLayout(QWidget):
    folders_dropped = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setLayout(QHBoxLayout(self))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.folders_dropped.emit(links)
        else:
            event.ignore()
