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


class Search(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(200, -1)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str)
        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = Gtk.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeview.set_headers_visible(False)
        self.treeview.set_model(self.treemodelsort)
        self.treeview.set_activate_on_single_click(True)
        self.treeview.connect("button-press-event", self.on_button_event)
        scrolledwindow.add(self.treeview)

        self.treeselection = self.treeview.get_selection()

        self.treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        self.treeview.append_column(self.treeviewcolumn)

        self.entrySearch = Gtk.SearchEntry()
        self.attach(self.entrySearch, 0, 1, 1, 1)

        self.contextmenu = ContextMenu()

    def activate_first_item(self):
        '''
        Get first item in search and activate.
        '''
        treeiter = self.treemodelsort.get_iter_first()

        if treeiter:
            self.treeselection.select_iter(treeiter)

            treepath = self.treemodelsort.get_path(treeiter)
            self.treeview.row_activated(treepath, self.treeviewcolumn)

    def activate_row(self, treepath):
        '''
        Scroll to provided treepath and activate row.
        '''
        self.treeview.scroll_to_cell(treepath)
        self.treeview.set_cursor(treepath, None, False)
        self.treeview.row_activated(treepath, self.treeviewcolumn)

    def on_button_event(self, treeview, event):
        '''
        Handle right-click on search list items.
        '''
        if event.button == 3:
            self.contextmenu.show_all()
            self.contextmenu.popup(None, None, None, None, event.button, event.time)


class ContextMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemRemove = uigtk.widgets.MenuItem("_Remove Item")
        self.menuitemRemove.connect("activate", self.on_remove_item)
        self.append(self.menuitemRemove)

    def on_remove_item(self, *args):
        '''
        Call remove item function of current page type.
        '''
        page = data.window.notebook.get_page_type()
        page.remove_item()
