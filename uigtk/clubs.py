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
import structures.clubs
import uigtk.dialogs
import uigtk.interface
import uigtk.search
import uigtk.widgets


class Clubs(uigtk.widgets.Grid):
    name = "Clubs"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible,
                                                     data.clubs.get_clubs())
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.clubedit = ClubEdit()
        self.clubedit.set_sensitive(False)
        self.attach(self.clubedit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        club = data.clubs.add_club()

        treeiter = self.search.liststore.insert(0, [club.clubid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.clubedit.clear_details()
        self.clubedit.club = club

        self.clubedit.entryName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected club if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            clubid = model[treeiter][0]

            if data.preferences.confirm_remove:
                club = data.clubs.get_club_by_id(clubid)

                if not club.can_remove():
                    uigtk.dialogs.ClubKeyError(club.name)
                else:
                    dialog = uigtk.dialogs.RemoveItem("Club", club.name)

                    if dialog.show():
                        data.clubs.remove_club(clubid)
                        self.populate_data()
            else:
                data.clubs.remove_club(clubid)
                self.populate_data()

    def filter_visible(self, model, treeiter, data):
        '''
        Filter listing for matching criteria when searching.
        '''
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
        Get club selected and initiate details loading.
        '''
        model = treeview.get_model()

        if treepath:
            clubid = model[treepath][0]

            club = data.clubs.get_club_by_id(clubid)

            self.clubedit.set_details(club)
            self.clubedit.set_sensitive(True)

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
            self.clubedit.clear_details()
            self.clubedit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for clubid, club in data.clubs.get_clubs():
            self.search.liststore.append([clubid, club.name])

        self.search.activate_first_item()


class ClubEdit(uigtk.widgets.Grid):
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

        label = uigtk.widgets.Label("_Nickname", leftalign=True)
        grid2.attach(label, 0, 1, 1, 1)
        self.entryNickname = Gtk.Entry()
        label.set_mnemonic_widget(self.entryNickname)
        grid2.attach(self.entryNickname, 1, 1, 1, 1)

        self.attributes = AttributeEdit()
        grid.attach(self.attributes, 0, 2, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonUpdate.connect("clicked", self.on_update_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

    def on_update_clicked(self, *args):
        '''
        Update current values into working data.
        '''
        self.club.name = self.entryName.get_text()
        self.club.nickname = self.entryNickname.get_text()

        self.club.attributes = {}

        for row in self.attributes.liststore:
            attributeid = row[0]
            attribute = structures.clubs.Attribute(self.club.clubid)
            self.club.attributes[attributeid] = attribute

            attribute.year = row[1]
            attribute.manager = row[2]
            attribute.chairman = row[3]
            attribute.stadium = row[4]
            attribute.reputation = row[6]

        model, treeiter = Clubs.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = self.club.name

        model, treeiter = Clubs.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Clubs.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def set_details(self, club):
        '''
        Update selected player with details to be displayed.
        '''
        self.clear_details()

        self.club = club

        self.entryName.set_text(club.name)
        self.entryNickname.set_text(club.nickname)

        self.attributes.club = club
        self.attributes.populate_data()

    def clear_details(self, *args):
        '''
        Clear visible attributes.
        '''
        self.entryName.set_text("")
        self.entryNickname.set_text("")

        self.attributes.liststore.clear()


class AttributeEdit(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, str, str, int, str, int, int)
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
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Manager", column=2)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Chairman", column=3)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Stadium", column=5)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Reputation", column=6)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Players", column=7)
        self.attributes.treeview.append_column(treeviewcolumn)

        self.attributedialog = AttributeDialog()

    def on_add_clicked(self, *args):
        '''
        Display add dialog for new attribute.
        '''
        self.attributedialog.show(self.club, self.liststore)

    def on_edit_clicked(self, *args):
        '''
        Display edit dialog for selected attribute.
        '''
        model, treeiter = self.attributes.treeselection.get_selected()
        treeiter1 = model.convert_iter_to_child_iter(treeiter)

        self.attributedialog.show(self.club, self.liststore, treeiter1)

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded club.
        '''
        dialog = uigtk.dialogs.RemoveAttribute(index=1)

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            treeiter1 = model.convert_iter_to_child_iter(treeiter)

            self.liststore.remove(treeiter1)

            data.unsaved = True

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

        for attributeid, attribute in self.club.attributes.items():
            stadium = attribute.get_stadium_name()

            self.liststore.append([attributeid,
                                   attribute.year,
                                   attribute.manager,
                                   attribute.chairman,
                                   attribute.stadium.stadiumid,
                                   stadium,
                                   attribute.reputation,
                                   attribute.get_player_count()])


class AttributeDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_default_size(-1, 300)
        self.set_modal(True)
        self.set_title("Add Attribute")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Add", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.vbox.set_border_width(5)

        notebook = Gtk.Notebook()
        self.vbox.add(notebook)

        grid = uigtk.widgets.Grid()
        grid.set_border_width(5)
        notebook.append_page(grid, uigtk.widgets.Label("_Details"))

        label = uigtk.widgets.Label("_Year", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBoxText()
        self.comboboxYear.set_tooltip_text("Year to add attribute data.")
        self.comboboxYear.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Manager", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.entryManager = Gtk.Entry()
        self.entryManager.set_tooltip_text("Name of manager for this club.")
        self.entryManager.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.entryManager)
        grid.attach(self.entryManager, 1, 1, 2, 1)

        label = uigtk.widgets.Label("_Chairman", leftalign=True)
        grid.attach(label, 0, 2, 1, 1)
        self.entryChairman = Gtk.Entry()
        self.entryChairman.set_tooltip_text("Name of chairman for this club.")
        self.entryChairman.connect("changed", self.update_commit_button)
        label.set_mnemonic_widget(self.entryChairman)
        grid.attach(self.entryChairman, 1, 2, 2, 1)

        label = uigtk.widgets.Label("_Stadium", leftalign=True)
        grid.attach(label, 0, 3, 1, 1)
        self.buttonStadium = Gtk.Button("")
        self.buttonStadium.set_tooltip_text("Stadium selection for this club.")
        self.buttonStadium.connect("clicked", self.on_stadium_clicked)
        label.set_mnemonic_widget(self.buttonStadium)
        grid.attach(self.buttonStadium, 1, 3, 2, 1)

        label = uigtk.widgets.Label("_Reputation", leftalign=True)
        grid.attach(label, 0, 4, 1, 1)
        self.spinbuttonReputation = Gtk.SpinButton()
        self.spinbuttonReputation.set_range(1, 20)
        self.spinbuttonReputation.set_increments(1, 2)
        self.spinbuttonReputation.set_tooltip_text("Reputation value of club (higher is better).")
        self.spinbuttonReputation.connect("value-changed", self.update_commit_button)
        label.set_mnemonic_widget(self.spinbuttonReputation)
        grid.attach(self.spinbuttonReputation, 1, 4, 1, 1)

        self.playerlist = uigtk.interface.ItemList()
        self.playerlist.set_border_width(5)
        self.playerlist.buttonAdd.connect("clicked", self.on_add_player_clicked)
        self.playerlist.buttonRemove.connect("clicked", self.on_remove_player_clicked)
        notebook.append_page(self.playerlist, uigtk.widgets.Label("_Squad"))

        self.stadiumdialog = uigtk.selectors.StadiumSelectorDialog()
        self.playerdialog = uigtk.selectors.PlayerSelectorDialog()

    def update_commit_button(self, *args):
        '''
        Update sensitivity of commit button on dialog.
        '''
        sensitive = False

        if self.comboboxYear.get_active_id():
            sensitive = True

        if sensitive:
            sensitive = self.entryManager.get_text_length() > 0

        if sensitive:
            sensitive = self.entryChairman.get_text_length() > 0

        if sensitive:
            if self.stadiumid:
                sensitive = True
            else:
                sensitive = False

        self.set_response_sensitive(Gtk.ResponseType.OK, sensitive)

    def on_add_player_clicked(self, *args):
        '''
        Add selected player to squad.
        '''
        playerid = self.playerdialog.show()

        if playerid:
            player = data.players.get_player_by_id(playerid)

            for attributeid, attribute in player.attributes.items():
                if int(self.comboboxYear.get_active_id()) == attribute.year:
                    attribute.club = self.clubid
                    break

            self.populate_squad()

    def on_remove_player_clicked(self, *args):
        '''
        Remove selected player from club and remove club attribute.
        '''
        model, treeiter = self.playerlist.treeview.treeselection.get_selected()

        playerid = model[treeiter][0]
        attributeid = model[treeiter][1]

        player = data.players.get_player_by_id(playerid)
        attribute = player.attributes[attributeid]
        attribute.club = None

        self.populate_squad()

    def on_stadium_clicked(self, *args):
        '''
        Display stadium selection dialog.
        '''
        if self.attributeid:
            attribute = self.club.attributes[self.attributeid]
            self.stadiumid = self.stadiumdialog.show(stadiumid=attribute.stadium)
        else:
            self.stadiumid = self.stadiumdialog.show()

        if self.stadiumid:
            self.stadium = data.stadiums.get_stadium_by_id(self.stadiumid)
            self.buttonStadium.set_label(self.stadium.name)
            self.update_commit_button()

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
        Load attributes for given club.
        '''
        self.attribute = self.club.attributes[self.attributeid]

        self.comboboxYear.set_active_id(str(self.model[self.treeiter][1]))
        self.entryManager.set_text(self.model[self.treeiter][2])
        self.entryChairman.set_text(self.model[self.treeiter][3])

        self.stadiumid = self.model[self.treeiter][4]
        self.stadium = data.stadiums.get_stadium_by_id(self.stadiumid)

        self.buttonStadium.set_label(self.attribute.stadium.name)

        self.spinbuttonReputation.set_value(self.model[self.treeiter][6])

        self.populate_squad()

    def save_attributes(self):
        '''
        Save attributes for given club.
        '''
        if not self.treeiter:
            self.attributeid = self.club.add_attribute()
            self.treeiter = self.model.append([self.attributeid, 0, "", "", 0, "", 0, 0])

        self.model[self.treeiter][1] = int(self.comboboxYear.get_active_id())
        self.model[self.treeiter][2] = self.entryManager.get_text()
        self.model[self.treeiter][3] = self.entryChairman.get_text()
        self.model[self.treeiter][4] = self.stadiumid
        self.model[self.treeiter][5] = self.stadium.name
        self.model[self.treeiter][6] = self.spinbuttonReputation.get_value_as_int()

    def clear_attributes(self):
        '''
        Reset data entry fields on close of dialog.
        '''
        self.entryManager.set_text("")
        self.entryChairman.set_text("")
        self.buttonStadium.set_label("")
        self.spinbuttonReputation.set_value(1)

        self.stadiumid = None
        self.stadium = None

        self.playerlist.liststore.clear()

    def populate_squad(self):
        '''
        Load squad for club attribute being displayed.
        '''
        self.playerlist.liststore.clear()

        self.playerlist.labelCount.set_label("%i/30 Players" % (self.attribute.get_player_count()))

        for playerid, player in data.players.get_players():
            for attributeid, attribute in player.attributes.items():
                if attribute.club == self.club.clubid:
                    if attribute.year == self.attribute.year:
                        self.playerlist.liststore.append([playerid,
                                                          attributeid,
                                                          player.get_name()])

    def show(self, club, model, treeiter=None):
        self.club = club

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

            years = [attribute.year for attribute in club.attributes.values()]

            self.attributeid = None

            self.stadiumid = None
            self.stadium = None

            self.populate_years(years)

        self.update_commit_button()

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            self.save_attributes()

        self.clear_attributes()
        self.hide()
