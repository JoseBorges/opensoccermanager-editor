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


class YearManager(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_default_size(-1, 200)
        self.set_transient_for(data.window)
        self.set_title("Year Manager")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(int)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_headers_visible(False)
        self.treeview.set_model(self.liststore)
        scrolledwindow.add(self.treeview)

        self.treeselection = self.treeview.get_selection()
        self.treeselection.connect("changed", self.on_treeselection_changed)

        cellrenderertext = Gtk.CellRendererText()
        cellrenderertext.set_property("editable", True)
        cellrenderertext.connect("edited", self.on_cellrenderer_edited)

        self.treeviewcolumn = Gtk.TreeViewColumn(None, cellrenderertext, text=0)
        self.treeview.append_column(self.treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        self.vbox.add(buttonbox)

        buttonAdd = uigtk.widgets.Button("_Add")
        buttonAdd.connect("clicked", self.on_add_clicked)
        buttonbox.add(buttonAdd)
        self.buttonRemove = uigtk.widgets.Button("_Remove")
        self.buttonRemove.connect("clicked", self.on_remove_clicked)
        buttonbox.add(self.buttonRemove)

        self.populate_data()

        self.show_all()

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonRemove.set_sensitive(False)

    def on_add_clicked(self, *args):
        treeiter = self.liststore.append([None])
        treepath = self.liststore.get_path(treeiter)
        self.treeview.set_cursor(treepath,
                                 column=self.treeviewcolumn,
                                 start_editing=True)

    def on_remove_clicked(self, *args):
        model, treeiter = self.treeselection.get_selected()
        year = model[treeiter][0]

        # Check year can be removed
        data.years.remove_year(year)

        self.populate_data()

    def on_cellrenderer_edited(self, cellrenderertext, treepath, text):
        if int(text) not in data.years.get_years():
            data.years.add_year(int(text))

        self.populate_data()

    def on_response(self, *args):
        self.destroy()

    def populate_data(self):
        self.liststore.clear()

        for year in data.years.get_years():
            self.liststore.append([year])
