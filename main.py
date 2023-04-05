import logging
from PySide6.QtWidgets import QApplication

from src.core.main_window import MainWindow


def main():
    logging.basicConfig(format="[%(asctime)s->%(levelname)s->%(module)s" +
                               "->%(funcName)s]: %(message)s",
                        datefmt="%H:%M:%S",
                        level=logging.INFO)
    app = QApplication()
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    main()
