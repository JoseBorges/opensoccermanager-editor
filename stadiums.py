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

        attributes = stadium.attributes

        self.attributes.stadiumid = stadiumid

        self.attributes.populate_attributes()

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

        commonframe = widgets.CommonFrame("Attributes")
        self.attach(commonframe, 0, 1, 3, 1)

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        commonframe.insert(grid2)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 120)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        grid2.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreAttributes = Gtk.ListStore(int, str, str)

        self.treeview = Gtk.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.liststoreAttributes)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        #self.treeview.connect("row-activated", self.attribute_activated)
        self.treeselectionAttribute = self.treeview.get_selection()
        #self.treeselectionAttribute.connect("changed", self.attribute_changed)
        scrolledwindow.add(self.treeview)
        treeviewcolumn = widgets.TreeViewColumn(title="Year", column=1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Capacity", column=2)
        self.treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonAdd = Gtk.Button.new_from_icon_name("gtk-add", Gtk.IconSize.BUTTON)
        #buttonAdd.connect("clicked", self.add_attribute)
        buttonbox.add(buttonAdd)
        self.buttonEdit = Gtk.Button.new_from_icon_name("gtk-edit", Gtk.IconSize.BUTTON)
        self.buttonEdit.set_sensitive(False)
        #self.buttonEdit.connect("clicked", self.edit_attribute)
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove", Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        #self.buttonRemove.connect("clicked", self.remove_attribute)
        buttonbox.add(self.buttonRemove)
        grid2.attach(buttonbox, 1, 0, 1, 1)

    def populate_attributes(self):
        '''
        Populate attribute treeview with values for player id.
        '''
        self.liststoreAttributes.clear()

        stadium = data.stadiums[self.stadiumid]

        for attributeid, attribute in stadium.attributes.items():
            self.liststoreAttributes.append([attributeid,
                                             "%i" % (attribute.year),
                                             "%i" % (attribute.capacity)
                                            ])

    def clear_fields(self):
        self.entryName.set_text("")


class AttributeDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(parent)
        self.set_border_width(5)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.response_handler)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.vbox.add(notebook)

        # Stands
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        label = widgets.Label("_Capacity")
        notebook.append_page(grid, label)

        for count, item in enumerate(("North", "East", "South", "West", "North East", "North West", "South East", "South West")):
            label = widgets.Label("_%s" % (item))
            grid.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_increments(1000, 1000)
            spinbutton.set_snap_to_ticks(True)
            label.set_mnemonic_widget(spinbutton)

            if count < 4:
                spinbutton.set_range(0, 15000)
            else:
                spinbutton.set_range(0, 3000)

            grid.attach(spinbutton, 1, count, 1, 1)

            radiobuttonStanding = Gtk.RadioButton("_Standing")
            radiobuttonStanding.set_use_underline(True)
            grid.attach(radiobuttonStanding, 2, count, 1, 1)
            radiobuttonSeating = Gtk.RadioButton("_Seating")
            radiobuttonSeating.join_group(radiobuttonStanding)
            radiobuttonSeating.set_use_underline(True)
            grid.attach(radiobuttonSeating, 3, count, 1, 1)

            checkbutton = Gtk.CheckButton("_Roof")
            checkbutton.set_use_underline(True)
            grid.attach(checkbutton, 4, count, 1, 1)

            if count < 4:
                label = widgets.Label("_Box")
                grid.attach(label, 5, count, 1, 1)
                spinbutton = Gtk.SpinButton.new_with_range(0, 500, 250)
                label.set_mnemonic_widget(spinbutton)
                grid.attach(spinbutton, 6, count, 1, 1)

        # Buildings
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

    def display(self):
        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        self.destroy()
