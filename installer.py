from json import load

import PyInstaller.__main__


def install():
    try:
        with open('specs/spec_list.json', 'r') as f:
            spec_list = load(f)
            if spec_list is not None:
                PyInstaller.__main__.run(spec_list)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    install()