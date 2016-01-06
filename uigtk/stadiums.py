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
import structures.stadiums
import uigtk.interface
import uigtk.search
import uigtk.widgets


class Stadiums(uigtk.widgets.Grid):
    name = "Stadiums"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible, data.stadiums.get_stadiums())
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.stadiumedit = StadiumEdit()
        self.stadiumedit.set_sensitive(False)
        self.attach(self.stadiumedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        stadiumid = data.stadiums.add_stadium()

        treeiter = self.search.liststore.insert(0, [stadiumid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.stadiumedit.clear_details()
        self.stadiumedit.stadiumid = stadiumid

        self.stadiumedit.entryName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected player if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            stadiumid = model[treeiter][0]

            if data.preferences.confirm_remove:
                stadium = data.stadiums.get_stadium_by_id(stadiumid)

                dialog = uigtk.dialogs.RemoveItem("Stadium", stadium.name)

                if dialog.show():
                    self.delete_stadium(stadiumid)
            else:
                self.delete_stadium(stadiumid)

    def delete_stadium(self, stadiumid):
        '''
        Remove stadium from working data and repopulate list.
        '''
        data.stadiums.remove_stadium(stadiumid)

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
        Get player selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            stadiumid = model[treeiter][0]

            self.stadiumedit.set_details(stadiumid)
            self.stadiumedit.set_sensitive(True)

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
            self.stadiumedit.clear_details()
            self.stadiumedit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for stadiumid, stadium in data.stadiums.get_stadiums():
            self.search.liststore.append([stadiumid, stadium.name])

        self.search.activate_first_item()


class StadiumEdit(uigtk.widgets.Grid):
    stadiumid = None

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
        self.actionbuttons.buttonSave.connect("clicked", self.on_save_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_save_clicked(self, *args):
        '''
        Save current values into working data.
        '''
        stadium = data.stadiums.get_stadium_by_id(self.stadiumid)

        stadium.name = self.entryName.get_text()

        model, treeiter = Stadiums.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = stadium.name

        model, treeiter = Stadiums.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Stadiums.search.treeview.scroll_to_cell(treepath)

    def set_details(self, stadiumid):
        '''
        Update selected stadium with details to be displayed.
        '''
        self.clear_details()

        StadiumEdit.stadiumid = stadiumid
        stadium = data.stadiums.get_stadium_by_id(stadiumid)

        self.entryName.set_text(stadium.name)

        self.attributes.stadiumid = stadiumid
        self.attributes.populate_data()

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")


class AttributeEdit(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, int)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.attributes = uigtk.interface.Attributes()
        self.attributes.treeview.set_model(treemodelsort)
        self.attributes.treeselection.connect("changed", self.on_treeselection_changed)
        self.attributes.buttonAdd.connect("clicked", self.on_add_clicked)
        self.attributes.buttonEdit.connect("clicked", self.on_edit_clicked)
        self.attributes.buttonRemove.connect("clicked", self.on_remove_clicked)
        self.attach(self.attributes, 0, 0, 1, 1)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Year", column=1)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Capacity", column=2)
        self.attributes.treeview.append_column(treeviewcolumn)
        #treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Buildings", column=3)
        #self.attributes.treeview.append_column(treeviewcolumn)

        self.stadiumdialog = AttributeDialog()

    def on_add_clicked(self, *args):
        self.stadiumdialog.show()

        self.populate_data()

    def on_edit_clicked(self, *args):
        self.stadiumdialog.show()

        self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded stadium.
        '''
        dialog = uigtk.dialogs.RemoveAttribute()

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            attributeid = model[treeiter][0]

            stadium = data.stadiums.get_stadium_by_id(self.stadiumid)
            del stadium.attributes[attributeid]

            data.unsaved = True

            self.populate_data()

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.attributes.buttonEdit.set_sensitive(True)
            self.attributes.buttonRemove.set_sensitive(True)
        else:
            self.attributes.buttonEdit.set_sensitive(False)
            self.attributes.buttonRemove.set_sensitive(False)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        self.on_edit_clicked()

    def populate_data(self):
        stadium = data.stadiums.get_stadium_by_id(self.stadiumid)

        self.liststore.clear()

        for attributeid, attribute in stadium.attributes.items():
            self.liststore.append([attributeid,
                                   attribute.year,
                                   attribute.get_capacity()])


class AttributeDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Add Attribute")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Add", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        self.capacity = []
        self.box = []

        for count, name in enumerate(("North", "West", "South", "East"), start=1):
            label = uigtk.widgets.Label(name, leftalign=True)
            grid.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton.new_with_range(0, 15000, 1000)
            spinbutton.set_snap_to_ticks(True)
            self.capacity.append(spinbutton)
            grid.attach(spinbutton, 1, count, 1, 1)

            radiobuttonStanding = uigtk.widgets.RadioButton("_Standing")
            grid.attach(radiobuttonStanding, 2, count, 1, 1)

            radiobuttonSeating = uigtk.widgets.RadioButton("_Seating")
            radiobuttonSeating.join_group(radiobuttonStanding)
            grid.attach(radiobuttonSeating, 3, count, 1, 1)

            checkbuttonRoof = uigtk.widgets.CheckButton("_Roof")
            grid.attach(checkbuttonRoof, 4, count, 1, 1)

            label = uigtk.widgets.Label("_Executive Box", leftalign=True)
            grid.attach(label, 5, count, 1, 1)

            spinbutton = Gtk.SpinButton.new_with_range(0, 500, 250)
            spinbutton.set_snap_to_ticks(True)
            self.box.append(spinbutton)
            grid.attach(spinbutton, 6, count, 1, 1)

        for count, name in enumerate(("North West", "North East", "South West", "South East"), start=5):
            label = uigtk.widgets.Label(name, leftalign=True)
            grid.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton.new_with_range(0, 3000, 1000)
            spinbutton.set_snap_to_ticks(True)
            self.capacity.append(spinbutton)
            grid.attach(spinbutton, 1, count, 1, 1)

    def show(self, stadiumid, attributeid=None):
        self.stadiumid = stadiumid
        self.attributeid = attributeid

        button = self.get_widget_for_response(Gtk.ResponseType.OK)

        if attributeid:
            self.set_title("Edit Attribute")
            button.set_label("_Edit")

            self.load_year_values()

            self.load_attributes()
        else:
            self.set_title("Add Attribute")
            button.set_label("_Add")

            stadium = data.stadiums.get_stadium_by_id(stadiumid)
            years = [attribute.year for attribute in stadium.attributes.values()]

            self.load_year_values(years)

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            pass

        self.hide()

        return
