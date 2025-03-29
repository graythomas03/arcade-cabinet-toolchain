#!/usr/bin/python3

"""
Author: Gray Thomas (graythomas03@protonmail.com)
Description:
    Python module that provides wrappers and functionality for interacting with the VGDC Arcade Machine's kinda janky menu system

Canonical Path: /home/vgdc/
SYMLINK'd TO: /home/vgdc/.local/lib/python3.13/site-packages
"""

import fileinput # give me File
import tomllib # give me manifest config reader
import os # give me Linux
import pathlib # give me more Linux
import shutil # give me copy

# HOME_DIR = os.getenv('HOME') # should be /home/vgdc
# ICON_DIR = os.getenv('ARCADE_ICON_DIR') # should be /home/vgdc/menu/icons
# APP_DIR = os.getenv('ARCADE_APP_DIR') # should be /home/vgdc/apps/
# MENU_DIR = os.getenv('ARCADE_MENU_DIR') # should be /home/vgdc/menu/entries
HOME_DIR = '/home/vgdc'
ICON_DIR = f'{HOME_DIR}/menu/icons'
APP_DIR = f'{HOME_DIR}/apps'
MENU_DIR = f'{HOME_DIR}/menu/entries'
MENU_CONF = f'{HOME_DIR}/menu-config.ini'
FLEX_LAUNCHER_CONFIG_PATH = f'{HOME_DIR}/.config/flex-launcher/config.ini'

# FORMAT: display_name;icon_name;app_name
# MENU_ENTRY_FMT = 'Entry{0}={1};' + ICON_DIR + '{2}.png;' + MENU_DIR + '{3}'
# MENU_ENTRY_FMT = '{1};' + ICON_DIR + '/{2}.png;' + MENU_DIR + '/{3}'
MENU_ENTRY_FMT = '{0};{1}.png;{2}' # debugging case

# According to the Free Desktop standard
DESKTOP_ENTRY_FILE_FMT = """
[Desktop Entry]
Name={0}
Type=Application
Terminal=false
Exec={1}
"""

class Manifest:
    name : str
    _type : str
    display_name : str
    icon : str
    _exec : str

    def __init__(self, _type : str, name : str, display_name : str, icon : str, _exec : str):
        self._type = _type
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self._exec = _exec

    def to_menu_entry(self) -> str:
        cmd = None
        if self.type == 'App':
            cmd = self.name.join('.desktop')
        else:
            # print( 'Unknown type', self.type, 'for manifest', self.name )
            return None
        return MENU_ENTRY_FMT.format(self.name_display, self.icon, cmd)

## ENTRY CREATION FUNCTIONS FROM MANIFEST FILES ##

def create_desktop_entry_from_manifest( app: Manifest ) -> None:
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
        # print( 'Skipping entry build for non-app manifest', app.name )
        pass

## MANIFEST FILE READING ##

def read_manifest_from_file( path : str ) -> Manifest:
    out : Manifest = None
    try:
        with open( path, 'rb' ) as fp:
            manifest_data = tomllib.load(fp)
            cmd = None
            # ensure manifest has type
            manifest_type = manifest_data['Type']
            if manifest_type == 'Installer':
                # check for custom installer
                if manifest_data['CustomInstaller'] != None:
                    cmd = manifest_data['CustomInstaller'] + ' ' + manifest_data['InstallFrom'] + APP_DIR + '/' + manifest_data['Name']

                # else use default copy-installer
                else:
                    # cmd = 'default-installer ' + manifest_data['InstallFrom'] + APP_DIR + '/' + manifest_data['Name']
                    cmd = f'default-installer {manifest_data['InstallFrom']} {APP_DIR}/{manifest_data['Name']}'

            elif manifest_type == 'App':
                cmd = manifest_data['Exec']

            else:
                print('Unrecognized type in manifest file', path)

            out = Manifest(manifest_type, manifest_data['Name'],
                               manifest_data['DisplayName'],
                               manifest_data['Icon'],
                               cmd)
            
    except Exception as e:
        print( 'Invalid format in manifest file', path, ' Got exception', e)

    return out

def read_manifests_from_dir( path : str ) -> list[Manifest]:
    manifests : list[Manifest]

    for entry in os.scandir(path):
        if entry.is_file():
            manifests += read_manifest_from_file( path )

    return manifests

def write_manifest_to_file( m : Manifest ):
    pass

## MENU MANAGEMENT ##

def build_menu_struct_from_dir( menu_dir: str ) -> dict:
    menu_structure = {}

    for entry in os.scandir( menu_dir ):
        if entry.is_dir(): # If its a submenu
            menu_structure[entry.name] = build_menu_struct_from_dir( entry.path )
        else: # entry is manifest file
            print(entry.path)
            m = read_manifest_from_file( entry.path )
            if m != None:
                menu_structure.setdefault('__manifests__', []).append( m )

    return menu_structure

def menu_struct_to_str( menu: dict, submenu='Main') -> str:
    menu_str = f"[{submenu}]\n"
    entry_cnt = 1 # used for the weird entry numbering thing flex-launcher has going on
    submenus = [] # post-process all encountered submenu after current submenu

    # Read __manifests__ first
    for key, val in menu.items():
        if isinstance(val, list):
            for m in val:
                if isinstance(m, Manifest):
                    menu_str += f'Entry{entry_cnt}=' + m.to_menu_entry() + '\n'
                    entry_cnt += 1

    # Process submenus
    for key, val in menu.items():
        if isinstance( val, dict ):
            menu_str += f'Entry{entry_cnt}={key};{ICON_DIR}/folder.png;:submenu {key}\n'
            entry_cnt += 1
            submenus.append( menu_struct_to_str( val, section=key ) )
    # join everything together
    menu_str += '\n'
    menu_str += ''.join( submenus )

    return menu_str

def rebuild_menu() -> None:
    menu = menu_struct_to_str( build_menu_struct_from_dir( MENU_DIR ) )
    # combine flex-launcher options with new menu structure #
    shutil.copyfile( MENU_CONF,  FLEX_LAUNCHER_CONFIG_PATH)
    with open( FLEX_LAUNCHER_CONFIG_PATH, 'a' ) as fp:
        fp.write( menu )

# testing things
def main():
    menu = build_menu_struct_from_dir( './test' )
    print(menu)

main()
