from json import dump
from os import listdir, remove

from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWidgets import (QComboBox, QLineEdit, QMainWindow, QPushButton, QToolBar,
                             QMessageBox, QFileDialog, QMenu, QPlainTextEdit, QProgressBar)

from builder import Builder, resource_path
from stylesheets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Packager")
        self.setWindowIcon(QIcon(resource_path('./gear.ico')))
        self.resize(1200, 800)
        self.builder = Builder()
        self.base_dir = 'C:\\'

        self.set_name = QLineEdit()
        self.set_name.setMaximumWidth(200)
        self.set_name.textChanged.connect(self.name)
        self.set_name.setToolTip('Set or update the name of the application to be built.\n'
                                 '(THIS IS NECESSARY)')

        self.main_file = QPushButton('Select Top Level File')
        self.main_file.setStyleSheet(need_unused_button)
        self.main_file.clicked.connect(lambda checked: self.open_file_dialog(
            'Select Top Level File', 'Python (*.py)', self.builder.add_source))
        self.main_file.setToolTip('Select the primary top level file of the application, often named main.py or similar.\n'
                             '(THIS IS NECESSARY)')

        self.dest_folder = QPushButton('Destination Folder')
        self.dest_folder.setStyleSheet(need_unused_button)
        self.dest_folder.clicked.connect(lambda checked: self.open_folder_dialog(
            'Destination Folder', self.builder.add_dest))
        self.dest_folder.setToolTip('Select the folder where you want the new application build sent to when completed.\n'
                               '(THIS IS NECESSARY)')

        self.add_icon = QPushButton('Add Icon')
        self.add_icon.setStyleSheet(unused_button)
        self.add_icon.clicked.connect(lambda checked: self.open_file_dialog(
            'Add Icon', 'Icon (*.ico)', self.builder.add_icon))
        self.add_icon.setToolTip('Select the .ico image to be used as the applications icon if desired.')

        self.move_folder = QPushButton('Copy and Move Folder')
        self.move_folder.setStyleSheet(unused_button)
        self.move_folder.clicked.connect(lambda checked: self.move_folder_dialog(
            'Copy and Move Folder', self.builder.move_folder))
        self.move_folder.setToolTip('If there is data in a directory that will be modified by the application\n'
                               'this will copy and move it to the destination folder\n'
                               '(DESTINATION FOLDER NEEDS TO BE SET FIRST)')

        self.move_file = QPushButton('Copy and Move File')
        self.move_file.setStyleSheet(unused_button)
        self.move_file.clicked.connect(lambda checked: self.move_file_dialog(
            'Copy and Move Folder', self.builder.move_file))
        self.move_file.setToolTip('If there is file that will be needed by the application externally\n'
                               'this will copy and move it to the destination folder\n'
                               '(DESTINATION FOLDER NEEDS TO BE SET FIRST)')

        self.add_folder = QPushButton('Add Folder')
        self.add_folder.setStyleSheet(unused_button)
        self.add_folder.clicked.connect(lambda checked: self.open_folder_dialog('Add Folder', self.builder.add_folder))
        self.add_folder.setToolTip('If there are additional working directories the application needs to reference,\n'
                              'add them to the build')

        self.add_file = QPushButton('Add File')
        self.add_file.setStyleSheet(unused_button)
        self.add_file.clicked.connect(lambda checked: self.open_file_dialog(
            'Add File', '', self.builder.add_file))
        self.add_file.setToolTip('If there are additional files that are not directly imported by the application,\n'
                            'add them to the build')

        self.remove_folder_dd = QComboBox()
        self.remove_folder_dd.setToolTip('Select added folders if you desire to remove them from the build')
        self.remove_folder_dd.addItem('Select Folder To Remove')
        self.remove_folder_dd.addItems(self.builder.specs['folders'])
        self.remove_folder_dd.currentIndexChanged.connect(self.remove_folder)

        self.remove_file_dd = QComboBox()
        self.remove_file_dd.setToolTip('Select added files if you desire to remove them from the build')
        self.remove_file_dd.addItem('Select File To Remove')
        self.remove_file_dd.addItems(self.builder.specs['files'])
        self.remove_file_dd.currentIndexChanged.connect(self.remove_file)

        self.console_button = QPushButton(
            'Build With Console' if self.builder.specs['console'] else 'Build Without Console')
        self.console_button.setStyleSheet(unused_console if self.builder.specs['console'] else used_console)
        self.console_button.clicked.connect(lambda checked: self.console_swap())
        self.console_button.setToolTip('Select if you want the build to have an external console terminal included.\n'
                                       'Having a console will display errors in the console as it closes,\n'
                                       'while excluding it will cause errors to pop up in a warning window.')

        self.run_button = QPushButton('Build Application')
        self.run_button.setStyleSheet(unused_button)
        self.run_button.clicked.connect(lambda checked: self.start_process())
        self.run_button.setToolTip('Once all of the specification for the build are set,\n'
                              'check the display to ensure they look correct,\n'
                              'click here to execute building the package as a single .exe.')

        self.readout = QPlainTextEdit('Load Specification or Configure and Press "Build Application".')
        self.readout.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.readout.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.readout.setToolTip('Display relevant feedback during setup\n'
                                'and execution of the application build process.')

        self.process = None
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setToolTip('Show progress of build during execution.')

        save = QAction(QIcon(resource_path('./folder.ico')), 'Save Specs', self)
        save.triggered.connect(self.save)
        save.setShortcut(QKeySequence('Ctrl+s'))
        save.setToolTip('Save build specification, display show state.\n'
                        'Ideally, save when before executing build.')

        load = QAction(QIcon(resource_path('./folder.ico')), 'Load Specs', self)
        load.triggered.connect(self.load)
        load.setShortcut(QKeySequence('Ctrl+l'))
        load.setToolTip('Load existing saved build specifications.')

        self.load_menu = QMenu('&Load', self)
        for spec in listdir('specs'):
            if spec != 'spec_list.json':
                action = self.load_menu.addAction(spec)
                action.triggered.connect(lambda chk, item=spec: self.load(item))
                action.setToolTip('Build Specification for %s' % spec[:5])

        reset = QAction(QIcon(resource_path('./folder.ico')), 'Create New Specs', self)
        reset.triggered.connect(self.reset)
        reset.setShortcut(QKeySequence('Ctrl+r'))
        reset.setToolTip('Reset specifications to create a new spec file.')

        delete = QAction(QIcon(resource_path('./folder.ico')), 'Delete Specs', self)
        delete.triggered.connect(self.delete)
        delete.setShortcut(QKeySequence('Ctrl+d'))
        delete.setToolTip('Delete current specification file.')

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addSeparator()
        file_menu.addAction(save)
        file_menu.addSeparator()
        file_menu.addMenu(self.load_menu)
        file_menu.addSeparator()
        file_menu.addAction(reset)
        file_menu.addSeparator()
        file_menu.addAction(delete)
        file_menu.addSeparator()

        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addSeparator()
        toolbar.addWidget(self.set_name)
        toolbar.addSeparator()
        toolbar.addWidget(self.main_file)
        toolbar.addSeparator()
        toolbar.addWidget(self.dest_folder)
        toolbar.addSeparator()
        toolbar.addWidget(self.add_icon)
        toolbar.addSeparator()
        toolbar.addWidget(self.move_folder)
        toolbar.addSeparator()
        toolbar.addWidget(self.move_file)
        toolbar.addSeparator()
        toolbar.addWidget(self.add_folder)
        toolbar.addSeparator()
        toolbar.addWidget(self.add_file)
        toolbar.addSeparator()
        toolbar.addWidget(self.remove_folder_dd)
        toolbar.addSeparator()
        toolbar.addWidget(self.remove_file_dd)
        toolbar.addSeparator()
        toolbar.addWidget(self.console_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.run_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.progress)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)
        self.setCentralWidget(self.readout)

    def update(self, saved:bool=False):
        self.progress.setValue(0)
        specs_file = self.builder.specs
        specs_file['saved'] = saved
        self.base_dir = specs_file['source'][:specs_file['source'].rfind('/')]
        self.set_name.setText(specs_file['name'][7:])
        self.main_file.setStyleSheet(used_button if specs_file['source'] else need_unused_button)
        self.dest_folder.setStyleSheet(used_button if specs_file['dest'] else need_unused_button)
        self.add_icon.setStyleSheet(used_button if specs_file['icon'] else unused_button)
        self.add_folder.setStyleSheet(used_button if specs_file['folders'] else unused_button)
        self.remove_folder_dd.clear()
        self.remove_folder_dd.addItem('Select Folder To Remove')
        [self.remove_folder_dd.addItem(folder[:folder.rfind('/')]) for folder in specs_file['folders']]
        self.add_file.setStyleSheet(used_button if specs_file['files'] else unused_button)
        self.remove_file_dd.clear()
        self.remove_file_dd.addItem('Select File To Remove')
        [self.remove_file_dd.addItem(file[:file.rfind('/')]) for file in specs_file['files']]
        self.console_button.setStyleSheet(unused_console if specs_file['console'] else used_console)
        self.console_button.setText('Build With Console' if specs_file['console'] else 'Build Without Console')
        self.run_button.setStyleSheet(saved_button if saved else not_saved_button)
        self.readout.clear()
        self.readout.appendPlainText('App Name: %s\n'
                                     'Path to Source: %s\n'
                                     'Path to Distribution Folder: %s\n'
                                     'Path to Icon: %s\n'
                                     'Paths to Additional Folders: %s\n'
                                     'Paths to Individual Files %s\n'
                                     'Include Active Console in Build: %s\n'
                                     'Spec File Saved: %s' % tuple([specs_file[spec] for spec in specs_file]))

    def save(self):
        name = self.builder.specs['name']
        if name:
            self.builder.save_specs(name[7:])
            if name[7:] + '.json' not in listdir('specs'):
                action = self.load_menu.addAction(name[7:] + '.json')
                action.triggered.connect(lambda chk, item=name[7:] + '.json': self.load(item))
            self.update(True)
        else:
            QMessageBox.critical(self, "No File Name", "Input Name For Spec File",
                                 buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.Ok)

    def load(self, file_name):
        self.builder.load_specs(file_name)
        self.update(True)

    def delete(self):
        name = self.builder.specs['name'][7:] + '.json'
        remove('specs/' + name)
        self.load_menu.removeAction(name)
        self.reset()

    def reset(self):
        self.builder.reset()
        self.update()

    def open_file_dialog(self, title, file_type, func):
        filename, ok = QFileDialog.getOpenFileName(self, title, self.base_dir, file_type)
        if filename:
            func(filename)
            self.update()

    def open_folder_dialog(self, title, func):
        folder = QFileDialog.getExistingDirectory(self, title, self.base_dir)
        if folder:
            func(folder)
            self.update()

    def move_folder_dialog(self, title, func):
        folder = QFileDialog.getExistingDirectory(self, title, self.base_dir)
        if folder:
            moved = func(folder, False)
            if not moved:
                self.move_folder.setStyleSheet(used_button)
                ow = QMessageBox.question(self, "Folder Exists","Continue and overwrite all existing data in folder?",
                                          buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort,
                                          defaultButton=QMessageBox.StandardButton.Ok)
                if ow == QMessageBox.StandardButton.Ok:
                    moved = func(folder, True)
            if moved:
                self.move_folder.setStyleSheet(used_button)
                self.update(self.builder.specs['saved'])

    def move_file_dialog(self, title,  func):
        filename, ok = QFileDialog.getOpenFileName(self, title, self.base_dir)
        if filename:
            moved = func(filename)
            if moved:
                self.move_file.setStyleSheet(used_button)
                self.update(self.builder.specs['saved'])

    def name(self, name):
        if name != self.builder.specs['name'][7:]:
            self.builder.add_name(name)
            self.update()

    def remove_folder(self, folder_index):
        if folder_index > 0:
            self.builder.remove_folder(folder_index - 1)
            self.update()

    def remove_file(self, file_index):
        if file_index > 0:
            self.builder.remove_file(file_index - 1)
            self.update()

    def console_swap(self):
        self.builder.swap_console()
        self.update()

    def start_process(self):
        if self.process is None:
            self.run_button.setStyleSheet(running_button)
            spec_list = self.builder.set_spec_list()
            if spec_list is not None:
                with open('specs/spec_list.json', 'w') as f:
                    dump(spec_list, f)
                self.readout.appendPlainText("Executing process")
                self.process = QProcess()
                self.process.readyReadStandardOutput.connect(self.handle_stdout)
                self.process.readyReadStandardError.connect(self.handle_stderr)
                self.process.stateChanged.connect(self.handle_state)
                self.process.finished.connect(self.process_finished)
                self.process.start('python', [resource_path('installer.py')])
            else:
                QMessageBox.critical(self, "No Build Configured", "Set name, top-level file, and destination folder.\n"
                                                                  "Add icon, and additional files/folders if desired.\n"
                                                                  "Once configured, save the specs file and run again.",
                                     buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.Ok)
                self.run_button.setStyleSheet(saved_button if self.builder.specs['saved'] else not_saved_button)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.readout.appendPlainText(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        try:
            ref = stderr.split(' ')[0]
            val = int(int(ref) / 500)
            if val < 100:
                self.progress.setValue(val)
            else:
                self.progress.setValue(100)
        #          add animation or effect to bar if at 100% and still installing...
        except (TypeError, ValueError):
            pass
        self.readout.appendPlainText(stderr)

    def handle_state(self, state):
        states = {QProcess.ProcessState.NotRunning: 'Build Not Running',
                  QProcess.ProcessState.Starting: 'Starting Build',
                  QProcess.ProcessState.Running: 'Building Application'}
        state_name = states[state]
        if state_name == 'Build Not Running':
            with open('specs/spec_list.json', 'w') as f:
                dump(None, f)
        self.readout.appendPlainText(f"State changed: {state_name}")

    def process_finished(self):
        self.process = None
        self.run_button.setStyleSheet(saved_button if self.builder.specs['saved'] else not_saved_button)
        if self.builder.specs['name'][7:] + '.exe' in listdir(self.builder.specs['dest'][11:]):
            self.readout.appendPlainText("Build Complete! Find it in: %s" % self.builder.specs['dest'][11:])
            self.progress.setValue(100)
        else:
            self.readout.appendPlainText("Build Failed.\n"
                                         "Check for errors in applications code base.\n"
                                         "Incorrect resource paths\n"
                                         "or missing files that are not directly imported by the application\n"
                                         "are common causes.\n"
                                         "Try building with a console window to catch errors.")
