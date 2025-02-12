from PyQt6.QtWidgets import QApplication
from sys import argv, exit
from builder import dir_check
from main_window import MainWindow


class PyPackager(QApplication):
    def __init__(self):
        super().__init__(argv)
        dir_check()
        MainWindow().show()
        exit(self.exec())


if __name__ == "__main__":
    PyPackager()