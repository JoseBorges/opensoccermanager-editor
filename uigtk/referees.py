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
import uigtk.dialogs
import uigtk.interface
import uigtk.search
import uigtk.widgets


class Referees(uigtk.widgets.Grid):
    name = "Referees"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        Referees.search = uigtk.search.Search(data.referees.get_referees)
        Referees.search.treeview.connect("row-activated", self.on_row_activated)
        Referees.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.attach(Referees.search, 0, 0, 1, 1)

        self.refereeedit = RefereeEdit()
        self.refereeedit.set_sensitive(False)
        self.attach(self.refereeedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        referee = data.referees.add_referee()

        treeiter = Referees.search.liststore.insert(0, [referee.refereeid, ""])
        treeiter1 = Referees.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = Referees.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = Referees.search.treemodelsort.get_path(treeiter2[1])

        Referees.search.activate_row(treepath)

        self.refereeedit.clear_details()
        self.refereeedit.referee = referee

        self.refereeedit.entryName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected referee if dialog enabled.
        '''
        model, treeiter = Referees.search.treeselection.get_selected()

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

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Get referee selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            refereeid = model[treeiter][0]

            referee = data.referees.get_referee_by_id(refereeid)

            self.refereeedit.set_details(referee)
            self.refereeedit.set_sensitive(True)

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
            self.refereeedit.clear_details()
            self.refereeedit.set_sensitive(False)

    def populate_data(self):
        Referees.search.liststore.clear()

        for refereeid, referee in data.referees.get_referees():
            Referees.search.liststore.append([refereeid, referee.name])

        Referees.search.activate_first_item()


class RefereeEdit(uigtk.widgets.Grid):
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
        grid.attach(self.attributes, 0, 1, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonUpdate.connect("clicked", self.on_update_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_update_clicked(self, *args):
        '''
        Update current values into working data.
        '''
        self.referee.name = self.entryName.get_text()

        model, treeiter = Referees.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = self.referee.name

        model, treeiter = Referees.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Referees.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, referee):
        '''
        Update selected referee with details to be displayed.
        '''
        self.clear_details()

        self.entryName.set_text(referee.name)

        self.attributes.referee = referee
        self.attributes.populate_data()

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")


class AttributeEdit(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.attributes = uigtk.interface.Attributes()
        self.attributes.treeview.set_model(treemodelsort)
        self.attributes.treeview.connect("row-activated", self.on_row_activated)
        self.attributes.treeselection.connect("changed", self.on_treeselection_changed)
        self.attributes.buttonAdd.connect("clicked", self.on_add_clicked)
        self.attributes.buttonEdit.connect("clicked", self.on_edit_clicked)
        self.attributes.buttonRemove.connect("clicked", self.on_remove_clicked)
        self.attach(self.attributes, 0, 0, 1, 1)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Year", column=1)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        self.attributes.treeview.append_column(treeviewcolumn)

        self.attributedialog = AttributeDialog()

    def on_add_clicked(self, *args):
        '''
        Display add dialog for new attribute.
        '''
        self.attributedialog.show(self.referee, self.liststore)

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Display edit dialog for selected attribute.
        '''
        model, treeiter = self.attributes.treeselection.get_selected()
        attributeid = model[treeiter][0]

        self.attributedialog.show(self.referee, attributeid)

        self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded club.
        '''
        dialog = uigtk.dialogs.RemoveAttribute(index=4)

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            attributeid = model[treeiter][0]

            referee = data.referees.get_referee_by_id(self.referee.refereeid)
            del referee.attributes[attributeid]

            data.unsaved = True

            self.populate_data()

    def on_row_activated(self, *args):
        '''
        Display edit dialog on activation of row.
        '''
        self.on_edit_clicked()

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.attributes.buttonEdit.set_sensitive(True)
            self.attributes.buttonRemove.set_sensitive(True)
        else:
            self.attributes.buttonEdit.set_sensitive(False)
            self.attributes.buttonRemove.set_sensitive(False)

    def populate_data(self):
        self.liststore.clear()

        for attributeid, attribute in self.referee.attributes.items():
            league = data.leagues.get_league_by_id(attribute.league)

            self.liststore.append([attributeid,
                                   attribute.year,
                                   attribute.league,
                                   league.name])


class AttributeDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Add Attribute")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Add", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        grid.set_border_width(5)
        self.vbox.add(grid)

        label = uigtk.widgets.Label("_Year", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBoxText()
        self.comboboxYear.set_tooltip_text("Year to add attribute data.")
        self.comboboxYear.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_League", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxLeague = Gtk.ComboBoxText()
        self.comboboxLeague.set_tooltip_text("League selection for this referee.")
        self.comboboxLeague.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.comboboxLeague)
        grid.attach(self.comboboxLeague, 1, 1, 1, 1)

    def update_commit_button(self, *args):
        '''
        Update sensitivity of commit button on dialog.
        '''
        sensitive = False

        if self.comboboxYear.get_active_id():
            sensitive = True

        if sensitive:
            if self.comboboxLeague.get_active_id():
                sensitive = True
            else:
                sensitive = False

        self.set_response_sensitive(Gtk.ResponseType.OK, sensitive)

    def populate_years(self, years=None):
        '''
        Customise available year values for add and edit actions.
        '''
        self.comboboxYear.remove_all()

        if years:
            added = False

            for year in data.years.get_years():
                if year not in years:
                    self.comboboxYear.append(str(year), str(year))
                    added = True

            self.comboboxYear.set_sensitive(added)
            self.comboboxYear.set_active(0)
        else:
            for year in data.years.get_years():
                self.comboboxYear.append(str(year), str(year))

    def populate_leagues(self):
        '''
        List selection of leagues available for referee.
        '''
        self.comboboxLeague.remove_all()

        for leagueid, league in data.leagues.get_leagues():
            self.comboboxLeague.append(str(leagueid), league.name)

    def load_attributes(self):
        '''
        Load attributes for given club and attribute.
        '''
        self.referee = data.referees.get_referee_by_id(self.refereeid)
        self.attribute = self.referee.attributes[self.attributeid]

        self.comboboxYear.set_active_id(str(self.attribute.year))
        self.comboboxLeague.set_active_id(str(self.attribute.league))

    def save_attributes(self):
        '''
        Save attributes for given referee.
        '''
        if not self.treeiter:
            self.attributeid = self.referee.add_attribute()
            self.treeiter = self.model.append([self.attributeid, 0, 0, ""])

        self.model[self.treeiter][1] = int(self.comboboxYear.get_active_id())
        self.model[self.treeiter][2] = self.leagueid
        self.model[self.treeiter][3] = self.league.name

    def clear_attributes(self):
        '''
        Reset data entry fields on close of dialog.
        '''
        self.leagueid = None
        self.league = None

    def show(self, referee, model, treeiter=None):
        self.referee = referee

        self.model = model
        self.treeiter = treeiter

        button = self.get_widget_for_response(Gtk.ResponseType.OK)

        if treeiter:
            self.set_title("Edit Attribute")
            button.set_label("_Edit")

            self.attributeid = model[treeiter][0]

            self.populate_years()
            self.populate_leagues()

            self.load_attributes()
        else:
            self.set_title("Add Attribute")
            button.set_label("_Add")

            years = [attribute.year for attribute in referee.attributes.values()]

            self.attributeid = None

            self.leagueid = None
            self.league = None

            self.populate_years(years)
            self.populate_leagues()

        self.update_commit_button()

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            self.save_attributes()

        self.clear_attributes()
        self.hide()
