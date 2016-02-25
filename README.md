# OnceAnHour
A simple idle game written in python.

OnceAnHour is written with Python 2.7.

OnceAnHour uses the following modules: ctypes, time, random, shelve, dbhash, os.

OnceAnHour.py is packaged with two key files: setup.py and config.txt.

setup.py is a simple py2exe script that packages OnceAnHour.py as an .exe. It will also apply an icon to the .exe if an appropriately named .ico file is provided.

config.txt contains a variety of variables and strings from OnceAnHour.py being exposed in plain text. A large percentage of the game is "moddable" in this way. One of the goals of the project is to expose everything that is reasonable to config.txt and thus allow for full moddability. 

By default, OnceAnHour is only supported on Windows. The main reason for this is because of the usage of ctypes to create the popup window. The source should be fully accessible on any platform that supports Python 2.7.

Please see the LICENSE file for information on the license for OnceAnHour.

OnceAnHour was written by roocey (Andrew Wright).

Contact:

blog: http://www.caffeineoverdose.me/

twitter: https://twitter.com/roocey

e-mail: roocey at gmail dot com
