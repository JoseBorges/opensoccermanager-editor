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


from gi.repository import Gtk

import data


class NewDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("New Database")
        self.set_do_overwrite_confirmation(True)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.set_current_name("New Database")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Create", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

    def show(self):
        filename = None

        if self.run() == Gtk.ResponseType.OK:
            filename = self.get_filename()

        self.destroy()

        return filename


class OpenDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Open Database")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Open", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

    def show(self):
        filename = None

        if self.run() == Gtk.ResponseType.OK:
            filename = self.get_filename()

        self.destroy()

        return filename


class SaveDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Save Database")
        self.set_do_overwrite_confirmation(True)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.on_response)

    def on_response(self, dialog, response):
        self.destroy()
