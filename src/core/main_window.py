import logging
import os
from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog, QWidget, QSpacerItem, QSizePolicy, \
    QLabel
from src.core.file_moving_manager import FileMovingManager
from src.core.user_config import UserConfig
from src.ui.destination_container_view import DestinationContainerLayout
from src.ui.destination_folder_view import DestinationFolderView
from src.ui.main_window_view import Ui_MainWindow
from src.ui.preview_picture_view import PreviewPictureView
from src.core.addon_loader import AddonLoader


@dataclass
class CoreConfig:
    filter: str = ".*"
    zoom_level: float = 1.0


class MainWindow(QMainWindow):
    full_ui_reload = Signal()
    ui_reload_sources = Signal()
    ui_reload_destinations = Signal()

    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._config_manager = UserConfig()
        self._config: Optional[CoreConfig] = None
        self.reload_config()

        self._file_m_manager = FileMovingManager(self._config.filter)
        self._current_file_index = 0

        self._finalize_ui()
        self._set_up_triggers()

        self._addon_manager = AddonLoader(self)
        self._addon_manager.load_addons()
        self._finalize_addon_ui()

        self.ui_reload_sources.connect(self._reload_sources)
        self.ui_reload_destinations.connect(self._reload_destinations)
        self.full_ui_reload.connect(self._reload_all)

    def get_current_file_index(self) -> int:
        return self._current_file_index

    def get_file_manager(self) -> FileMovingManager:
        return self._file_m_manager

    def get_addon_manager(self) -> AddonLoader:
        return self._addon_manager

    def get_config_manager(self) -> UserConfig:
        return self._config_manager

    def get_ui(self):
        return self._ui

    def add_ui_to_addon_panel(self, ui_element: QWidget, addon_info: dict):
        label = QLabel(f"{addon_info['name']}")
        self._ui.vlAddonsBar.addWidget(label)
        self._ui.vlAddonsBar.addWidget(ui_element)
        self._ui.vlAddonsBar.addSpacing(10)

    def reload_config(self):
        try:
            self._config = self._config_manager.load_config("core")
        except FileNotFoundError:
            self._config = CoreConfig()

    def save_config(self):
        self._config.zoom_level = self._preview_image.get_zoom()
        self._config.filter = self._file_m_manager.get_regex_filter()
        self._config_manager.save_config("core", self._config)

    def _set_up_triggers(self):
        self._preview_image.folders_dropped.connect(self.set_current_folder)
        self._ui.actionNext_file.triggered.connect(self._next_file)
        self._ui.actionPrevious_file.triggered.connect(self._prev_file)
        self._ui.actionConfirm.triggered.connect(self.on_confirm_changes)
        self._ui.actionZoom_in.triggered.connect(self.on_zoom_in)
        self._ui.actionZoom_out.triggered.connect(self.on_zoom_out)
        self._ui.actionDelete_file.triggered.connect(self.on_delete_file)
        self._ui.actionFilter.triggered.connect(self.on_change_filter)
        self._ui.actionOpen_new_destination.triggered.connect(self.on_add_destination)
        self._ui.actionReload_source.triggered.connect(self._refresh_sources)
        self._destination_container.folders_dropped.connect(self.on_add_destination_dropped)
        self._ui.actionClear_assignments.triggered.connect(self.on_clear_assignments)

    def _finalize_ui(self):
        self._preview_image = PreviewPictureView(self._config.zoom_level)
        self._destination_container = DestinationContainerLayout()
        self._ui.hlDestinations.layout().addWidget(self._destination_container)
        self._ui.vbPreviewContainer.layout().addWidget(self._preview_image)

        h = self.geometry().height()
        self._ui.spPreview.setSizes([h * 0.60, h * 0.40])

    def set_current_folder(self, folder_paths: list):
        folder_path = folder_paths[0]
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
            self.ui_reload_sources.emit()

    def on_zoom_out(self):
        self._preview_image.zoom_out()
        if self._file_m_manager.get_n_of_source_files() > 0:
            self.ui_reload_sources.emit()

    def on_delete_file(self):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file_path = self._file_m_manager.get_file_on_index(self._current_file_index)
        res = QMessageBox.question(None, "Are you sure", f"Are you sure you want to delete {current_file_path}?")
        if res == QMessageBox.StandardButton.Yes:
            os.remove(current_file_path)
            logging.info(f"Deleted {current_file_path}")

            if self._current_file_index > 0:
                self._current_file_index -= 1
            self._file_m_manager.refresh_sources()
            self._file_m_manager.remove_assignment(current_file_path)
            self._reload_all()

    def on_add_destination(self):
        directory_path = QFileDialog.getExistingDirectory(None, "Add a destination")
        if directory_path != "":
            self._file_m_manager.add_destination(directory_path)
            self.ui_reload_destinations.emit()

    def on_add_destination_dropped(self, folder_paths: list):
        for folder_path in folder_paths:
            if os.path.isdir(folder_path):
                self._file_m_manager.add_destination(folder_path)
            else:
                logging.info(f"{folder_path} is not a folder")
        self.ui_reload_destinations.emit()

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
        self.ui_reload_destinations.emit()

    def on_assign_destination(self, folder_path: str):
        if self._file_m_manager.get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file_path = self._file_m_manager.get_file_on_index(self._current_file_index)
        try:
            current_assignment = self._file_m_manager.get_assignment(current_file_path)
        except KeyError:
            current_assignment = None

        if current_assignment == folder_path:
            self._file_m_manager.remove_assignment(current_file_path)
        else:
            self._file_m_manager.add_assignment(current_file_path, folder_path)
        self.ui_reload_destinations.emit()

    def on_confirm_changes(self):
        n_files = len(self._file_m_manager.get_all_assignments())
        res = QMessageBox.question(None, f"Are you sure?", f"Are you sure you want to move {n_files} files?")
        if res == QMessageBox.StandardButton.Yes:
            logging.info("Applying changes")
            self._file_m_manager.apply_assignments()
            self._file_m_manager.clear_assignments()
            self._file_m_manager.refresh_sources()
            self._reload_all()

    def on_clear_assignments(self):
        n_files = len(self._file_m_manager.get_all_assignments())
        res = QMessageBox.question(None, f"Are you sure?", f"Are you sure you want to clear {n_files} files?")
        if res == QMessageBox.StandardButton.Yes:
            logging.info("Clearing changes")
            self._file_m_manager.clear_assignments()
            self._reload_all()

    def _reload_all(self):
        self.ui_reload_sources.emit()
        self.ui_reload_destinations.emit()

    def _refresh_sources(self):
        self._file_m_manager.refresh_sources()
        self._current_file_index = 0
        self._reload_sources()

    def _reload_sources(self):
        if self._file_m_manager.get_n_of_source_files() > 0:
            current_file = self._file_m_manager.get_file_on_index(self._current_file_index)
            self._preview_image.set_preview(current_file)
        else:
            self._preview_image.no_files_found()

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

        for i in range(self._destination_container.layout().count()):
            widget = self._destination_container.layout().itemAt(0).widget()
            widget.setParent(None)
            widget.deleteLater()

        for i, destination_path in enumerate(all_destinations):
            destination_widget = None
            if destination_path == assigned_folder:
                destination_widget = DestinationFolderView(destination_path, True, i)
            else:
                destination_widget = DestinationFolderView(destination_path, False, i)

            destination_widget.onClickWPath.connect(self.on_assign_destination)
            destination_widget.onRemoveWPath.connect(self.on_delete_destination)
            self._destination_container.layout().addWidget(destination_widget)

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

    def clear_selection(self):
        self._current_file_index = 0
        self._file_m_manager.set_current_source(None)

    def closeEvent(self, event) -> None:
        res = QMessageBox.question(None, "Are you sure", f"Do you want to save your config?")
        if res == QMessageBox.StandardButton.Yes:
            self.save_config()
        return super().closeEvent(event)

    def _finalize_addon_ui(self):
        spacer = QSpacerItem(1, 1, vData=QSizePolicy.Policy.Expanding, hData=QSizePolicy.Policy.Minimum)
        self._ui.vlAddonsBar.addSpacerItem(spacer)
        self._ui.spAddons.setSizes([100, 0])
