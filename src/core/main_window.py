import logging
import os

from PySide6 import QtGui, QtCore

from src.core.action_history import ActionHistory
from PySide6.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog
from src.core.file_moving_manager import FileMovingManager
from src.ui.destination_folder_view import DestinationFolderView
from src.ui.main_window_view import Ui_MainWindow
from src.ui.preview_picture_view import PreviewPictureView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._file_m_manager = FileMovingManager()
        self._current_file_index = 0

        self._finalize_ui()
        self._set_up_triggers()

    def _set_up_triggers(self):
        self._preview_image.fileDropped.connect(self.set_current_folder)
        self._ui.actionNext_file.triggered.connect(self._next_file)
        self._ui.actionPrevious_file.triggered.connect(self._prev_file)
        # self._ui.actionConfirm.triggered.connect(self._file_m_manager.apply_assignments)
        self._ui.actionZoom_in.triggered.connect(self.on_zoom_in)
        self._ui.actionZoom_out.triggered.connect(self.on_zoom_out)
        self._ui.actionDelete_file.triggered.connect(self.on_delete)
        self._ui.actionFilter.triggered.connect(self.on_change_filter)
        self._ui.actionOpen_new_destination.triggered.connect(self.on_add_destination)

    def _finalize_ui(self):
        self._preview_image = PreviewPictureView()
        self._ui.vbPreviewContainer.layout().addWidget(self._preview_image)

    def set_current_folder(self, folder_path):
        folder_path = folder_path[0]
        try:
            self._file_m_manager.set_current_source(folder_path)
        except NotADirectoryError:
            logging.info(f"{folder_path} is not a directory")
            return
        logging.info(f"New folder: {folder_path}")
        self._current_file_index = 0
        self._reload_all()

    def on_zoom_in(self):
        self._preview_image.zoom_in()
        if self._file_m_manager.get_n_of_source_files() > 0:
            self._reload_sources()

    def on_zoom_out(self):
        self._preview_image.zoom_out()
        if self._file_m_manager.get_n_of_source_files() > 0:
            self._reload_sources()

    def on_delete(self):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file_path = self._file_m_manager.get_file_on_index(self._current_file_index)
        res = QMessageBox.question(None, "Are you sure", f"Are you sure you want to delete {current_file_path}?")
        if res == QMessageBox.StandardButton.Yes:
            os.remove(current_file_path)
            logging.info(f"Deleted {current_file_path}")

    def on_add_destination(self):
        directory_path = QFileDialog.getExistingDirectory(None, "Add a destination")
        if directory_path != "":
            self._file_m_manager.add_destination(directory_path)
            self._reload_destinations()

    def on_change_filter(self):
        new_regex, succ = QInputDialog.getText(None, "Change filter", "Type in regex pattern to match path files",
                                               text=self._file_m_manager.get_regex_filter())
        if succ:
            self._file_m_manager.set_regex_filter(new_regex)
            self._file_m_manager.refresh_sources()
            self._current_file_index = 0
            self._reload_all()

    def on_delete_destination(self, folder_path: str):
        try:
            self._file_m_manager.remove_destination(folder_path)
        except Exception as e:
            logging.warning(e)
            QMessageBox.warning(None, "Warning", str(e))
            return
        self._reload_destinations()

    def on_assign_destination(self, folder_path: str):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file_path = self._file_m_manager.get_file_on_index(self._current_file_index)
        self._file_m_manager.add_assignment(current_file_path, folder_path)
        self._reload_destinations()

    def _reload_all(self):
        self._reload_sources()
        self._reload_destinations()

    def _reload_sources(self):
        if self._file_m_manager.get_n_of_source_files() > 0:
            current_file = self._file_m_manager.get_file_on_index(self._current_file_index)
            self._preview_image.set_preview(current_file)
        else:
            self._preview_image.no_signal()

    def _reload_destinations(self):
        if self._file_m_manager.get_n_of_source_files() > 0:
            current_file = self._file_m_manager.get_file_on_index(self._current_file_index)
            try:
                assigned_folder = self._file_m_manager.get_assignment(current_file)
            except KeyError:
                assigned_folder = ""
        else:
            assigned_folder = ""
        all_destinations = self._file_m_manager.get_all_destinations()

        for i in range(self._ui.hlDestinations.layout().count()):
            widget = self._ui.hlDestinations.layout().itemAt(0).widget()
            widget.setParent(None)
            widget.deleteLater()

        for destination_path in all_destinations:
            destination_widget = None
            if destination_path == assigned_folder:
                destination_widget = DestinationFolderView(destination_path, True)
            else:
                destination_widget = DestinationFolderView(destination_path)

            destination_widget.onClickWPath.connect(self.on_assign_destination)
            destination_widget.onRemoveWPath.connect(self.on_delete_destination)
            self._ui.hlDestinations.layout().addWidget(destination_widget)

    def _next_file(self):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        self._current_file_index += 1
        self._current_file_index %= self._file_m_manager.get_n_of_source_files()
        self._reload_all()

    def _prev_file(self):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        self._current_file_index -= 1
        self._current_file_index += self._file_m_manager.get_n_of_source_files()
        self._current_file_index %= self._file_m_manager.get_n_of_source_files()
        self._reload_all()
