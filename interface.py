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


from gi.repository import Gtk
import re
import unicodedata

import widgets


class Search(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(200, -1)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str)
        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = Gtk.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_model(self.treemodelsort)
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeview.set_activate_on_single_click(True)
        scrolledwindow.add(self.treeview)

        self.treeselection = self.treeview.get_selection()

        self.treeviewcolumn = widgets.TreeViewColumn(None, column=1)
        self.treeview.append_column(self.treeviewcolumn)

        self.searchentry = Gtk.SearchEntry()
        self.attach(self.searchentry, 0, 1, 1, 1)

    def clear_data(self):
        self.liststore.clear()
