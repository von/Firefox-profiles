Firefox-profiles
================

Used to create Macintosh applications for launching different firefox profiles.

Usage:

> `./make-firefox-profile.py <profile-name> [<application-name>]`

By default, creates an application named `Firefox-<profile>.app`.
You can specify `<application-name>` to change this.

The profile name `ProfileManager` is a special case that will create
an application that launches the Firefox profile manager.

To see all options:

> ./make-firefox-profile.py -h

Note this requires you have Firefox installed as /Applications/Firefox.app
(you can change the path with the -A option).

Creating .icns files
====================

* Open OmniGraffle and drag existing icns into a new document.

* Edit as you wish.

* Export as png (with transparent background)

* Open /Developer/Applications/Utilities/Icon Composer.app

* Under File select New ICNS

* Drag png into each of the different sizes

* Save As... filename as you wish.

Kudos: http://macapper.com/2007/04/21/how-to-create-custom-icons-for-your-mac/
