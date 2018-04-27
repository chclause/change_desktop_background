Made by Charlie Clausen

This script can be run in crontab to change desktop background in a provided interval.  Tested on Ubuntu 16.04.
It works by pulling pictures from your /home/username/Pictures/Wallpapers/ directory, so put any pictures you
want in the rotation in there.  

To Use:

    1. Open your crontab file with '$ crontab -e'

    2. Add the line '0,30 * * * * /home/username/path/to/python_script.py' without the quotes.
        This will change your background every 30 minutes.  Replace 'username' with your username.
        Replace 'path/to/script.py' with wherever you stored the python file from this repo.
        In the end it should look something like: /home/charlie/background_script/change_background.py
        Remove the ',30' to have it change every hour or review crontab syntax to set your own schedule.

    3. Make sure the script has executable permissions with '$ chmod a+x path/to/script.py'