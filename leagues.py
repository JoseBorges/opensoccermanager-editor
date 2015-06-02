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
        self.search.treeview.connect("row-activated", self.league_activated)
        self.search.treeselection.connect("changed", self.league_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attach(self.attributes, 1, 0, 1, 1)

    def league_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()
        self.leagueid = model[treepath][0]

        league = data.leagues[self.leagueid]
        self.attributes.leagueid = self.leagueid

        self.attributes.entryName.set_text(league.name)

        self.attributes.populate_attributes()

    def league_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            widgets.toolbuttonRemove.set_sensitive(True)
            self.attributes.set_sensitive(True)
        else:
            self.selected = None
            widgets.toolbuttonRemove.set_sensitive(False)
            self.attributes.clear_fields()
            self.attributes.set_sensitive(False)

    def populate_data(self, values):
        self.search.clear_data()

        for leagueid, league in values.items():
            self.search.liststore.append([leagueid, league.name])

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
            scrolledwindow.set_vexpand(True)
            scrolledwindow.set_hexpand(True)
            self.attach(scrolledwindow, 0, 0, 1, 1)

            self.liststore = Gtk.ListStore(str)

            treemodelsort = Gtk.TreeModelSort(self.liststore)
            treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

            treeview = Gtk.TreeView()
            treeview.set_model(treemodelsort)
            treeview.set_headers_visible(False)
            scrolledwindow.add(treeview)

            cellrenderertext = Gtk.CellRendererText()
            treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=0)
            treeview.append_column(treeviewcolumn)

            self.show_all()

        def add_item(self, data):
            self.liststore.append([data])

    def __init__(self):
        self.liststoreClubs = Gtk.ListStore(str)

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.Label("Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        grid.attach(self.entryName, 1, 0, 1, 1)

        self.notebook = Gtk.Notebook()
        self.attach(self.notebook, 0, 1, 1, 1)

    def clear_fields(self):
        self.entryName.set_text("")

    def populate_attributes(self):
        pages = self.notebook.get_n_pages()

        self.notebook.remove_page(0)

        for count in range(0, pages):
            self.notebook.remove_page(count)

        clubs = {}

        for year in data.years:
            clubs[year] = []

        for year, items in clubs.items():
            for club in data.clubs.values():
                for attribute in club.attributes.values():
                    if attribute.league == self.leagueid and attribute.year == year:
                        items.append(club.name)

        for year, items in clubs.items():
            if len(items) > 0:
                club = self.Clubs()

                for item in items:
                    club.add_item(item)

                label = Gtk.Label("%i" % (year))
                self.notebook.append_page(club, label)
