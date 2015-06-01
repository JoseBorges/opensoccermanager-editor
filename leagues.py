#!/usrsel/bin/env python3

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


from gi.repository import Gtk

import data
import interface
import widgets


class Leagues(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attach(self.attributes, 1, 0, 1, 1)

    def populate_data(self, values):
        self.search.clear_data()

        for leagueid, league in values.items():
            self.search.liststore.append([leagueid, league.name])
            print(league.name)

    def run(self):
        self.populate_data(values=data.leagues)
        self.show_all()


class Attributes(Gtk.Grid):
    class Clubs(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            scrolledwindow = Gtk.ScrolledWindow()
            self.attach(scrolledwindow, 0, 0, 1, 1)

            treeview = Gtk.TreeView()
            treeview.set_headers_visible(False)
            scrolledwindow.add(treeview)

            cellrenderertext = Gtk.CellRendererText()
            treeviewcolumn = Gtk.TreeViewColumn("", cellrenderer, text=0)
            treeview.append_column(treeviewcolumn)

    def __init__(self):
        self.liststoreClubs = Gtk.ListStore(str)

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = widgets.Label("Name")
        self.attach(label, 0, 0, 1, 1)
        entryName = Gtk.Entry()
        self.attach(entryName, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 1, 3, 1)

    def run(self):
        print("Hit")
