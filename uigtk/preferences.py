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
import uigtk.widgets


class Preferences(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_title("Preferences")
        self.set_transient_for(data.window)
        self.set_resizable(False)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        frame = uigtk.widgets.CommonFrame("Interface")
        self.vbox.add(frame)

        checkbutton = uigtk.widgets.CheckButton("Display Confirmation Dialog When _Quitting")
        checkbutton.set_active(data.preferences.confirm_quit)
        checkbutton.set_tooltip_text("Ask user to confirm when exiting data editor.")
        checkbutton.connect("toggled", self.on_quit_toggled)
        frame.grid.attach(checkbutton, 0, 0, 1, 1)

        checkbutton = uigtk.widgets.CheckButton("Display Confirmation Dialog When _Removing Items")
        checkbutton.set_active(data.preferences.confirm_remove)
        checkbutton.set_tooltip_text("Ask user to confirm removal of data.")
        checkbutton.connect("toggled", self.on_remove_toggled)
        frame.grid.attach(checkbutton, 0, 1, 1, 1)

        checkbutton = uigtk.widgets.CheckButton("Show _Toolbar")
        checkbutton.set_active(data.preferences.show_toolbar)
        checkbutton.set_tooltip_text("Toggle visibility of the toolbar.")
        checkbutton.connect("toggled", self.on_toolbar_toggled)
        frame.grid.attach(checkbutton, 0, 2, 1, 1)

        self.show_all()

    def on_quit_toggled(self, checkbutton):
        '''
        Toggle whether quit confirmation dialog is shown.
        '''
        data.preferences.confirm_quit = checkbutton.get_active()
        data.preferences.write_to_config()

    def on_remove_toggled(self, checkbutton):
        '''
        Toggle whether remove confirmation dialog is shown.
        '''
        data.preferences.confirm_remove = checkbutton.get_active()
        data.preferences.write_to_config()

    def on_toolbar_toggled(self, checkbutton):
        '''
        Toggle visibility of toolbar in interface.
        '''
        data.preferences.show_toolbar = checkbutton.get_active()
        data.window.toolbar.set_visible(data.preferences.show_toolbar)
        data.preferences.write_to_config()

    def on_response(self, *args):
        self.destroy()
