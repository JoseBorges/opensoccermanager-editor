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

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_spacing(5)
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

        self.buttonSave = uigtk.widgets.Button("_Save")
        self.buttonSave.set_tooltip_text("Save updated values into working data.")
        self.add(self.buttonSave)
