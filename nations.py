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
        self.attributes.buttonSave.connect("clicked", self.save_data)
        self.attributes.buttonReset.connect("clicked", self.reset_data)
        self.attach(self.attributes, 1, 0, 1, 1)

    def add_nation(self):
        '''
        Add the nation to the date structure, and append to search interface.
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

    def save_data(self, button):
        name = self.attributes.entryName.get_text()

        model, treeiter = self.search.treeselection.get_selected()
        liststore = model.get_model()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore[child_treeiter][1] = name
        self.attributes.save_fields()

        model, treeiter = self.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        self.search.treeview.scroll_to_cell(treepath)

    def reset_data(self, button):
        nation = data.nations[self.selected]

        self.attributes.entryName.set_text(nation.name)
        self.attributes.entryDenonym.set_text(nation.denonym)

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

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.Label("_Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Denonym")
        grid.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        label.set_mnemonic_widget(self.entryDenonym)
        grid.attach(self.entryDenonym, 1, 1, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 1, 1, 1)
        self.buttonReset = widgets.Button("_Reset")
        buttonbox.add(self.buttonReset)
        self.buttonSave = widgets.Button("_Save")
        buttonbox.add(self.buttonSave)

    def save_fields(self):
        nation = data.nations[self.nationid]

        nation.name = self.entryName.get_text()
        nation.denonym = self.entryDenonym.get_text()

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryDenonym.set_text("")
