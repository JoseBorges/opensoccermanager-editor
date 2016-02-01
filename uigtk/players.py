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
import structures.positions
import structures.skills
import uigtk.dateofbirth
import uigtk.dialogs
import uigtk.interface
import uigtk.search
import uigtk.selectors
import uigtk.widgets


class Players(uigtk.widgets.Grid):
    name = "Players"

    search = uigtk.search.Search()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.search.treemodelfilter.set_visible_func(self.filter_visible, data.players.get_players())
        self.search.treeview.connect("row-activated", self.on_row_activated)
        self.search.treeselection.connect("changed", self.on_treeselection_changed)
        self.search.entrySearch.connect("activate", self.on_search_activated)
        self.search.entrySearch.connect("changed", self.on_search_changed)
        self.search.entrySearch.connect("icon-press", self.on_search_cleared)
        self.attach(self.search, 0, 0, 1, 1)

        self.playeredit = PlayerEdit()
        self.playeredit.set_sensitive(False)
        self.attach(self.playeredit, 1, 0, 1, 1)

        self.populate_data()

    def add_item(self):
        '''
        Add item into model and load attributes for editing.
        '''
        playerid = data.players.add_player()

        treeiter = self.search.liststore.insert(0, [playerid, ""])
        treeiter1 = self.search.treemodelfilter.convert_child_iter_to_iter(treeiter)
        treeiter2 = self.search.treemodelsort.convert_child_iter_to_iter(treeiter1[1])
        treepath = self.search.treemodelsort.get_path(treeiter2[1])

        self.search.activate_row(treepath)

        self.playeredit.clear_details()
        self.playeredit.playerid = playerid

        self.playeredit.entryFirstName.grab_focus()

    def remove_item(self):
        '''
        Query removal of selected player if dialog enabled.
        '''
        model, treeiter = self.search.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]

            if data.preferences.confirm_remove:
                player = data.players.get_player_by_id(playerid)

                dialog = uigtk.dialogs.RemoveItem("Player", player.get_name(mode=1))

                if dialog.show():
                    self.delete_player(playerid)
                    self.populate_data()
            else:
                self.delete_player(playerid)
                self.populate_data()

    def delete_player(self, playerid):
        '''
        Remove player from working data and repopulate list.
        '''
        data.players.remove_player(playerid)

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
            playerid = model[treeiter][0]

            self.playeredit.set_details(playerid)
            self.playeredit.set_sensitive(True)

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
            self.playeredit.clear_details()
            self.playeredit.set_sensitive(False)

    def populate_data(self):
        self.search.liststore.clear()

        for playerid, player in data.players.get_players():
            self.search.liststore.append([playerid, player.get_name()])

        self.search.activate_first_item()


class PlayerEdit(Players, uigtk.widgets.Grid):
    playerid = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.attach(grid, 0, 0, 1, 1)

        frame = uigtk.widgets.CommonFrame("Personal")
        grid.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_First Name", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.entryFirstName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryFirstName)
        frame.grid.attach(self.entryFirstName, 1, 0, 1, 1)
        label = uigtk.widgets.Label("_Second Name", leftalign=True)
        frame.grid.attach(label, 0, 1, 1 ,1)
        self.entrySecondName = Gtk.Entry()
        label.set_mnemonic_widget(self.entrySecondName)
        frame.grid.attach(self.entrySecondName, 1, 1, 1, 1)
        label = uigtk.widgets.Label("_Common Frame", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.entryCommonName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryCommonName)
        frame.grid.attach(self.entryCommonName, 1, 2, 1, 1)

        label = uigtk.widgets.Label("_Date Of Birth", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        self.buttonDateOfBirth = Gtk.Button("")
        self.buttonDateOfBirth.connect("clicked", self.on_date_of_birth_clicked)
        label.set_mnemonic_widget(self.buttonDateOfBirth)
        frame.grid.attach(self.buttonDateOfBirth, 1, 3, 1, 1)

        label = uigtk.widgets.Label("_Nationality", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        self.buttonNationality = Gtk.Button("")
        self.buttonNationality.connect("clicked", self.on_nationality_clicked)
        label.set_mnemonic_widget(self.buttonNationality)
        frame.grid.attach(self.buttonNationality, 1, 4, 1, 1)

        self.attributes = AttributeEdit()
        grid.attach(self.attributes, 0, 1, 1, 1)

        self.actionbuttons = uigtk.interface.ActionButtons()
        self.actionbuttons.buttonUpdate.connect("clicked", self.on_save_clicked)
        self.attach(self.actionbuttons, 0, 1, 1, 1)

        self.dialogDateOfBirth = uigtk.dateofbirth.DateOfBirth()
        self.dialogNationality = uigtk.selectors.NationSelectorDialog()

    def on_save_clicked(self, *args):
        '''
        Save current values into working data.
        '''
        player = data.players.get_player_by_id(self.playerid)

        player.first_name = self.entryFirstName.get_text()
        player.second_name = self.entrySecondName.get_text()
        player.common_name = self.entryCommonName.get_text()

        player.date_of_birth = self.dialogDateOfBirth.get_date_of_birth()
        player.nationality = self.dialogNationality.get_nationality()

        model, treeiter = Players.search.treeselection.get_selected()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore = model.get_model()
        liststore[child_treeiter][1] = player.get_name()

        model, treeiter = Players.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        Players.search.treeview.scroll_to_cell(treepath)

        data.unsaved = True

    def on_date_of_birth_clicked(self, *args):
        '''
        Display date of birth selection dialog.
        '''
        if self.dialogDateOfBirth:
            date_of_birth = self.dialogDateOfBirth.date_of_birth
        else:
            date_of_birth = self.player.date_of_birth

        if self.dialogDateOfBirth.show(date_of_birth):
            self.update_date_of_birth_button()

    def on_nationality_clicked(self, *args):
        '''
        Display nationality selection dialog.
        '''
        if self.dialogNationality.show(self.player.nationality):
            self.update_nationality_button()

    def set_details(self, playerid):
        '''
        Update selected player with details to be displayed.
        '''
        self.clear_details()

        PlayerEdit.playerid = playerid
        self.player = data.players.get_player_by_id(playerid)

        self.entryFirstName.set_text(self.player.first_name)
        self.entrySecondName.set_text(self.player.second_name)
        self.entryCommonName.set_text(self.player.common_name)

        self.dialogDateOfBirth.date_of_birth = self.player.date_of_birth
        self.update_date_of_birth_button()

        self.dialogNationality.nationid = self.player.nationality
        self.update_nationality_button()

        self.attributes.playerid = playerid
        self.attributes.populate_data()

    def clear_details(self):
        '''
        Clear visible attributes.
        '''
        self.entryFirstName.set_text("")
        self.entrySecondName.set_text("")
        self.entryCommonName.set_text("")

        self.dialogDateOfBirth.date_of_birth = None
        self.buttonDateOfBirth.set_label("")
        self.dialogNationality.nationid = None
        self.buttonNationality.set_label("")

        self.attributes.liststore.clear()

    def update_date_of_birth_button(self):
        '''
        Update selected date of birth label on button.
        '''
        if self.dialogDateOfBirth.date_of_birth:
            self.buttonDateOfBirth.set_label("%s-%s-%s" % (self.dialogDateOfBirth.date_of_birth))
        else:
            self.buttonDateOfBirth.set_label("")

    def update_nationality_button(self):
        '''
        Update selected nationality label on button.
        '''
        if self.dialogNationality.nationid:
            nationality = data.nations.get_nation_by_id(self.dialogNationality.nationid)
            self.buttonNationality.set_label(nationality.name)
        else:
            self.buttonNationality.set_label("")


class AttributeEdit(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.liststore = Gtk.ListStore(int, int, str, int, str, int, int, int,
                                       int, int, int, int, int, int, int)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.attributes = uigtk.interface.Attributes()
        self.attributes.treeview.set_model(self.treemodelsort)
        self.attributes.treeview.connect("row-activated", self.on_row_activated)
        self.attributes.treeselection.connect("changed", self.on_treeselection_changed)
        self.attributes.buttonAdd.connect("clicked", self.on_add_clicked)
        self.attributes.buttonEdit.connect("clicked", self.on_edit_clicked)
        self.attributes.buttonRemove.connect("clicked", self.on_remove_clicked)
        self.attach(self.attributes, 0, 0, 1, 1)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Year", column=1)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        treeviewcolumn.set_expand(True)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age", column=3)
        self.attributes.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=4)
        self.attributes.treeview.append_column(treeviewcolumn)

        skills = structures.skills.Skills()

        for count, item in enumerate(skills.get_short_skills(), start=5):
            label = Gtk.Label("%s" % (item))
            label.set_tooltip_text(skills.get_skills()[count - 5])
            label.show()
            treeviewcolumn = uigtk.widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_widget(label)
            self.attributes.treeview.append_column(treeviewcolumn)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Training", column=14)
        self.attributes.treeview.append_column(treeviewcolumn)

        self.attributedialog = AttributeDialog()

    def on_add_clicked(self, *args):
        '''
        Add new attribute for loaded player.
        '''
        self.attributedialog.show(PlayerEdit.playerid)

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Handle editing of attribute for selected item.
        '''
        model, treeiter = self.attributes.treeselection.get_selected()
        attributeid = model[treeiter][0]

        self.attributedialog.show(self.playerid, attributeid)

        self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Remove selected attribute for loaded player.
        '''
        dialog = uigtk.dialogs.RemoveAttribute()

        if dialog.show():
            model, treeiter = self.attributes.treeselection.get_selected()
            attributeid = model[treeiter][0]

            player = data.players.get_player_by_id(self.playerid)
            player.attributes.remove_attribute(attributeid)

            self.populate_data()

    def on_row_activated(self, *args):
        self.on_edit_clicked()

    def on_treeselection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            attributeid = model[treeiter][0]
            self.attributes.buttonEdit.set_sensitive(True)
            self.attributes.buttonRemove.set_sensitive(True)
        else:
            self.attributes.buttonEdit.set_sensitive(False)
            self.attributes.buttonRemove.set_sensitive(False)

    def populate_data(self):
        player = data.players.get_player_by_id(self.playerid)

        self.liststore.clear()

        for attributeid, attribute in player.attributes.items():
            club = data.clubs.get_club_by_id(attribute.club)

            self.liststore.append([attributeid,
                                   attribute.year,
                                   club.name,
                                   player.get_age(attribute.year),
                                   attribute.position,
                                   attribute.keeping,
                                   attribute.tackling,
                                   attribute.passing,
                                   attribute.shooting,
                                   attribute.heading,
                                   attribute.pace,
                                   attribute.stamina,
                                   attribute.ball_control,
                                   attribute.set_pieces,
                                   attribute.training])


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

        label = uigtk.widgets.Label("_Year", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBoxText()
        self.comboboxYear.set_tooltip_text("Year to add attribute data.")
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Club", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.buttonClub = Gtk.Button("")
        self.buttonClub.set_hexpand(True)
        self.buttonClub.connect("clicked", self.on_club_clicked)
        self.buttonClub.set_tooltip_text("Club player is contracted to.")
        label.set_mnemonic_widget(self.buttonClub)
        grid.attach(self.buttonClub, 1, 1, 2, 1)

        label = uigtk.widgets.Label("_Position", leftalign=True)
        grid.attach(label, 0, 2, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.set_tooltip_text("Position player will play in.")
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 2, 1, 1)

        positions = structures.positions.Positions()

        for position in positions.get_positions():
            self.comboboxPosition.append(position, position)

        self.comboboxPosition.set_active(0)

        skills = structures.skills.Skills()
        self.spinbuttonSkills = []

        for count, skill in enumerate(skills.get_skills(), start=3):
            label = uigtk.widgets.Label("_%s" % (skill), leftalign=True)
            grid.attach(label, 0, count, 1, 1)
            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 99)
            spinbutton.set_increments(1, 10)
            spinbutton.set_value(0)
            label.set_mnemonic_widget(spinbutton)
            grid.attach(spinbutton, 1, count, 1, 1)
            self.spinbuttonSkills.append(spinbutton)

        label = uigtk.widgets.Label("_Training", leftalign=True)
        grid.attach(label, 0, 13, 1, 1)
        self.spinbuttonTraining = Gtk.SpinButton()
        self.spinbuttonTraining.set_range(1, 10)
        self.spinbuttonTraining.set_increments(1, 2)
        self.spinbuttonTraining.set_tooltip_text("Player improvement value (higher causes player to improve faster).")
        label.set_mnemonic_widget(self.spinbuttonTraining)
        grid.attach(self.spinbuttonTraining, 1, 13, 1, 1)

        self.dialogClubSelect = uigtk.selectors.ClubSelectorDialog()

    def on_club_clicked(self, *args):
        '''
        Display club selection dialog.
        '''
        player = data.players.get_player_by_id(self.playerid)
        attribute = player.attributes[self.attributeid]

        self.clubid = self.dialogClubSelect.show(self.clubid)

        if self.clubid:
            club = data.clubs.get_club_by_id(self.clubid)
            self.buttonClub.set_label(club.name)

    def load_attributes(self):
        '''
        Load selected player and attribute data.
        '''
        player = data.players.get_player_by_id(self.playerid)
        attribute = player.attributes[self.attributeid]

        self.comboboxYear.set_active_id(str(attribute.year))

        self.clubid = attribute.club
        club = data.clubs.get_club_by_id(attribute.club)
        self.buttonClub.set_label("%s" % (club.name))

        self.comboboxPosition.set_active_id(attribute.position)

        for count, skill in enumerate(attribute.get_skills()):
            self.spinbuttonSkills[count].set_value(skill)

        self.spinbuttonTraining.set_value(attribute.training)

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

    def show(self, playerid, attributeid=None):
        self.playerid = playerid
        self.attributeid = attributeid

        button = self.get_widget_for_response(Gtk.ResponseType.OK)

        if attributeid:
            self.set_title("Edit Attribute")
            button.set_label("_Edit")

            self.populate_years()

            self.load_attributes()
        else:
            self.set_title("Add Attribute")
            button.set_label("_Add")

            player = data.players.get_player_by_id(self.playerid)
            years = [attribute.year for attribute in player.attributes.values()]

            self.populate_years(years)

            self.attributeid = player.add_attribute()

            self.clubid = None

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            player = data.players.get_player_by_id(self.playerid)
            attribute = player.attributes[self.attributeid]

            attribute.year = int(self.comboboxYear.get_active_id())
            attribute.club = self.clubid
            attribute.position = self.comboboxPosition.get_active_text()
            attribute.keeping = self.spinbuttonSkills[0].get_value_as_int()
            attribute.tackling = self.spinbuttonSkills[1].get_value_as_int()
            attribute.passing = self.spinbuttonSkills[2].get_value_as_int()
            attribute.shooting = self.spinbuttonSkills[3].get_value_as_int()
            attribute.heading = self.spinbuttonSkills[4].get_value_as_int()
            attribute.pace = self.spinbuttonSkills[5].get_value_as_int()
            attribute.stamina = self.spinbuttonSkills[6].get_value_as_int()
            attribute.ball_control = self.spinbuttonSkills[7].get_value_as_int()
            attribute.set_pieces = self.spinbuttonSkills[8].get_value_as_int()
            attribute.training = self.spinbuttonTraining.get_value_as_int()

        self.hide()
