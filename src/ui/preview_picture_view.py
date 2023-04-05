import logging
import os.path

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout


class PreviewPictureView(QLabel):
    folders_dropped = QtCore.Signal(list)

    def __init__(self, zoom_level:float = 1.0):
        super().__init__()
        self.setAcceptDrops(True)
        self._image_base_size = QSize(400, 400)
        self._zoom_level = zoom_level
        self._current_file_path = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self._finalize_ui()

    def _finalize_ui(self):
        self.setText("DROP FOLDER TO EXPLORE")
        self._on_preview_filename = QLabel()
        self._on_preview_filename.setStyleSheet("background: #555555")
        self._on_preview_filename.setContentsMargins(5, 5, 5, 5)
        self._on_preview_filename.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self._on_preview_filename)
        self._on_preview_filename.hide()

    def zoom_in(self):
        self._zoom_level *= 1.2

    def mouseDoubleClickEvent(self, event) -> None:
        if self._current_file_path:
            os.system(f"xdg-open \"{self._current_file_path}\"")

    def zoom_out(self):
        self._zoom_level /= 1.2


    def get_zoom(self):
        return self._zoom_level

    def no_files_found(self):
        self.setText("NO MATCHING FILES FOUND")
        self._on_preview_filename.hide()

    def set_preview(self, file_path: str):
        self._current_file_path = file_path
        path, filename = os.path.split(file_path)
        name, extension = os.path.splitext(filename)

        if extension[1:] in QImageReader.supportedImageFormats():
            pix_map = QPixmap(file_path).scaled(self._zoom_level * self._image_base_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                QtCore.Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pix_map)
            self._on_preview_filename.setText(os.path.basename(self._current_file_path))
            self._on_preview_filename.show()
        else:
            self.setText("No preview available!")
            self._on_preview_filename.setText(os.path.basename(self._current_file_path))
            self._on_preview_filename.show()

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
