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

import data
import uigtk.widgets


class Attributes(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self)
        self.set_title("Attributes")

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.treeview = Gtk.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        scrolledwindow.add(self.treeview)

        self.treeselection = self.treeview.get_selection()

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.grid.attach(buttonbox, 1, 0, 1, 1)

        self.buttonAdd = Gtk.Button.new_from_icon_name("gtk-add",
                                                       Gtk.IconSize.BUTTON)
        self.buttonAdd.set_tooltip_text("Add new attribute for player.")
        buttonbox.add(self.buttonAdd)
        self.buttonEdit = Gtk.Button.new_from_icon_name("gtk-edit",
                                                        Gtk.IconSize.BUTTON)
        self.buttonEdit.set_sensitive(False)
        self.buttonEdit.set_tooltip_text("Edit selected attribute for player.")
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove",
                                                          Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.set_tooltip_text("Remove selected attribute for player.")
        buttonbox.add(self.buttonRemove)


class ActionButtons(Gtk.ButtonBox):
    def __init__(self):
        Gtk.ButtonBox.__init__(self)
        self.set_spacing(5)
        self.set_layout(Gtk.ButtonBoxStyle.END)

        self.buttonUpdate = uigtk.widgets.Button("_Update")
        self.buttonUpdate.set_tooltip_text("Update values into current working data.")
        key, mod = Gtk.accelerator_parse("<Control>U")
        self.buttonUpdate.add_accelerator("activate",
                                          data.window.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        self.add(self.buttonUpdate)


class ItemList(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        grid = uigtk.widgets.Grid()
        self.add(grid)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = uigtk.widgets.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_visible(False)
        treeview.treeselection.connect("changed", self.on_treeselection_changed)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        treeview.append_column(treeviewcolumn)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        grid.attach(buttonbox, 0, 1, 1, 1)

        self.buttonAdd = Gtk.Button.new_from_icon_name("gtk-add",
                                                       Gtk.IconSize.BUTTON)
        buttonbox.add(self.buttonAdd)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove",
                                                          Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        buttonbox.add(self.buttonRemove)

    def on_treeselection_changed(self, treeselection):
        '''
        Update remove button when selection is changed.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonRemove.set_sensitive(False)
