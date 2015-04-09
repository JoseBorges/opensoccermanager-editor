#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import re
import unicodedata

import data
import dialogs
import interface
import menu
import widgets


class Stadiums(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.search.searchentry.connect("activate", self.search_activated)
        self.search.searchentry.connect("changed", self.search_changed)
        self.search.searchentry.connect("icon-press", self.search_cleared)
        self.search.treeview.connect("row-activated", self.row_activated)
        self.search.treeselection.connect("changed", self.stadium_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attributes.entryName.connect("focus-out-event", self.name_changed)
        self.attach(self.attributes, 1, 0, 1, 1)

    def name_changed(self, entry, event):
        name = entry.get_text()

        model, treeiter = self.search.treeselection.get_selected()
        liststore = model.get_model()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore[child_treeiter][1] = name
        data.stadiums[self.selected].name = name

        # Get new position of modified item
        model, treeiter = self.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        self.search.treeview.scroll_to_cell(treepath)

    def stadium_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            self.attributes.set_sensitive(True)
        else:
            self.selected = None
            self.attributes.clear_fields()
            self.attributes.set_sensitive(False)

    def row_activated(self, treeview=None, treepath=None, treeviewcolumn=None):
        model = treeview.get_model()
        stadiumid = model[treepath][0]

        stadium = data.stadiums[stadiumid]

        self.attributes.entryName.set_text(stadium.name)

    def row_delete(self, treeview=None, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=3)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                stadiumid = [model[treepath][0] for treepath in treepath]

                keys = [club.stadium for club in data.clubs.values()]

                if [item for item in stadiumid if item in keys]:
                    dialogs.error(2)
                else:
                    for item in stadium:
                        del(data.stadiums[item])

                    data.unsaved = True

                    self.populate()

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if criteria is not "":
            values = {}

            for stadiumid, stadium in data.stadiums.items():
                for search in (stadium.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[stadiumid] = stadium

                        break

            self.populate_data(values=values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data(data.stadiums)

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(values=data.stadiums)

    def populate_data(self, values):
        self.search.clear_data()

        for stadiumid, stadium in values.items():
            self.search.liststore.append([stadiumid, stadium.name])

    def run(self):
        self.populate_data(values=data.stadiums)
        self.show_all()

        treepath = Gtk.TreePath.new_first()
        self.search.treeselection.select_path(treepath)
        column = self.search.treeviewcolumn

        if self.search.treeselection.path_is_selected(treepath):
            self.search.treeview.row_activated(treepath, column)


class Attributes(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        grid1 = Gtk.Grid()
        grid1.set_column_spacing(5)
        self.attach(grid1, 0, 0, 2, 1)

        label = widgets.Label("_Name")
        grid1.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid1.attach(self.entryName, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.attach(notebook, 0, 1, 3, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        label = widgets.Label("_Capacity")
        notebook.append_page(grid, label)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        label = widgets.Label("_Buildings")
        notebook.append_page(grid, label)

        label = widgets.Label("Programme Vendor")
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.Label("Stall")
        grid.attach(label, 0, 1, 1, 1)
        label = widgets.Label("Small Shop")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.Label("Large Shop")
        grid.attach(label, 0, 3, 1, 1)
        label = widgets.Label("Burger Bar")
        grid.attach(label, 0, 4, 1, 1)
        label = widgets.Label("Bar")
        grid.attach(label, 0, 5, 1, 1)
        label = widgets.Label("Cafe")
        grid.attach(label, 0, 6, 1, 1)
        label = widgets.Label("Restaurant")
        grid.attach(label, 0, 7, 1, 1)

        self.buildings = []

        for count in range(8):
            spinbutton = Gtk.SpinButton.new_with_range(0, 8, 1)
            grid.attach(spinbutton, 1, count, 1, 1)
            self.buildings.append(spinbutton)

    def clear_fields(self):
        self.entryName.set_text("")
