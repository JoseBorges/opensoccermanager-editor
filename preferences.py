#!/usr/bin/env python3

from configparser import ConfigParser
import os


class Preferences(ConfigParser):
    show_toolbar = True
    confirm_quit = True
    confirm_remove = True
    window_maximize = True
    window_width = 0
    window_height = 0

    def __init__(self):
        ConfigParser.__init__(self)

        home = os.path.expanduser("~")
        data = os.path.join(home, ".config", "opensoccermanager")

        self["INTERFACE"] = {"ShowToolbar": True,
                             "ConfirmQuit": True,
                             "ConfirmRemove": True,
                             "Maximized": True,
                             "Width": 0,
                             "Height": 0,}

        self.filename = os.path.join(data, "editor.ini")

    def read_file(self):
        self.read(self.filename)

        self.show_toolbar = self["INTERFACE"].getboolean("ShowToolbar")
        self.confirm_quit = self["INTERFACE"].getboolean("ConfirmQuit")
        self.confirm_remove = self["INTERFACE"].getboolean("ConfirmRemove")
        self.window_maximize = self["INTERFACE"].getboolean("Maximized")
        self.window_width = int(self["INTERFACE"].get("Width"))
        self.window_height = int(self["INTERFACE"].get("Height"))

    def write_file(self):
        with open(self.filename, "w") as configfile:
            self.write(configfile)