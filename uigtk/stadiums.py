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
import structures.buildings
import structures.stadiums
import uigtk.dialogs
import uigtk.interface
import uigtk.search
import uigtk.widgets


class Stadiums(uigtk.widgets.Grid):
    name = "Stadiums"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search = uigtk.search.Search(data.stadiums.get_stadiums)
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
        stadium = data.stadiums.add_stadium()

        treeiter = self.search.liststore.insert(0, [stadium.stadiumid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.stadiumedit.clear_details()
        self.stadiumedit.stadium = stadium

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

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Get player selected and initiate details loading.
        '''
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()

        if treeiter:
            stadiumid = model[treeiter][0]

            stadium = data.stadiums.get_stadium_by_id(stadiumid)

            self.stadiumedit.set_details(stadium)
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
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.attach(grid, 0, 0, 1, 1)

        grid1 = uigtk.widgets.Grid()
        grid.attach(grid1, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Name", leftalign=True)
        grid1.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid1.attach(self.entryName, 1, 0, 1, 1)

        self.attributes = AttributeEdit()
        grid.attach(self.attributes, 0, 1, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonUpdate.connect("clicked", self.on_update_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_update_clicked(self, *args):
        '''
        Update current values into working data.
        '''
        self.stadium.name = self.entryName.get_text()

        model, treeiter = Stadiums.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = self.stadium.name

        model, treeiter = Stadiums.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Stadiums.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, stadium):
        '''
        Update selected stadium with details to be displayed.
        '''
        self.clear_details()

        self.stadium = stadium

        self.entryName.set_text(stadium.name)

        self.attributes.stadium = stadium
        self.attributes.populate_data()

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")

        self.attributes.liststore.clear()


class AttributeEdit(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, int, int)
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
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Capacity", column=2)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Buildings", column=3)
        self.attributes.treeview.append_column(treeviewcolumn)

        self.attributedialog = AttributeDialog()

    def on_add_clicked(self, *args):
        '''
        Display add dialog for new attribute.
        '''
        self.attributedialog.show(self.stadium, self.liststore)

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Display edit dialog for selected attribute.
        '''
        model, treeiter = self.attributes.treeselection.get_selected()
        treeiter1 = model.convert_iter_to_child_iter(treeiter)

        self.attributedialog.show(self.stadium, self.liststore, treeiter1)

        self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded stadium.
        '''
        dialog = uigtk.dialogs.RemoveAttribute(index=2)

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            treeiter1 = model.convert_iter_to_child_iter(treeiter)

            self.liststore.remove(treeiter1)

            data.unsaved = True

            self.populate_data()

    def on_row_activated(self, *args):
        '''
        Display edit dialog on activation of row.
        '''
        self.on_edit_clicked()

    def on_treeselection_changed(self, treeselection):
        '''
        Update visible details when selection is changed.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.attributes.buttonEdit.set_sensitive(True)
            self.attributes.buttonRemove.set_sensitive(True)
        else:
            self.attributes.buttonEdit.set_sensitive(False)
            self.attributes.buttonRemove.set_sensitive(False)

    def populate_data(self):
        self.liststore.clear()

        for attributeid, attribute in self.stadium.attributes.items():
            self.liststore.append([attributeid,
                                   attribute.year,
                                   attribute.get_capacity(),
                                   attribute.get_building_count()])


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
        self.vbox.set_spacing(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("_Year", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBoxText()
        self.comboboxYear.set_tooltip_text("Year to add attribute data.")
        self.comboboxYear.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        self.vbox.add(notebook)

        grid = uigtk.widgets.Grid()
        grid.set_border_width(5)
        label = uigtk.widgets.Label("_Stands")
        notebook.append_page(grid, label)

        names = structures.stadiums.StandNames()

        for count, name in enumerate(names.get_names()):
            label = uigtk.widgets.Label(name, leftalign=True)
            grid.attach(label, 0, count, 1, 1)

        self.main_stands = []
        self.corner_stands = []

        for count in range(0, 4):
            stand = MainStand()
            self.main_stands.append(stand)

            stand.capacity = Gtk.SpinButton()
            stand.capacity.set_range(0, 15000)
            stand.capacity.set_increments(1000, 1000)
            stand.capacity.set_value(0)
            stand.capacity.set_snap_to_ticks(True)
            stand.capacity.set_numeric(True)
            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            grid.attach(stand.capacity, 1, count, 1, 1)

            stand.roof = Gtk.CheckButton("Roof")
            stand.roof.set_sensitive(False)
            stand.roof.connect("toggled", stand.on_roof_changed)
            grid.attach(stand.roof, 2, count, 1, 1)

            stand.standing = Gtk.RadioButton("Standing")
            stand.standing.set_sensitive(False)
            grid.attach(stand.standing, 3, count, 1, 1)
            stand.seating = Gtk.RadioButton("Seating")
            stand.seating.set_sensitive(False)
            stand.seating.join_group(stand.standing)
            grid.attach(stand.seating, 4, count, 1, 1)

            label = uigtk.widgets.Label("Box", leftalign=True)
            grid.attach(label, 5, count, 1, 1)
            stand.box = Gtk.SpinButton()
            stand.box.set_range(0, 500)
            stand.box.set_increments(250, 250)
            stand.box.set_value(0)
            stand.box.set_snap_to_ticks(True)
            stand.box.set_numeric(True)
            stand.box.set_sensitive(False)
            grid.attach(stand.box, 6, count, 1, 1)

        for count in range(0, 4):
            stand = CornerStand()
            self.corner_stands.append(stand)

            stand.main.append(self.main_stands[count])

            if count + 1 == len(self.main_stands):
                stand.main.append(self.main_stands[0])
            else:
                stand.main.append(self.main_stands[count + 1])

            stand.capacity = Gtk.SpinButton()
            stand.capacity.set_range(0, 3000)
            stand.capacity.set_increments(1000, 1000)
            stand.capacity.set_value(0)
            stand.capacity.set_snap_to_ticks(True)
            stand.capacity.set_numeric(True)
            stand.capacity.set_sensitive(False)
            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            grid.attach(stand.capacity, 1, count + 4, 1, 1)

            stand.roof = Gtk.CheckButton("Roof")
            stand.roof.set_sensitive(False)
            grid.attach(stand.roof, 2, count + 4, 1, 1)

            stand.standing = Gtk.RadioButton("Standing")
            stand.standing.set_sensitive(False)
            grid.attach(stand.standing, 3, count + 4, 1, 1)
            stand.seating = Gtk.RadioButton("Seating")
            stand.seating.set_sensitive(False)
            stand.seating.join_group(stand.standing)
            grid.attach(stand.seating, 4, count + 4, 1, 1)

        for count, stand in enumerate(self.main_stands):
            stand.corners.append(self.corner_stands[count])
            stand.corners.append(self.corner_stands[count - 1 % len(self.corner_stands)])

        grid = uigtk.widgets.Grid()
        grid.set_border_width(5)
        label = uigtk.widgets.Label("_Buildings")
        notebook.append_page(grid, label)

        names = structures.buildings.BuildingNames()

        self.buildings = []

        for count, name in enumerate(names.get_names()):
            label = uigtk.widgets.Label("_%s" % (name), leftalign=True)
            grid.attach(label, 0, count, 1, 1)
            spinbutton = Gtk.SpinButton.new_with_range(0, 10, 1)
            label.set_mnemonic_widget(spinbutton)
            grid.attach(spinbutton, 1, count, 1, 1)
            self.buildings.append(spinbutton)

    def update_commit_button(self, *args):
        '''
        Update sensitivity of commit button on dialog.
        '''
        sensitive = False

        if self.comboboxYear.get_active_id():
            sensitive = True

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

    def load_attributes(self):
        '''
        Load attributes for given club and attribute.
        '''
        self.attribute = self.stadium.attributes[self.attributeid]

        self.comboboxYear.set_active_id(str(self.attribute.year))

        for count, stand in enumerate(self.main_stands):
            stand.capacity.set_value(self.attribute.main[count])
            stand.roof.set_active(self.attribute.roof[count])
            stand.seating.set_active(self.attribute.seating[count])
            stand.box.set_value(self.attribute.box[count])

        for count, stand in enumerate(self.corner_stands):
            stand.capacity.set_value(self.attribute.corner[count])
            stand.roof.set_active(self.attribute.roof[count])
            stand.seating.set_active(self.attribute.seating[count])

        for count, building in enumerate(self.buildings):
            building.set_value(self.attribute.buildings[count])

    def save_attributes(self):
        '''
        Save attributes for given stadium.
        '''
        if not self.treeiter:
            self.treeiter = self.model.append([self.attributeid, 0, 0, 0])

        self.model[self.treeiter][1] = int(self.comboboxYear.get_active_id())
        self.model[self.treeiter][2] = 0
        self.model[self.treeiter][3] = 0

    def clear_attributes(self):
        '''
        Reset data entry fields on close of dialog.
        '''
        self.comboboxYear.set_active(0)

        for stand in self.main_stands:
            stand.capacity.set_value(0)
            stand.roof.set_active(False)
            stand.standing.set_active(True)
            stand.box.set_value(0)

        for stand in self.corner_stands:
            stand.capacity.set_value(0)
            stand.roof.set_active(False)
            stand.standing.set_active(True)

        for building in self.buildings:
            building.set_value(0)

    def show(self, stadium, model, treeiter=None):
        self.stadium = stadium

        self.model = model
        self.treeiter = treeiter

        button = self.get_widget_for_response(Gtk.ResponseType.OK)

        if treeiter:
            self.set_title("Edit Attribute")
            button.set_label("_Edit")

            self.attributeid = model[treeiter][0]

            self.populate_years()

            self.load_attributes()
        else:
            self.set_title("Add Attribute")
            button.set_label("_Add")

            years = [attribute.year for attribute in stadium.attributes.values()]

            self.attributeid = stadium.add_attribute()

            self.populate_years(years)

        self.update_commit_button()

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            self.save_attributes()

        self.clear_attributes()
        self.hide()


class MainStand:
    def __init__(self):
        self.corners = []

    def add_adjacent_corner(self, stand):
        '''
        Add passed stand to corners list.
        '''
        self.corners.append(stand)

    def on_capacity_changed(self, spinbutton):
        '''
        Update widgets on change of capacity.
        '''
        sensitive = spinbutton.get_value_as_int() > 0

        if not self.roof.get_active():
            self.roof.set_sensitive(True)

        if not self.seating.get_active():
            self.standing.set_sensitive(True)
            self.seating.set_sensitive(True)

        if not sensitive:
            self.roof.set_active(False)
            self.standing.set_active(True)

        self.update_box_status()
        self.update_adjacent_status()

    def update_adjacent_status(self):
        '''
        Update adjacent stand status for capacity change.
        '''
        for stand in self.corners:
            stand.check_adjacent_capacity()

    def on_roof_changed(self, *args):
        '''
        Update box status when roof widget is toggled.
        '''
        self.update_box_status()

    def update_box_status(self):
        '''
        Update box widget based on capacity and roof status.
        '''
        sensitive = self.capacity.get_value_as_int() >= 4000 and self.roof.get_active()

        if not self.roof.get_active():
            self.box.set_value(0)

        if self.capacity.get_value_as_int() < 4000:
            self.box.set_value(0)

        self.box.set_sensitive(sensitive)


class CornerStand:
    def __init__(self):
        self.main = []

    def check_adjacent_capacity(self):
        '''
        Determine whether adjacent main stand capacities are enough.
        '''
        if self.main[0].capacity.get_value_as_int() < 8000 and self.main[1].capacity.get_value_as_int() < 8000:
            self.capacity.set_sensitive(False)
        else:
            self.capacity.set_sensitive(True)

    def on_capacity_changed(self, spinbutton):
        '''
        Update sensitivity of widgets and roof/standing values.
        '''
        sensitive = spinbutton.get_value_as_int() > 0
        self.roof.set_sensitive(sensitive)
        self.standing.set_sensitive(sensitive)
        self.seating.set_sensitive(sensitive)

        if not sensitive:
            self.roof.set_active(False)
            self.standing.set_active(True)
