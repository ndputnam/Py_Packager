from typing import Union
from os import PathLike
import sys
from os.path import dirname, abspath, join
from PyInstaller import __main__ as pi_main
from copy import deepcopy
from json import dump, load
from ast import literal_eval

SPECS = {'source': '',
         'dest': '',
         'name': '',
         'icon': '',
         'folders': [],
         'files': [],
         'console': False}

def resource_path(relative_path:Union[str, PathLike]):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = dirname(abspath(__file__))
    except AttributeError:
        base_path = abspath(".")
    return join(base_path, relative_path)


class Installer:
    def __init__(self):
        self.pi_main = pi_main
        self.specs = deepcopy(SPECS)

    def add_source(self, source_path:str):
        """
        full path to primary top-level source (main.py)
        :param source_path: str
        :return:
        """
        self.specs['source'] = source_path

    def add_dest(self, dest_path:str):
        """
        full path to destination folder for the build
        :param dest_path: str
        :return:
        """
        self.specs['dest'] = '--distpath=' + dest_path

    def add_name(self, name:str):
        """
        name of application to be applied to final build
        :param name: str
        :return:
        """
        self.specs['name'] = '--name=' + name

    def add_icon(self, icon_path:str):
        """
        full path to .ico image to be applied to the final build
        :param icon_path: str
        :return:
        """
        self.specs['icon'] = '--icon=' + icon_path

    def add_folder(self, folder_path:str):
        """
        full path to additional folders in the application
        :param folder_path: str
        :return:
        """
        self.specs['folders'].append('--add-data=' + folder_path + ';./')

    def remove_folder(self, folder_path:str):
        self.specs['folders'].pop(self.specs['folders'].index('--add-data=' + folder_path + ';./'))

    def add_file(self, file_path:str):
        """
        full path to individual files not specifically imported into the application
        :param file_path: str
        :return:
        """
        self.specs['files'].append('--add-data=' + file_path + ';./')

    def remove_file(self, file_path:str):
        self.specs['files'].pop(self.specs['files'].index('--add-data=' + file_path + ';./'))

    def swap_console(self):
        """
        Build app with or without a console
        :return:
        """
        self.specs['console'] = not self.specs['console']

    def save_specs(self, spec_file:str):
        with open(resource_path('specs/' + spec_file + '.json'), 'w') as f:
            dump(self.specs, f)

    def load_specs(self, spec_file:str):
        with open(resource_path('specs/' + spec_file + '.json'), 'r') as f:
            self.specs = literal_eval(load(f))

    def run(self):
        """
        execute build with specifications
        :return:
        """
        self.pi_main.run(['%s' % self.specs['source'],
                          '%s' % self.specs['dest'],
                          '%s' % self.specs['name'],
                          '%s' % self.specs['icon'],
                          '%s' % ''.join(', ' + folder for folder in self.specs['folders']),
                          '%s' % ''.join(', ' + file for file in self.specs['files']),
                          '%s' % '' if self.specs['console'] else '--windowed',
                          '%s' % '' if self.specs['console'] else '--noconsole',
                          '--onefile',
                          '--noconfirm',
                          '--clean'])