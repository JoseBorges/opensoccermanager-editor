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
        model, treeiter = self.treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]

            widgets.window.menuitemRemove.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None

            widgets.window.menuitemRemove.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

    def clear_data(self):
        self.liststore.clear()
