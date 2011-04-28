#!/usr/bin/env python
"""Create a FireFox profile application"""
import argparse
import glob
import logging
import os
import os.path
import shutil
import string
import sys

def process(arg):
    """Print the given argument"""
    print "Argument: {}".format(arg)
    # Allow command-line argument to create an error
    if arg == "error":
        return True
    return False

def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    # Set up out output via logging module
    output = logging.getLogger(argv[0])
    output.setLevel(logging.DEBUG)
    output_handler = logging.StreamHandler(sys.stdout)  # Default is sys.stderr
    # Set up formatter to just print message without preamble
    output_handler.setFormatter(logging.Formatter("%(message)s"))
    output.addHandler(output_handler)

    # Argument parsing
    parser = argparse.ArgumentParser(
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
        )
    # Only allow one of debug/quiet mode
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-d", "--debug",
                                 action='store_const', const=logging.DEBUG,
                                 dest="output_level", default=logging.INFO,
                                 help="print debugging")
    verbosity_group.add_argument("-q", "--quiet",
                                 action="store_const", const=logging.WARNING,
                                 dest="output_level",
                                 help="run quietly")
    parser.add_argument("-A", "--application", 
                        default="/Applications/Firefox.app/",
                        metavar="path", help="specify Firefox application")
    parser.add_argument("-R", "-allow_remote",
                        action="store_true", dest="allow_remote", default=False,
                        help="Allow profile to accept remote requests (do not specify -no-remote)")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("profile", metavar="profile", type=str, nargs=1,
                        help="Profile to create. 'ProfileManage' opens profile manager.")
    parser.add_argument("app_name", metavar="app_name", type=str,
                        nargs="?", default=None,
                        help="Application name to create (default is Firefox-[profile].app")
    
    args = parser.parse_args()
    output_handler.setLevel(args.output_level)

    # Figure out our parameters
    firefox_app = args.application
    profile_name = args.profile[0]
    my_path = os.path.abspath(os.path.dirname(argv[0]))
    data_path = os.path.join(my_path, "data")
    app_name = "Firefox-" + args.profile[0] + ".app" if args.app_name is None \
        else args.app_name[0]
    script_name = "firefox-bin"  # From Info.plist
    conf_name = "ff-profile.conf"
    macOS_path = os.path.join(app_name, "Contents", "MacOS")
    no_remote = not args.allow_remote

    if os.path.exists(app_name):
        output.error("Application \"{}\" already exists.".format(app_name))
        return(1)

    # And create the app
    os.makedirs(macOS_path)
    shutil.copy(os.path.join(data_path, "firefox-profile.py"),
                os.path.join(macOS_path, script_name))
    
    # Create configuration from template
    with open(os.path.join(data_path, "ff-profile.conf.in")) as f:
        template = string.Template("".join(f.readlines()))

    conf = template.substitute({
            "Application" : firefox_app,
            "Profile" : profile_name,
            "NoRemote" : str(no_remote),
            })

    with open(os.path.join(macOS_path, conf_name), "w") as f:
        f.write(conf)

    # Copy stuff to set the icon from real application
    info_plist = os.path.join(firefox_app, "Contents", "Info.plist")
    shutil.copy(info_plist, os.path.join(app_name, "Contents"))

    icns_glob = os.path.join(firefox_app, "Contents", "Resources", "*.icns")
    resources_path = os.path.join(app_name, "Contents", "Resources")
    os.makedirs(resources_path)
    for file in glob.glob(icns_glob):
        shutil.copy(file, resources_path)

    return(0)

if __name__ == "__main__":
    sys.exit(main())
