import logging
import os.path
from PySide6.QtGui import QShortcut
from addons.lib.FFMPEGconvertwebptopng import ffmpeg_conversion_from_webp_to_png
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from src.core.addon import Addon
from src.core.main_window import MainWindow


class WebpToPNG(Addon):
    def __init__(self, context: MainWindow):
        super().__init__(context)
        self._addon_info = {
            "name": "Webp to PNG conversion",
            "description": "Converts currently viewed .webp file into png format using FFMPEG. Requires FFMPEG in path"
        }
        self._context: MainWindow = context
        self._addon_ui = QWidget()

    def _build_ui(self):
        self.btConvert = QPushButton()
        self.btConvert.setText("Convert WEBP to PNG")
        self.btConvert.clicked.connect(self._on_convert)
        self.btConvert.setDisabled(True)
        vbox = QVBoxLayout()
        vbox.addWidget(self.btConvert)
        self._addon_ui.setLayout(vbox)

        self._shortcut = QShortcut(self._context)
        self._shortcut.setKey("Ctrl+P")
        self._shortcut.activated.connect(self._on_convert)

    def _on_update(self):
        if self._context.get_file_manager().get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file = self._context.get_file_manager().get_file_on_index(self._context.get_current_file_index())
        name, extension = os.path.splitext(current_file)
        if extension == ".webp":
            self.btConvert.setDisabled(False)
        else:
            self.btConvert.setDisabled(True)

    def _on_convert(self):
        if self._context.get_file_manager().get_n_of_source_files() == 0:
            logging.info("No files")
            return
        current_file = self._context.get_file_manager().get_file_on_index(self._context.get_current_file_index())

        name, extension = os.path.splitext(current_file)
        folder, filename = os.path.split(current_file)
        if extension != ".webp":
            logging.error(f"Can't convert {extension} file to png")

        res = QMessageBox.question(None, "Are you sure",
                                   f"Are you sure you want to convert {current_file} to png format?")
        if res != QMessageBox.StandardButton.Yes:
            return

        converted_file = ffmpeg_conversion_from_webp_to_png(folder, filename)
        self._swap_assignments(converted_file, current_file)
        self._context.full_ui_reload.emit()

    def _swap_assignments(self, converted_file, current_file):
        file_manager = self._context.get_file_manager()
        file_manager.set_file_on_index(self._context.get_current_file_index(), converted_file)
        assignment = file_manager.get_assignment(current_file)
        if assignment:
            file_manager.remove_assignment(current_file)
            file_manager.add_assignment(converted_file, assignment)

    def init(self):
        self._build_ui()
        self._context.add_ui_to_addon_panel(self._addon_ui, self._addon_info)
        self._context.ui_reload_sources.connect(self._on_update)


ADDON_CLASS = WebpToPNG
