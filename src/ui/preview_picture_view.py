import logging
import os.path

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtWidgets import QLabel, QSizePolicy


class PreviewPictureView(QLabel):
    fileDropped = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self._image_size = QSize(400, 400)
        self._current_file_path = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setText("DROP FOLDER TO EXPLORE")

    def zoom_in(self):
        self._image_size *= 1.2

    def mouseDoubleClickEvent(self, event) -> None:
        if self._current_file_path:
            os.system(f"xdg-open \"{self._current_file_path}\"")

    def zoom_out(self):
        self._image_size /= 1.2

    def set_preview(self, file_path: str):
        self._current_file_path = file_path
        path, filename = os.path.split(file_path)
        name, extension = os.path.splitext(filename)

        if extension[1:] in QImageReader.supportedImageFormats():
            pix_map = QPixmap(file_path).scaled(self._image_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                QtCore.Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pix_map)
        else:
            self.setText(file_path)

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
            self.fileDropped.emit(links)
        else:
            event.ignore()

    def no_signal(self):
        self.setText("NO MATCHING FILES FOUND")
