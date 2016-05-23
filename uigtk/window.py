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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os

import data
import uigtk.menu
import uigtk.toolbar
import uigtk.welcome


class Window(Gtk.Window):
    def __init__(self):
        data.preferences.read_from_config()

        iconpath = os.path.join("resources", "logo.svg")
        self.logo = GdkPixbuf.Pixbuf.new_from_file(iconpath)

        Gtk.Window.__init__(self)
        self.set_title("Editor")
        self.set_default_icon(self.logo)
        self.connect("delete-event", self.on_quit)

        self.set_default_size(*data.preferences.window_size)
        self.move(*data.preferences.window_position)

        if data.preferences.maximized:
            self.maximize()

        self.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(self.accelgroup)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.welcome = uigtk.welcome.Welcome()

    def add_interface_widget(self, notebook):
        '''
        Add notebook interface to window.
        '''
        self.notebook = notebook
        self.grid.attach(notebook, 0, 2, 1, 1)

    def on_quit(self, *args):
        '''
        Determine user response and save config to file to exit.
        '''
        state = 1

        if data.unsaved:
            dialog = UnsavedDialog()
            state = dialog.show()
        else:
            if data.preferences.confirm_quit:
                dialog = QuitDialog()
                state = dialog.show()
            else:
                state = 0

        if state == 0:
            data.preferences.window_size = self.get_size()
            data.preferences.window_position = self.get_position()
            data.preferences.write_to_config()

            Gtk.main_quit()

        return state

    def run(self):
        self.menu = uigtk.menu.Menu()
        self.grid.attach(self.menu, 0, 0, 1, 1)

        self.toolbar = uigtk.toolbar.Toolbar()
        self.grid.attach(self.toolbar, 0, 1, 1, 1)

        self.grid.attach(self.welcome, 0, 2, 1, 1)

        self.show_all()

        self.toolbar.set_visible(data.preferences.show_toolbar)
        
        Gtk.main()


class UnsavedDialog(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Unsaved Data")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Quit", Gtk.ResponseType.CLOSE)
        self.add_button("_Save and Quit", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>The database is currently unsaved.</b></span>")
        self.format_secondary_text("Do you want to save it before closing?")

    def show(self):
        response = self.run()

        state = 1

        if response == Gtk.ResponseType.CLOSE:
            state = 0
        elif response == Gtk.ResponseType.OK:
            data.database.save_database()
            state = 0

        self.destroy()

        return state


class QuitDialog(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Quit Editor")
        self.add_button("_Do Not Quit", Gtk.ResponseType.CANCEL)
        self.add_button("_Quit", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Quit the data editor?")

    def show(self):
        state = 1

        if self.run() == Gtk.ResponseType.OK:
            state = 0

        self.destroy()

        return state
