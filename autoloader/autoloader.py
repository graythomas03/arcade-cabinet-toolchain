#!/bin/python

"""
Author: Gray Thomas (graythomas03@protonmail.com)
Description:
    This Python script checks a working directory for special .manifest files then imports
    the application
"""

import os # give me Linux
import fileinput # give me File
import tomllib # give me Config format

HOME_DIR = os.getenv('HOME') # should be /home/vgdc
ICON_DIR = os.getenv('ARCADE_ICON_DIR') # should be /home/vgdc/menu/icons
APP_DIR = os.getenv('ARCADE_APP_DIR') # should be /home/vgdc/apps/
MENU_DIR = os.getenv('ARCADE_MENU_DIR') # should be /home/vgdc/menu/entries

DESKTOP_ENTRY_FILE_FMT = """
[Desktop Entry]
Name={0}
Type=Application
Terminal=false
Exec={1}
"""

# FORMAT: display_name;icon_name;app_name
# MENU_ENTRY_FMT = 'Entry{0}={1};' + ICON_DIR + '{2}.png;' + MENU_DIR + '{3}'

class Manifest:
    type : str
    name : str
    name_display : str
    icon : str
    executable : str
    menu_path : str
    
    def __init__(self, type, name, name_display, icon, executable, menu_path):
        self.type = type
        self.name = name
        self.name_display = name_display
        self.icon = icon
        self.executable = executable
        self.menu_path = menu_path

def create_menu_entry_string():
    pass

def create_desktop_entry( app: Manifest ):
    # skip Manifest entry if Link or Category
    if app.type == 'App':
        # abs_exec_path = HOME_DIR + '/' + APP_DIR + '/' + app.name + '/' + app.executable
        abs_exec_path = app.executable
        # open new desktop file with same name as manifest
        # new_desktop_entry_path = "%s/apps/%s.desktop".format(HOME_DIR, app.name)
        new_desktop_entry_path = app.name + '.desktop'
        with open(new_desktop_entry_path, 'w+') as fp:
            fp.write( DESKTOP_ENTRY_FILE_FMT.format( app.name, abs_exec_path ) )
    else:
        print( 'Skipping entry build for non-app manifest', app.name )

def main():
    test_manifest_0 = Manifest('App', 'Test0', 'DisplayTest', 'Debug', 'TestExec', '')
    test_manifest_1 = Manifest('Link', 'Test1', 'DisplayTest', 'Debug', 'TestExec', '')
    create_desktop_entry( test_manifest_0 )
    create_desktop_entry( test_manifest_1 )

main()