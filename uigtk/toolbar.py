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


class Toolbar(Gtk.Toolbar):
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.set_sensitive(False)

        toolbutton = uigtk.widgets.ToolButton("_Add")
        toolbutton.set_icon_name("gtk-add")
        toolbutton.set_tooltip_text("Add item to the database.")
        toolbutton.connect("clicked", self.on_add_clicked)
        self.add(toolbutton)
        self.toolbuttonRemove = uigtk.widgets.ToolButton("_Remove")
        self.toolbuttonRemove.set_icon_name("gtk-remove")
        self.toolbuttonRemove.set_tooltip_text("Remove item from the database.")
        self.toolbuttonRemove.connect("clicked", self.on_remove_clicked)
        self.add(self.toolbuttonRemove)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)

        toolbutton = uigtk.widgets.ToolButton("_Save")
        toolbutton.set_icon_name("gtk-save")
        toolbutton.set_tooltip_text("Save changes to database.")
        toolbutton.connect("clicked", self.on_save_clicked)
        self.add(toolbutton)
        toolbutton = uigtk.widgets.ToolButton("_Save As")
        toolbutton.set_icon_name("gtk-save-as")
        toolbutton.set_tooltip_text("Save changes into new database file.")
        toolbutton.connect("clicked", self.on_save_as_clicked)
        self.add(toolbutton)

    def on_add_clicked(self, *args):
        '''
        Call add item function of current page type.
        '''
        page = data.window.notebook.get_page_type()
        page.add_item()

    def on_remove_clicked(self, *args):
        '''
        Call remove item function of current page type.
        '''
        page = data.window.notebook.get_page_type()
        page.remove_item()

    def on_save_clicked(self, *args):
        '''
        Call save functions for each data set.
        '''
        data.database.save_database()

    def on_save_as_clicked(self, *args):
        '''
        Display dialog to select location of new save file.
        '''
        dialog = uigtk.filedialog.SaveAsDialog()
        filename = dialog.show()

        if filename:
            data.window.set_title("Editor - %s" % (filename))

            data.database = structures.database.Database(filename)
            data.database.save_database()
