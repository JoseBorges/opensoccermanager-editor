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
import gi
import platform
import sqlite3

import data
import uigtk.widgets


class Dialog(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_resizable(False)
        self.set_title("Versions")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.vbox.set_border_width(5)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = uigtk.widgets.Label("Python Version", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("%s" % (platform.python_version()),
                                    leftalign=True)
        grid.attach(label, 1, 0, 1, 1)

        label = uigtk.widgets.Label("GTK+ Version", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        label = uigtk.widgets.Label("%i.%i.%i" % (Gtk.MAJOR_VERSION,
                                                  Gtk.MINOR_VERSION,
                                                  Gtk.MICRO_VERSION),
                                    leftalign=True)
        grid.attach(label, 1, 1, 1, 1)

        label = uigtk.widgets.Label("GObject Version", leftalign=True)
        grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("%i.%i.%i" % (gi.version_info),
                                    leftalign=True)
        grid.attach(label, 1, 2, 1, 1)

        label = uigtk.widgets.Label("Sqlite Version", leftalign=True)
        grid.attach(label, 0, 3, 1, 1)
        label = uigtk.widgets.Label("%s" % (sqlite3.version),
                                    leftalign=True)
        grid.attach(label, 1, 3, 1, 1)

        self.show_all()
        self.run()
        self.destroy()
