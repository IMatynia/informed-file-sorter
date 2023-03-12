import logging

from PySide6.QtWidgets import QApplication

from src.core.main_window import MainWindow


def main():
    logging.basicConfig(level=logging.INFO)
    app = QApplication()
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    main()
