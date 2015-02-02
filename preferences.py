#!/usr/bin/env python3

from configparser import ConfigParser
import os


class Preferences(ConfigParser):
    confirm_quit = False
    confirm_remove = False

    def __init__(self):
        ConfigParser.__init__(self)

        home = os.path.expanduser("~")
        data = os.path.join(home, ".config", "opensoccermanager")

        self["INTERFACE"] = {"ConfirmQuit": True}
        self["INTERFACE"] = {"ConfirmRemove": True}

        self.filename = os.path.join(data, "editor.ini")

    def read_file(self):
        self.read(self.filename)

        self.confirm_quit = self["INTERFACE"].getboolean("ConfirmQuit")
        self.confirm_remove = self["INTERFACE"].getboolean("ConfirmRemove")

    def write_file(self):
        with open(self.filename, "w") as configfile:
            self.write(configfile)
