#!/bin/python

"""
Author: Gray Thomas (graythomas03@protonmail.com)
Description:
    This Python script checks a working directory for special .manifest files then imports
    the application
"""

import os
import sys

class Manifest:
    _type
    name : str
    name_display : str
    icon : str
    menu_path : str
    
    def __init__(self):
        pass

# read manifest files found at app installtion directory
def cache_manifests( root_app_dir : str ) -> list :
    # enter every directory found in the root_dir

    # if dir contains .manifest file, read info
    pass

def write_menu_changes( manifest_list ):
    pass

def main():

    # Process any cmd args

    # Search for all local app entries

    ### APP PATHS
    root_app_dir = ""
    root_icon_dir = ""
    manifest_file_ext = "*.manifest"
    root_bkup_dir = ""

    incoming_app_dir = ""

    ### CACHED ENTRIES
    entries = cache_manifests( root_app_dir )

    # Install/load new games from incoming USB storage device

    new_entries = cache_manifests( incoming_app_dir )
    for new_entry in new_entries:
        print("Loading manifest for app '{}'...", new_entry.name)
        
        # check if App has been previously loaded
        for entry in entries:
            if new_entry.name == entry.name:
                print("[WARNING] Existing manifest for app '{}' found. Creating backup...", new_entry.name)
                # backup and compress files

        # move files to destination

    # update menu and config files

    write_menu_changes()

main()