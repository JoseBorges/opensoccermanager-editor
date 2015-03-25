#!/usr/bin/env python3

from gi.repository import Gtk
import re
import unicodedata

import data
import widgets


class Search(Gtk.Grid):
    def __init__(self):
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

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        scrolledwindow.add(treeview)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.treeselection_changed)
        treeviewcolumn = widgets.TreeViewColumn(None, column=1)
        treeview.append_column(treeviewcolumn)

        searchentry = Gtk.SearchEntry()
        searchentry.connect("activate", self.search_activated)
        searchentry.connect("changed", self.search_changed)
        searchentry.connect("icon-press", self.search_cleared)
        self.attach(searchentry, 0, 1, 1, 1)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        data = self.data

        if criteria is not "":
            values = {}

            for itemid, item in data.items():
                for search in (item.name,):
                    search = ''.join((c for c in unicodedata.normalize('NFD', search) if unicodedata.category(c) != 'Mn'))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[itemid] = item

                        break

            self.populate_data(data=values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data()

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data()

    def treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]

            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None

            widgets.toolbuttonRemove.set_sensitive(False)

    def populate_data(self, data=None):
        self.liststore.clear()

        if data is None:
            data = self.data

        for itemid, item in data.items():
            self.liststore.append([itemid, item.name])
