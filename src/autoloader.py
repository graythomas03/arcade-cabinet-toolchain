#!/usr/bin/env python3

"""
Author: Gray Thomas (graythomas03@protonmail.com)
Description:
    This Python script checks a working directory for special .manifest files then imports
    the application
"""

import argparse # give me command line options

import src.arcade as arcade

def main( paths : list[str] ):
    manifests : list[arcade.Manifest]

    # get list of all manifests from every mounted usb
    for path in paths:
        manifests += arcade.read_manifests_from_dir( path )
    # run the install process for each incoming app
    for m in manifests:
        # only handling installer manifests here
        if m._type == 'Installer':
            pass
    # regenerate menu entries

# define and read command line arguments
if __name__ == "__main__": 
    # Define cmdline arguments/options #
    arg_parser = argparse.ArgumentParser(
        prog='autoloader',
        description='Load new applications and create new menu entries for the VGDC Aracde Machine'
    )
    arg_parser.add_argument('-s','--skip-backup', action='store_true')
    arg_parser.add_argument('path_args', nargs='*')
        
    # CMD ARG VALUES
    paths : list[str] = []
    # read args into values
    args = arg_parser.parse_args()

    # Read manifests from USB storage mount
    for arg in args.path_args:
        paths += arg

main( paths )