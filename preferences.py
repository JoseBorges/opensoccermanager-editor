#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager-Editor is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager-Editor is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager-Editor.  If not, see <http://www.gnu.org/licenses/>.


from configparser import ConfigParser
import os


class Preferences(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)

        self.window_maximize = True
        self.window_width = 0
        self.window_height = 0
        self.show_toolbar = True
        self.confirm_quit = True
        self.confirm_remove = True
        self.show_age = False
        self.show_value_wage = False

        self["INTERFACE"] = {"Maximized": True,
                             "Width": 0,
                             "Height": 0,
                             "ShowToolbar": True,
                             "ConfirmQuit": True,
                             "ConfirmRemove": True,
                             "ShowAge": False,
                             "ShowValueWage": False,
                            }

        home = os.path.expanduser("~")
        data = os.path.join(home, ".config", "opensoccermanager")
        self.filename = os.path.join(data, "editor.ini")

    def read_file(self):
        self.read(self.filename)

        self.window_maximize = self["INTERFACE"].getboolean("Maximized")
        self.window_width = int(self["INTERFACE"].get("Width"))
        self.window_height = int(self["INTERFACE"].get("Height"))
        self.show_toolbar = self["INTERFACE"].getboolean("ShowToolbar")
        self.confirm_quit = self["INTERFACE"].getboolean("ConfirmQuit")
        self.confirm_remove = self["INTERFACE"].getboolean("ConfirmRemove")
        self.show_age = self["INTERFACE"].getboolean("ShowAge")
        self.show_value_wage = self["INTERFACE"].getboolean("ShowValueWage")

    def write_file(self):
        with open(self.filename, "w") as configfile:
            self.write(configfile)
