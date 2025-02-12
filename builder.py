from os import PathLike, makedirs
from os.path import dirname, abspath, join, exists
from shutil import copytree, copyfile, rmtree
from json import dump, load
from pathlib import Path
from typing import Union
import sys

def dir_check():
    if not exists('specs'):
        makedirs('specs')
    with open('specs/spec_list.json', 'w') as f:
        dump(None, f)

def resource_path(relative_path:Union[str, PathLike]):
    """
    Takes path and formats it as needed to be reached when packaged
    :param relative_path:
    :return: modified path
    """
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = dirname(abspath(__file__))
    except AttributeError:
        base_path = abspath(".")
    return join(base_path, relative_path)


class Builder:
    def __init__(self):
        self.spec_list = None
        self.specs = {'name': '',
                      'source': '',
                      'dest': '',
                      'icon': '',
                      'folders': [],
                      'files': [],
                      'console': False,
                      'saved': False}

    def add_name(self, name:str):
        """
        Name of application to be applied to final build.
        :param name: str
        """
        self.specs['name'] = '--name=' + name

    def add_source(self, source_path:str):
        """
        Full path to primary top-level source (main.py).
        :param source_path: str
        :return:
        """
        self.specs['source'] = resource_path(source_path)

    def add_dest(self, dest_path:str):
        """
        Full path to destination folder for the build.
        :param dest_path: str
        """
        self.specs['dest'] = '--distpath=' + resource_path(dest_path)

    def add_icon(self, icon_path:str):
        """
        Full path to .ico image to be applied to the final build.
        :param icon_path: str
        """
        self.specs['icon'] = '--icon=' + resource_path(icon_path)

    def move_folder(self, folder_path:str, overwrite:bool):
        """
        Move a folder containing dynamic reference for the application (saved data).
        :param folder_path: path to folder to be moved.
        :param overwrite: found the folder already exists, verify if to overwrite.
        :return: True if moved
        """
        dest_dir = self.specs['dest'][11:] + folder_path[folder_path.rfind('/'):]
        try:
            copytree(Path(folder_path), Path(dest_dir))
            return True
        except WindowsError:
            if overwrite:
                try:
                    rmtree(Path(dest_dir))
                    copytree(Path(folder_path), Path(dest_dir))
                    return True
                except Exception as e:
                    print('error %s' % e)
                    return False
            return False

    def move_file(self, file_path:str):
        """
        Move a file needed externally for the application.
        :param file_path: path to file to be moved.
        :return: True if moved.
        """
        dest_dir = self.specs['dest'][11:] + file_path[file_path.rfind('/'):]
        try:
            copyfile(Path(file_path), Path(dest_dir))
            return True
        except Exception as e:
            print('error %s' % e)
            return False

    def add_folder(self, folder_path:str):
        """
        Full path to additional folders in the application.
        :param folder_path: str
        :return:
        """
        self.specs['folders'].append('--add-data=' + folder_path + ';.' + folder_path[folder_path.rfind('/'):])

    def remove_folder(self, folder_index:int):
        self.specs['folders'].pop(folder_index)

    def add_file(self, file_path:str):
        """
        Full path to individual files not specifically imported into the application.
        :param file_path: str
        """
        self.specs['files'].append('--add-data=' + resource_path(file_path) + ';./')

    def remove_file(self, file_index:int):
        self.specs['files'].pop(file_index)

    def swap_console(self):
        """
        Build app with or without a console.
        """
        self.specs['console'] = not self.specs['console']

    def save_specs(self, spec_file:str):
        with open('specs/' + spec_file + '.json', 'w') as f:
            dump(self.specs, f)

    def load_specs(self, spec_file:str):
        with open('specs/' + spec_file, 'r') as f:
            self.specs = load(f)

    def reset(self):
        self.specs = {'name': '',
                      'source': '',
                      'dest': '',
                      'icon': '',
                      'folders': [],
                      'files': [],
                      'console': False,
                      'saved': False}

    def set_spec_list(self):
        """
        Structure list to be applied to PyInstaller to build application.
        :return: list
        """
        root_dir = self.specs['source'][:self.specs['source'].rfind('/')]
        if self.specs['source'] and self.specs['dest'] and self.specs['name']:
            self.spec_list = ['%s' % self.specs['source'],
                              '%s' % self.specs['dest'],
                              '%s' % self.specs['name'],
                              '--paths=%s' % root_dir,
                              '--onefile',
                              '--noconfirm',
                              '--clean']
            if self.specs['icon']:
                self.spec_list.append(self.specs['icon'])
            for folder in self.specs['folders']:
                self.spec_list.append(folder)
            for file in self.specs['files']:
                self.spec_list.append(file)
            if not self.specs['console']:
                self.spec_list.append('--windowed')
                self.spec_list.append('--noconsole')
            return self.spec_list
        return None