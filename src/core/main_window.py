from src.core.action_history import ActionHistory
from PySide6.QtWidgets import QMainWindow

from src.core.file_moving_manager import FileMovingManager
from src.ui.main_window_view import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._set_up_triggers()
        self._action_history = ActionHistory()
        self._file_m_manager = FileMovingManager()
        self._current_file_index = 0

    def _set_up_triggers(self):
        self._ui.actionRedo.connect(self._action_history.redo_action)
        self._ui.actionRevert.connect(self._action_history.undo_action)
