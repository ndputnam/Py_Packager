from PyInstaller import __main__ as pi_main

if input('RUN BUILD?') == '':
    pi_main.run([
        'C:/Users/chance/PycharmProjects/Sacred Ground/main.py',
        '--onefile',
        '--name=Sacred Ground',
        '--icon=favicon.ico',
        '--distpath=D:\\THE_GAME\\beta testing',
        '--add-data=data;./data',
        '--add-data=logic.dll;./',
        '--add-data=SteamworksPy64.dll;./',
        '--add-data=steam_api64.dll;./',
        '--add-data=steam_api64.lib;./',
        '--add-data=steam_appid.txt;./',
        '--noconfirm',
        # comment out windowed and noconsole to allow terminal outputs window...
        '--windowed',
        '--noconsole',
        '--clean'])


