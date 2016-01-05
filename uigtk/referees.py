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
import uigtk.search
import uigtk.widgets


class Referees(uigtk.widgets.Grid):
    name = "Referees"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible, data.referees)
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.refereeedit = RefereeEdit()
        self.attach(self.refereeedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        refereeid = data.referees.add_referee()

        treeiter = self.search.liststore.insert(0, [refereeid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.treeview.scroll_to_cell(treepath)
        self.search.treeview.set_cursor_on_cell(treepath, None, None, False)

        self.refereeedit.clear_details()
        self.refereeedit.refereeid = refereeid

        self.refereeedit.entryName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected referee if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            refereeid = model[treeiter][0]

            if data.preferences.confirm_remove:
                referee = data.referees.get_referee_by_id(refereeid)

                dialog = uigtk.dialogs.RemoveItem("Referee", referee.name)

                if dialog.show():
                    data.referees.remove_referee(refereeid)
                    self.populate_data()
            else:
                data.referees.remove_referee(refereeid)
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
        Get referee selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            refereeid = model[treeiter][0]

            self.refereeedit.set_details(refereeid)
            self.refereeedit.set_sensitive(True)

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            data.window.menu.menuitemRemove.set_sensitive(True)
            data.window.toolbar.toolbuttonRemove.set_sensitive(True)
        else:
            data.window.menu.menuitemRemove.set_sensitive(False)
            data.window.toolbar.toolbuttonRemove.set_sensitive(False)
            self.refereeedit.clear_details()
            self.refereeedit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for refereeid, referee in data.referees.get_referees():
            self.search.liststore.append([refereeid, referee.name])

        self.search.activate_first_item()


class RefereeEdit(Referees, uigtk.widgets.Grid):
    refereeid = None

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

        actions = uigtk.interface.ActionButtons()
        actions.buttonSave.connect("clicked", self.on_save_clicked)
        self.attach(actions, 0, 1, 1, 1)

    def on_save_clicked(self, *args):
        '''
        Save current values into working data.
        '''
        referee = data.referees.get_referee_by_id(self.refereeid)

        referee.name = self.entryName.get_text()

        model, treeiter = Referees.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = referee.name

        model, treeiter = Referees.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Referees.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, refereeid):
        '''
        Update selected referee with details to be displayed.
        '''
        self.clear_details()

        self.refereeid = refereeid
        referee = data.referees.get_referee_by_id(refereeid)

        self.entryName.set_text(referee.name)

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")
