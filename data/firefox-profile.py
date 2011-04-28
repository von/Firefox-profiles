#!/usr/bin/env python
"""Run FireFox using a given profile as specified by ff-profile.conf

ff-profile.conf should look like:

[Profile]
name: Personal
# Disallow remote connections?
no-remote: True

[FireFox]
path: /Applications/Firefox.app/

"""

import ConfigParser
import os
import os.path
import subprocess
import sys

def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    # Find path script is being run out of
    my_path = os.path.abspath(os.path.dirname(argv[0]))

    config = ConfigParser.SafeConfigParser()
    config.read(os.path.join(my_path, "ff-profile.conf"))
    
    binary = os.path.join(config.get("FireFox", "path"),
                          "Contents/MacOS/firefox-bin")

    args = [binary]
    profile_name = config.get("Profile", "name")
    if profile_name == "ProfileManager":
        args.append("-ProfileManager")
    else:
        args.append("-P")
        args.append(config.get("Profile", "name"))

    no_remote = config.getboolean("Profile", "no-remote")
    if no_remote:
        args.append("-no-remote")

    try:
        os.execv(binary, args)
    except OSError as e:
        print "Error executing {}: {}".format(binary, e)

if __name__ == "__main__":
    sys.exit(main())
