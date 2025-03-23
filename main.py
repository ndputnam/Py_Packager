from os import makedirs
from sys import argv, exit

from PyQt6.QtWidgets import QApplication

from builder import dir_check
from main_window import MainWindow

makedirs('specs', exist_ok=True)


class PyPackager(QApplication):
    def __init__(self):
        super().__init__(argv)
        dir_check()
        MainWindow().show()
        exit(self.exec())


if __name__ == "__main__":
    PyPackager()