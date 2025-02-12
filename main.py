from json import dump
from PyQt6.QtWidgets import QApplication
from sys import argv, exit
from main_window import MainWindow

with open('specs/spec_list.json', 'w') as f:
    dump(None, f)


class PyPackager(QApplication):
    def __init__(self):
        super().__init__(argv)
        MainWindow().show()
        exit(self.exec())


if __name__ == "__main__":
    PyPackager()