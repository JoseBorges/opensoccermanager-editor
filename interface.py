#!/usr/bin/env python3

from gi.repository import Gtk
import re
import unicodedata

import data
import widgets


class Search(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(200, -1)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = Gtk.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_model(treemodelsort)
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
