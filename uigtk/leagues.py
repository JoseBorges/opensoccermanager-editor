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


class Leagues(uigtk.widgets.Grid):
    name = "Leagues"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible, data.leagues.get_leagues())
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.leagueedit = LeagueEdit()
        self.leagueedit.set_sensitive(False)
        self.attach(self.leagueedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        leagueid = data.leagues.add_league()

        treeiter = self.search.liststore.insert(0, [leagueid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.leagueedit.clear_details()
        self.leagueedit.leagueid = leagueid

        self.leagueedit.entryName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected player if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            leagueid = model[treeiter][0]
            league = data.leagues.get_league_by_id(leagueid)

            if not league.can_remove():
                if data.preferences.confirm_remove:
                    dialog = uigtk.dialogs.RemoveItem("League", league.name)

                    if dialog.show():
                        self.delete_league(leagueid)
                else:
                    self.delete_league(leagueid)
            else:
                uigtk.dialogs.LeagueKeyError(league.name)

    def delete_league(self, leagueid):
        '''
        Remove given league id from working data and repopulate list.
        '''
        data.leagues.remove_league(leagueid)

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
        Get league selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            leagueid = model[treeiter][0]

            self.leagueedit.set_details(leagueid)
            self.leagueedit.set_sensitive(True)

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
            self.leagueedit.clear_details()
            self.leagueedit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for leagueid, league in data.leagues.get_leagues():
            self.search.liststore.append([leagueid, league.name])

        self.search.activate_first_item()


class LeagueEdit(Leagues, uigtk.widgets.Grid):
    leagueid = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.attach(grid, 0, 0, 1, 1)

        grid2 = uigtk.widgets.Grid()
        grid.attach(grid2, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Name", leftalign=True)
        grid2.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid2.attach(self.entryName, 1, 0, 1, 1)

        self.attributes = AttributeEdit()
        grid.attach(self.attributes, 0, 2, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonSave.connect("clicked", self.on_save_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_save_clicked(self, *args):
        '''
        Save current values into working data.
        '''
        league = data.leagues.get_league_by_id(self.leagueid)

        league.name = self.entryName.get_text()

        model, treeiter = Leagues.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = league.name

        model, treeiter = Leagues.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Leagues.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, leagueid):
        '''
        Update selected player with details to be displayed.
        '''
        self.clear_details()

        LeagueEdit.leagueid = leagueid
        league = data.leagues.get_league_by_id(leagueid)

        self.entryName.set_text(league.name)

        self.attributes.leagueid = leagueid
        self.attributes.populate_data()

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")

        self.attributes.liststore.clear()


class AttributeEdit(LeagueEdit, uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, int)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.attributes = uigtk.interface.Attributes()
        self.attributes.treeview.set_model(treemodelsort)
        self.attributes.treeview.connect("row-activated", self.on_row_activated)
        self.attributes.treeselection.connect("changed", self.on_treeselection_changed)
        self.attributes.buttonAdd.connect("clicked", self.on_add_clicked)
        self.attributes.buttonRemove.connect("clicked", self.on_remove_clicked)
        self.attach(self.attributes, 0, 0, 1, 1)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Year", column=1)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Clubs", column=2)
        self.attributes.treeview.append_column(treeviewcolumn)

        self.attributedialog = AttributeDialog()

    def on_add_clicked(self, *args):
        '''
        Display add dialog for new attribute.
        '''
        self.attributedialog.show(LeagueEdit.leagueid)

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Display edit dialog for selected attribute.
        '''
        model, treeiter = self.attributes.treeselection.get_selected()
        attributeid = model[treeiter][0]

        self.attributedialog.show(LeagueEdit.leagueid, attributeid)

        self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded league.
        '''
        dialog = uigtk.dialogs.RemoveAttribute(index=3)

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            attributeid = model[treeiter][0]

            league = data.leagues.get_league_by_id(LeagueEdit.leagueid)
            del league.attributes[attributeid]

            data.unsaved = True

            self.populate_data()

    def on_row_activated(self, *args):
        self.on_edit_clicked()

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            attributeid = model[treeiter][0]
            self.attributes.buttonEdit.set_sensitive(True)
            self.attributes.buttonRemove.set_sensitive(True)
        else:
            self.attributes.buttonEdit.set_sensitive(False)
            self.attributes.buttonRemove.set_sensitive(False)

    def populate_data(self):
        league = data.leagues.get_league_by_id(self.leagueid)

        self.liststore.clear()

        for attributeid, attribute in league.attributes.items():
            self.liststore.append([attributeid,
                                   attribute.year,
                                   attribute.get_club_count()])


class AttributeDialog(Gtk.Dialog):
    def __init__(self, clubid=None, attributeid=None):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_default_size(-1, 350)
        self.set_modal(True)
        self.set_title("Add Attribute")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Add", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("_Year", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBoxText()
        self.comboboxYear.set_tooltip_text("Year to add attribute data.")
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        for year in data.years.get_years():
            self.comboboxYear.append(str(year), str(year))

        self.comboboxYear.set_active(0)

        notebook = Gtk.Notebook()
        self.vbox.add(notebook)

        self.clublist = uigtk.interface.ItemList()
        self.clublist.set_border_width(5)
        notebook.append_page(self.clublist, uigtk.widgets.Label("_Clubs"))

        self.refereelist = uigtk.interface.ItemList()
        self.refereelist.set_border_width(5)
        notebook.append_page(self.refereelist, uigtk.widgets.Label("_Referees"))

    def load_attributes(self):
        '''
        Load attributes for given club and attribute.
        '''
        self.league = data.leagues.get_league_by_id(self.leagueid)
        self.attribute = self.league.attributes[self.attributeid]

        for clubid, club in data.clubs.get_clubs():
            for attributeid, attribute in club.attributes.items():
                if attribute.league == self.leagueid:
                    if attribute.year == self.attribute.year:
                        self.clublist.liststore.append([clubid, club.name])

    def clear_attributes(self):
        '''
        Reset data entry fields on close of dialog.
        '''
        self.clublist.liststore.clear()
        self.refereelist.liststore.clear()

    def show(self, leagueid, attributeid=None):
        self.leagueid = leagueid
        self.attributeid = attributeid

        button = self.get_widget_for_response(Gtk.ResponseType.OK)

        if attributeid:
            self.set_title("Edit Attribute")
            button.set_label("_Edit")

            self.load_attributes()
        else:
            self.set_title("Add Attribute")
            button.set_label("_Add")

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            pass

        self.clear_attributes()
        self.hide()
