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


class Nations(Gtk.Grid):
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
        self.search.treeview.connect("row-activated", self.nation_activated)
        self.search.treeselection.connect("changed", self.nation_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attributes.entryName.connect("focus-out-event", self.name_changed)
        self.attach(self.attributes, 1, 0, 1, 1)

    def add_nation(self):
        '''
        Add the nation to the date structure, and append to the search
        interface.
        '''
        nation = data.Nation()
        nationid = data.idnumbers.request_nationid()
        data.nations[nationid] = nation

        child_treeiter = self.search.liststore.append([nationid, ""])
        treeiter = self.search.treemodelsort.convert_child_iter_to_iter(child_treeiter)
        treepath = self.search.treemodelsort.get_path(treeiter[1])

        self.search.treeview.scroll_to_cell(treepath)
        self.search.treeview.set_cursor_on_cell(treepath, None, None, False)

        self.attributes.clear_fields()
        self.attributes.entryName.grab_focus()

    def name_changed(self, entry, event):
        name = entry.get_text()

        model, treeiter = self.search.treeselection.get_selected()
        liststore = model.get_model()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore[child_treeiter][1] = name
        data.nations[self.selected].name = name

        # Get new position of modified item
        model, treeiter = self.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        self.search.treeview.scroll_to_cell(treepath)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if criteria is not "":
            values = {}

            for nationid, nation in data.nations.items():
                for search in (nation.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[nationid] = nation

                        break

            self.populate_data(values=values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data(data.nations)

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(values=data.nations)

    def row_delete(self, treeview, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=2)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                nationid = [model[treepath][0] for treepath in treepath]

                keys = [player.nationality for player in data.players.values()]

                if [item for item in nationid if item in keys]:
                    dialogs.error(1)
                else:
                    for item in nationid:
                        del(data.nations[item])

                    data.unsaved = True

                    self.populate_data(values=data.nations)

    def nation_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()
        self.nationid = model[treepath][0]

        nation = data.nations[self.nationid]
        self.attributes.nationid = self.nationid

        self.attributes.entryName.set_text(nation.name)
        self.attributes.entryDenonym.set_text(nation.denonym)

    def nation_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            self.attributes.set_sensitive(True)
        else:
            self.selected = None
            self.attributes.clear_fields()
            self.attributes.set_sensitive(False)

    def populate_data(self, values):
        self.search.clear_data()

        for nationid, nation in values.items():
            self.search.liststore.append([nationid, nation.name])

    def run(self):
        self.populate_data(values=data.nations)
        self.show_all()

        treepath = Gtk.TreePath.new_first()
        self.search.treeselection.select_path(treepath)
        column = self.search.treeviewcolumn

        if self.search.treeselection.path_is_selected(treepath):
            self.search.treeview.row_activated(treepath, column)


class Attributes(Gtk.Grid):
    def __init__(self):
        self.nationid = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_sensitive(False)

        label = widgets.Label("_Name")
        self.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        self.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Denonym")
        self.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        label.set_mnemonic_widget(self.entryDenonym)
        self.attach(self.entryDenonym, 1, 1, 1, 1)

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryDenonym.set_text("")
