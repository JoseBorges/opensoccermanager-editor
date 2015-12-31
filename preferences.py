#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


from configparser import ConfigParser
import os


class Preferences:
    def __init__(self):
        home = os.path.expanduser("~")
        self.data_path = os.path.join(home, ".config", "opensoccermanager")
        self.preferences_path = os.path.join(self.data_path, "editor.ini")

        self.maximized = False
        self.window_size = [832, 534]
        self.window_position = [0, 0]
        self.show_toolbar = True
        self.confirm_remove = True
        self.confirm_quit = True

        self.confighandler = ConfigParser()

        if not os.path.exists(self.preferences_path):
            self.create_initial_config()

    def create_initial_config(self):
        '''
        Create the initial config when it doesn't exist.
        '''
        self.confighandler["INTERFACE"] = {"Maximized": False}

    def read_from_config(self):
        '''
        Read preference settings from file.
        '''
        self.confighandler.read(self.preferences_path)

        self.maximized = self.confighandler["INTERFACE"].getboolean("Maximized")

        width = int(self.confighandler["INTERFACE"]["Width"])
        height = int(self.confighandler["INTERFACE"]["Height"])
        self.window_size = [width, height]

        xposition = int(self.confighandler["INTERFACE"]["XPosition"])
        yposition = int(self.confighandler["INTERFACE"]["YPosition"])
        self.window_position = [xposition, yposition]

        self.confirm_quit = self.confighandler["INTERFACE"].getboolean("ConfirmQuit")
        self.confirm_remove = self.confighandler["INTERFACE"].getboolean("ConfirmRemove")
        self.show_toolbar = self.confighandler["INTERFACE"].getboolean("ShowToolbar")

    def write_to_config(self):
        '''
        Write preference settings to file.
        '''
        self.confighandler["INTERFACE"]["ConfirmQuit"] = str(self.confirm_quit)
        self.confighandler["INTERFACE"]["ConfirmRemove"] = str(self.confirm_remove)
        self.confighandler["INTERFACE"]["ShowToolbar"] = str(self.show_toolbar)
        self.confighandler["INTERFACE"]["Width"] = str(self.window_size[0])
        self.confighandler["INTERFACE"]["Height"] = str(self.window_size[1])
        self.confighandler["INTERFACE"]["XPosition"] = str(self.window_position[0])
        self.confighandler["INTERFACE"]["YPosition"] = str(self.window_position[1])

        with open(self.preferences_path, "w") as config:
            self.confighandler.write(config)
