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
import re
import unicodedata

import data
import structures.nations
import uigtk.search
import uigtk.widgets


class Nations(uigtk.widgets.Grid):
    name = "Nations"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible, data.nations.get_nations())
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.nationedit = NationEdit()
        self.nationedit.set_sensitive(False)
        self.attach(self.nationedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        nationid = data.nations.add_nation()

        treeiter = self.search.liststore.insert(0, [nationid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.nationedit.clear_details()
        self.nationedit.nationid = nationid

        self.nationedit.entryName.grab_focus()

    def remove_item(self, *args):
        '''
        Query removal of selected nation if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            nationid = model[treeiter][0]

            if data.preferences.confirm_remove:
                nation = data.nations.get_nation_by_id(nationid)

                dialog = uigtk.dialogs.RemoveItem("Nation", nation.name)

                if dialog.show():
                    self.delete_nation(nationid)
            else:
                self.delete_nation(nationid)

    def delete_nation(self, nationid):
        '''
        Remove nation from working data and repopulate list.
        '''
        data.nations.remove_nation(nationid)

        self.populate_data()

    def filter_visible(self, model, treeiter, data):
        criteria = self.search.entrySearch.get_text()

        visible = True

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False
                break

        return visible

    def on_search_activated(self, *args):
        '''
        Apply search filter when entry is activated.
        '''
        self.search.treemodelfilter.refilter()

    def on_search_changed(self, entry):
        '''
        Reset search filter when last character is cleared.
        '''
        if entry.get_text_length() == 0:
            self.search.treemodelfilter.refilter()

    def on_search_cleared(self, entry, position, event):
        '''
        Reset search filter when clear icon is clicked.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")
            self.search.treemodelfilter.refilter()

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Get nation selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            nationid = model[treeiter][0]

            self.nationedit.set_details(nationid)
            self.nationedit.set_sensitive(True)
            data.window.toolbar.toolbuttonRemove.set_sensitive(True)
        else:
            self.nationedit.clear_details()
            self.nationedit.set_sensitive(False)
            data.window.toolbar.toolbuttonRemove.set_sensitive(False)

    def on_treeselection_changed(self, treeselection):
        '''
        Update visible details when selection is changed.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            data.window.menu.menuitemRemove.set_sensitive(True)
            data.window.toolbar.toolbuttonRemove.set_sensitive(True)
        else:
            data.window.menu.menuitemRemove.set_sensitive(False)
            data.window.toolbar.toolbuttonRemove.set_sensitive(False)
            self.nationedit.clear_details()
            self.nationedit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for nationid, nation in data.nations.get_nations():
            self.search.liststore.append([nationid, nation.name])

        self.search.activate_first_item()


class NationEdit(Nations, uigtk.widgets.Grid):
    nationid = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.attach(grid, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Name", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid.attach(self.entryName, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Denonym", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        label.set_mnemonic_widget(self.entryDenonym)
        grid.attach(self.entryDenonym, 1, 1, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonUpdate.connect("clicked", self.on_save_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_save_clicked(self, *args):
        '''
        Save updated details to working data, and update search list.
        '''
        nation = data.nations.get_nation_by_id(self.nationid)

        nation.name = self.entryName.get_text()
        nation.denonym = self.entryDenonym.get_text()

        model, treeiter = Nations.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = nation.name

        model, treeiter = Nations.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Nations.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, nationid):
        '''
        Load initial data when selection has changed.
        '''
        self.clear_details()

        self.nationid = nationid
        nation = data.nations.get_nation_by_id(nationid)

        self.entryName.set_text(nation.name)
        self.entryDenonym.set_text(nation.denonym)

    def clear_details(self):
        '''
        Clear nation fields to empty.
        '''
        self.entryName.set_text("")
        self.entryDenonym.set_text("")
