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
import uigtk.widgets


class SelectorDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_default_size(-1, 250)
        self.set_modal(True)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(int, str)
        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.set_model(self.treemodelsort)
        self.treeview.set_headers_visible(False)
        self.treeview.connect("row-activated", self.on_treeview_clicked)
        scrolledwindow.add(self.treeview)

        self.treeselection = self.treeview.get_selection()
        self.treeselection.connect("changed", self.on_treeselection_changed)

        self.treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        self.treeview.append_column(self.treeviewcolumn)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("changed", self.on_search_changed)
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("icon-press", self.on_search_cleared)
        self.vbox.add(self.entrySearch)

    def filter_visible(self, model, treeiter, data):
        visible = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False
                break

        return visible

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()
        treeview = treeselection.get_tree_view()

        if treeiter:
            treepath = model.get_path(treeiter)
            treeview.scroll_to_cell(treepath)

            self.set_response_sensitive(Gtk.ResponseType.OK, True)
        else:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

    def on_treeview_clicked(self, *args):
        '''
        Set response for double-click on treeview.
        '''
        self.response(Gtk.ResponseType.OK)

    def on_search_changed(self, entry):
        '''
        Auto-refilter treeview when last character deleted.
        '''
        if entry.get_text_length() == 0:
            self.treemodelfilter.refilter()

    def on_search_activated(self, *args):
        '''
        Refilter treeview when entry is activated.
        '''
        self.treemodelfilter.refilter()

    def on_search_cleared(self, entry, position, event):
        '''
        Refilter search display if search entry is cleared.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.treemodelfilter.refilter()

    def select_item(self, itemid):
        '''
        Pre-select already selected item in treeview.
        '''
        if itemid:
            for item in self.liststore:
                if item[0] == itemid:
                    treeiter1 = self.treemodelfilter.convert_child_iter_to_iter(item.iter)
                    treeiter2 = self.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
                    treepath = self.treemodelsort.get_path(treeiter2[1])

                    self.treeview.scroll_to_cell(treepath)
                    self.treeview.set_cursor(treepath, None, False)
                    self.treeselection.select_path(treepath)

    def display(self):
        self.show_all()
        self.set_focus(self.entrySearch)


class PlayerSelectorDialog(SelectorDialog):
    def __init__(self):
        SelectorDialog.__init__(self)
        self.set_title("Select Player")

        self.treemodelfilter.set_visible_func(self.filter_visible, data.players)

    def populate_data(self):
        self.liststore.clear()

        for playerid, player in data.players.get_players():
            self.liststore.append([playerid, player.get_name()])

    def show(self, playerid=None):
        self.populate_data()
        self.select_item(playerid)

        self.display()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            self.playerid = model[treeiter][0]

        self.hide()

        return self.playerid


class ClubSelectorDialog(SelectorDialog):
    def __init__(self):
        SelectorDialog.__init__(self)
        self.set_title("Select Club")

        self.treemodelfilter.set_visible_func(self.filter_visible, data.clubs)

    def populate_data(self):
        self.liststore.clear()

        for clubid, club in data.clubs.get_clubs():
            self.liststore.append([clubid, club.name])

    def show(self, clubid=None):
        self.clubid = clubid

        self.populate_data()
        self.select_item(clubid)

        self.display()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            self.clubid = model[treeiter][0]

        self.hide()

        return self.clubid


class NationSelectorDialog(SelectorDialog):
    def __init__(self):
        self.nationid = None

        SelectorDialog.__init__(self)
        self.set_title("Select Nation")

        self.treemodelfilter.set_visible_func(self.filter_visible, data.nations)

    def populate_data(self):
        self.liststore.clear()

        for nationid, nation in data.nations.get_nations():
            self.liststore.append([nationid, nation.name])

    def get_nationality(self):
        return self.nationid

    def show(self, nationid=None):
        self.nationid = nationid

        self.populate_data()
        self.select_item(nationid)

        self.display()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            self.nationid = model[treeiter][0]

        self.hide()

        return self.nationid


class StadiumSelectorDialog(SelectorDialog):
    def __init__(self):
        SelectorDialog.__init__(self)
        self.set_title("Select Nation")

        self.treemodelfilter.set_visible_func(self.filter_visible, data.stadiums)

    def populate_data(self):
        self.liststore.clear()

        for stadiumid, stadium in data.stadiums.get_stadiums():
            self.liststore.append([stadiumid, stadium.name])

    def show(self, stadiumid=None):
        self.populate_data()
        self.select_item(stadiumid)

        self.display()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            stadiumid = model[treeiter][0]

        self.hide()

        return stadiumid


class Button(Gtk.Button):
    def __init__(self):
        self.selected = None

        Gtk.Button.__init__(self)
        self.set_use_underline(True)

    def get_selected_item(self):
        return self.selected

    def set_selected_item(self, label):
        self.set_label(label)
