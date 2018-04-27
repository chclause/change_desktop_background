#!/usr/bin/env python

import os
import subprocess

def set_envir():
    """ DBUS_SESSION_BUS_ADDRESS environment variable is required to run '$gsettings set' in a cron job """
    pid = subprocess.check_output(["pgrep", "gnome-session"]).decode("utf-8").strip()
    cmd = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/"+pid+"/environ|cut -d= -f2-"
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = subprocess.check_output(
        ['/bin/bash', '-c', cmd]).decode("utf-8").strip().replace("\0", "")

def main():
    """ Script to change background based on contents of /home/username/Pictures/Wallpapers/ """
    command_start = 'file://'
    path_to_wallpapers = '/home/charlie/Pictures/Wallpapers/'
    get_command = 'gsettings get org.gnome.desktop.background picture-uri'
    set_command = 'gsettings set org.gnome.desktop.background picture-uri '

    set_envir()

    all_wallpapers = os.listdir(path_to_wallpapers)
    filtered_wallpapers = []
    num_wallpapers = len(all_wallpapers)
    # Ubuntu 16.04 makes a copy of the wallpaper, so filter it out
    for i in range(num_wallpapers):
        if 'copy' not in all_wallpapers[i]:
            filtered_wallpapers.append(all_wallpapers[i])
    
    # Get the full path to current wallpaper and split it, then get just image name
    try:
        # Communicate returns tuple of (output, error code)
        output = subprocess.Popen(
            get_command.split(),
            stdout=subprocess.PIPE).communicate()[0].split('/')
    except Exception as e:
        print e.message
        return
    image = output[-1]
    # Chop out the quotation mark and newline
    current_wallpaper = image[0:len(image)-2]

    # Get current index
    num_wallpapers = len(filtered_wallpapers)
    index = -1
    for i in range(num_wallpapers):
        if current_wallpaper == filtered_wallpapers[i]:
            index = i+1
            break

    # Something went wrong
    if index == -1:
        return

    # Set the next wallpaper in line
    # gsettings set org.gnome.desktop.background picture-uri
    if index >= num_wallpapers:
        index = 0
    next_wallpaper = command_start + path_to_wallpapers + filtered_wallpapers[index]
    next_wallpaper_command = set_command + '"' + next_wallpaper + '"'
    try:
        subprocess.Popen(
            next_wallpaper_command.split(),
            stdout=subprocess.PIPE
        )
    except Exception as e:
        print e.message
        return

main()