#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import unicodedata
import re

import data
import database
import dialogs
import display
import preferences
import widgets


class Player:
    pass


class Club:
    pass


class Nation:
    pass


class Stadium:
    pass


def about():
    path = os.path.join("resources", "logo.svg")
    icon = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 64, 64)

    aboutdialog = Gtk.AboutDialog()
    aboutdialog.set_transient_for(widgets.window)
    aboutdialog.set_program_name("Editor")
    aboutdialog.set_comments("Data editor for OpenSoccerManager")
    aboutdialog.set_website("http://opensoccermanager.org/")
    aboutdialog.set_website_label("Website")
    aboutdialog.set_license_type(Gtk.License.GPL_3_0)
    aboutdialog.set_logo(icon)

    aboutdialog.run()
    aboutdialog.destroy()


class Preferences(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_title("Preferences")
        self.set_border_width(5)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        self.checkbuttonQuit = Gtk.CheckButton("_Display confirmation dialog when quitting")
        self.checkbuttonQuit.set_use_underline(True)
        self.checkbuttonQuit.connect("toggled", self.quit_toggled)
        grid.attach(self.checkbuttonQuit, 0, 0, 1, 1)

    def response_handler(self, widget, event):
        self.hide()

    def quit_toggled(self, checkbutton):
        data.options.confirm_quit = checkbutton.get_active()
        data.options["INTERFACE"]["ConfirmQuit"] = str(data.options.confirm_quit)

        data.options.write_file()

    def run(self):
        self.checkbuttonQuit.set_active(data.options.confirm_quit)

        self.show_all()


class NewDatabase(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("New Database")
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.add_button("C_ancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Create", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_Season")
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonSeason = Gtk.SpinButton.new_with_range(1950, 2049, 1)
        label.set_mnemonic_widget(self.spinbuttonSeason)
        grid.attach(self.spinbuttonSeason, 1, 0, 1, 1)

        label = widgets.Label("_Location")
        grid.attach(label, 0, 1, 1, 1)
        self.filechooserLocation = Gtk.FileChooserButton()
        self.filechooserLocation.set_hexpand(True)
        self.filechooserLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        label.set_mnemonic_widget(self.filechooserLocation)
        grid.attach(self.filechooserLocation, 1, 1, 2, 1)

    def display(self):
        self.show_all()

        filepath = None

        if self.run() == Gtk.ResponseType.OK:
            season = self.spinbuttonSeason.get_value_as_int()
            year = str(season)[2:4]
            year1 = str(season + 1)[2:4]
            data.season = season
            filename = "osm%s%s.db" % (year, year1)

            if self.filechooserLocation.get_current_folder() is not None:
                folder = self.filechooserLocation.get_current_folder()
                filepath = os.path.join(folder, filename)
            else:
                if self.filechooserLocation.get_filename() is not None:
                    folder = self.filechooserLocation.get_filename()
                    filepath = os.path.join(folder, filename)
                else:
                    filepath = filename

        self.hide()

        return filepath


class AddPlayerDialog(Gtk.Dialog):
    state = False

    def __init__(self):
        def nation_changed(combobox):
            if self.comboboxNationality.get_active_id() is None:
                self.buttonSave.set_sensitive(False)
            else:
                self.buttonSave.set_sensitive(True)

        def free_agent_changed(checkbutton):
            if checkbutton.get_active():
                self.buttonClub.set_sensitive(False)
                self.buttonClub.set_label("")
            else:
                self.buttonClub.set_sensitive(True)

        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.connect("response", self.response_handler)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        self.buttonSave = widgets.Button()
        self.buttonSave.set_sensitive(False)
        self.buttonSave.connect("clicked", self.save_handler)
        action_area = self.get_action_area()
        action_area.add(self.buttonSave)

        self.checkbuttonMulti = Gtk.CheckButton("Add Multiple Items")
        action_area.add(self.checkbuttonMulti)

        self.liststoreClub = Gtk.ListStore(str, str)
        treemodelsortClub = Gtk.TreeModelSort(self.liststoreClub)
        treemodelsortClub.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.liststoreNationality = Gtk.ListStore(str, str)
        treemodelsortNationality = Gtk.TreeModelSort(self.liststoreNationality)
        treemodelsortNationality.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_First Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryFirstName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryFirstName)
        grid.attach(self.entryFirstName, 1, 0, 2, 1)
        label = widgets.Label("_Second Name")
        grid.attach(label, 0, 1, 1, 1)
        self.entrySecondName = Gtk.Entry()
        label.set_mnemonic_widget(self.entrySecondName)
        grid.attach(self.entrySecondName, 1, 1, 2, 1)
        label = widgets.Label("_Common Name")
        grid.attach(label, 0, 2, 1, 1)
        self.entryCommonName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryCommonName)
        grid.attach(self.entryCommonName, 1, 2, 2, 1)

        label = widgets.Label("_Date Of Birth")
        grid.attach(label, 0, 3, 1, 1)
        self.buttonDateOfBirth = widgets.Button()
        self.buttonDateOfBirth.connect("clicked", self.date_of_birth)
        label.set_mnemonic_widget(self.buttonDateOfBirth)
        grid.attach(self.buttonDateOfBirth, 1, 3, 1, 1)
        self.labelAge = widgets.Label()
        self.labelAge.set_tooltip_text("Age at start of game")
        grid.attach(self.labelAge, 2, 3, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_column_spacing(5)
        grid.attach(grid1, 1, 4, 2, 1)

        label = widgets.Label("_Club")
        grid.attach(label, 0, 4, 1, 1)
        self.checkbuttonFreeAgent = Gtk.CheckButton("_Free Agent")
        self.checkbuttonFreeAgent.set_use_underline(True)
        self.checkbuttonFreeAgent.connect("toggled", free_agent_changed)
        grid1.attach(self.checkbuttonFreeAgent, 1, 4, 1, 1)
        self.buttonClub = widgets.Button()
        self.buttonClub.set_hexpand(True)
        label.set_mnemonic_widget(self.buttonClub)
        self.buttonClub.connect("clicked", self.club_change)
        grid1.attach(self.buttonClub, 2, 4, 1, 1)

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.Label("_Nationality")
        grid.attach(label, 0, 5, 1, 1)
        self.comboboxNationality = Gtk.ComboBox()
        self.comboboxNationality.set_model(treemodelsortNationality)
        self.comboboxNationality.set_id_column(0)
        self.comboboxNationality.pack_start(cellrenderertext, True)
        self.comboboxNationality.add_attribute(cellrenderertext, "text", 1)
        self.comboboxNationality.connect("changed", nation_changed)
        label.set_mnemonic_widget(self.comboboxNationality)
        grid.attach(self.comboboxNationality, 1, 5, 1, 1)

        label = widgets.Label("_Position")
        grid.attach(label, 0, 6, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 6, 1, 1)

        for position in data.positions:
            self.comboboxPosition.append(position, position)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 7, 6, 1)

        label = widgets.Label("_Keeping")
        grid1.attach(label, 0, 0, 1, 1)
        self.spinbuttonKP = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonKP)
        grid1.attach(self.spinbuttonKP, 1, 0, 1, 1)

        label = widgets.Label("_Tackling")
        grid1.attach(label, 0, 1, 1, 1)
        self.spinbuttonTK = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonTK)
        grid1.attach(self.spinbuttonTK, 1, 1, 1, 1)

        label = widgets.Label("_Passing")
        grid1.attach(label, 0, 2, 1, 1)
        self.spinbuttonPS = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonPS)
        grid1.attach(self.spinbuttonPS, 1, 2, 1, 1)

        label = widgets.Label("_Shooting")
        grid1.attach(label, 2, 0, 1, 1)
        self.spinbuttonSH = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonSH)
        grid1.attach(self.spinbuttonSH, 3, 0, 1, 1)

        label = widgets.Label("_Heading")
        grid1.attach(label, 2, 1, 1, 1)
        self.spinbuttonHD = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonHD)
        grid1.attach(self.spinbuttonHD, 3, 1, 1, 1)

        label = widgets.Label("_Pace")
        grid1.attach(label, 2, 2, 1, 1)
        self.spinbuttonPC = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonPC)
        grid1.attach(self.spinbuttonPC, 3, 2, 1, 1)

        label = widgets.Label("_Stamina")
        grid1.attach(label, 4, 0, 1, 1)
        self.spinbuttonST = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonST)
        grid1.attach(self.spinbuttonST, 5, 0, 1, 1)

        label = widgets.Label("_Ball Control")
        grid1.attach(label, 4, 1, 1, 1)
        self.spinbuttonBC = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonBC)
        grid1.attach(self.spinbuttonBC, 5, 1, 1, 1)

        label = widgets.Label("_Set Pieces")
        grid1.attach(label, 4, 2, 1, 1)
        self.spinbuttonSP = Gtk.SpinButton.new_with_range(1, 99, 1)
        label.set_mnemonic_widget(self.spinbuttonSP)
        grid1.attach(self.spinbuttonSP, 5, 2, 1, 1)

        label = widgets.Label("Training _Value")
        grid.attach(label, 0, 8, 1, 1)
        self.spinbuttonTraining = Gtk.SpinButton.new_with_range(1, 10, 1)
        label.set_mnemonic_widget(self.spinbuttonTraining)
        grid.attach(self.spinbuttonTraining, 1, 8, 1, 1)

        self.clubselectiondialog = ClubSelectionDialog()
        self.dob = DateOfBirth(parent=self)

    def club_change(self, button):
        if self.current is not None:
            clubid = data.players[self.current].club

            if self.selected_club != clubid:
                clubid = self.selected_club
        else:
            clubid = None

        clubid = self.clubselectiondialog.display(parent=self, clubid=clubid)

        if clubid is not None:
            self.selected_club = clubid
            self.buttonClub.set_label("%s" % (data.clubs[clubid].name))
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

    def date_of_birth(self, button):
        self.date = self.dob.display(date=self.date)

        if self.date is not None:
            year, month, day = self.date
            date = "%i-%s-%s" % (year, month, day)
            self.buttonDateOfBirth.set_label("%s" % (date))

            year, month, day = list(map(int, self.date))

            age = data.season - year

            if (month, day) > (8, 1):
                age -= 1

            self.labelAge.set_label("Age: %i" % (age))

    def response_handler(self, dialog, response):
        self.clear_fields()

        self.hide()

    def save_handler(self, button):
        self.save_data(self.current)
        self.clear_fields()

        self.state = True

        if self.current:
            try:
                self.current = self.generator.__next__()
                self.load_fields(self.current)
            except StopIteration:
                self.hide()

        if self.checkbuttonMulti.get_visible():
            if not self.checkbuttonMulti.get_active():
                self.hide()

    def save_data(self, playerid):
        if playerid is None:
            data.idnumbers.playerid += 1

            player = Player()
            data.players[data.idnumbers.playerid] = player
        else:
            player = data.players[playerid]

        player.first_name = self.entryFirstName.get_text()
        player.second_name = self.entrySecondName.get_text()
        player.common_name = self.entryCommonName.get_text()

        if self.checkbuttonFreeAgent.get_active():
            player.club = 0
        else:
            player.club = self.selected_club

        player.nationality = int(self.comboboxNationality.get_active_id())

        year, month, day = self.date
        player.date_of_birth = ("%i-%s-%s" % (year, month, day))

        player.position = self.comboboxPosition.get_active_id()
        player.keeping = self.spinbuttonKP.get_value_as_int()
        player.tackling = self.spinbuttonTK.get_value_as_int()
        player.passing = self.spinbuttonPS.get_value_as_int()
        player.shooting = self.spinbuttonSH.get_value_as_int()
        player.heading = self.spinbuttonHD.get_value_as_int()
        player.pace = self.spinbuttonPC.get_value_as_int()
        player.stamina = self.spinbuttonST.get_value_as_int()
        player.ball_control = self.spinbuttonBC.get_value_as_int()
        player.set_pieces = self.spinbuttonSP.get_value_as_int()
        player.training_value = self.spinbuttonTraining.get_value_as_int()

    def display(self, playerid=None):
        self.state = False

        self.liststoreClub.clear()
        self.liststoreNationality.clear()

        for clubid, club in data.clubs.items():
            self.liststoreClub.append([str(clubid), club.name])

        for nationid, nation in data.nations.items():
            self.liststoreNationality.append([str(nationid), nation.name])

        self.show_all()

        if playerid is None:
            self.set_title("Add Player")
            self.buttonSave.set_label("_Add")

            self.current = None
        else:
            self.set_title("Edit Player")
            self.buttonSave.set_label("_Edit")
            self.checkbuttonMulti.set_visible(False)

            self.generator = playerid.__iter__()
            self.current = self.generator.__next__()

            self.load_fields(playerid=self.current)

        self.run()

    def load_fields(self, playerid):
        player = data.players[playerid]

        self.entryFirstName.set_text(player.first_name)
        self.entrySecondName.set_text(player.second_name)
        self.entryCommonName.set_text(player.common_name)
        self.buttonDateOfBirth.set_label("%s" % (player.date_of_birth))

        if player.club != 0 and player.club is not None:
            self.selected_club = player.club
            self.buttonClub.set_label("%s" % (data.clubs[player.club].name))
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

        self.comboboxNationality.set_active_id(str(player.nationality))

        date = player.date_of_birth.split("-")
        self.date = list(map(int, date))

        age = data.season - self.date[0]

        if (self.date[1], self.date[2]) > (8, 1):
            age -= 1

        self.labelAge.set_label("Age: %i" % (age))

        self.comboboxPosition.set_active_id(player.position)
        self.spinbuttonKP.set_value(player.keeping)
        self.spinbuttonTK.set_value(player.tackling)
        self.spinbuttonPS.set_value(player.passing)
        self.spinbuttonSH.set_value(player.shooting)
        self.spinbuttonHD.set_value(player.heading)
        self.spinbuttonPC.set_value(player.pace)
        self.spinbuttonST.set_value(player.stamina)
        self.spinbuttonBC.set_value(player.ball_control)
        self.spinbuttonSP.set_value(player.set_pieces)
        self.spinbuttonTraining.set_value(player.training_value)

    def clear_fields(self):
        self.entryFirstName.set_text("")
        self.entrySecondName.set_text("")
        self.entryCommonName.set_text("")
        self.buttonDateOfBirth.set_label("")
        self.labelAge.set_label("")
        self.buttonClub.set_label("")
        self.comboboxNationality.set_active(-1)

        self.comboboxPosition.set_active(-1)
        self.spinbuttonKP.set_value(1)
        self.spinbuttonTK.set_value(1)
        self.spinbuttonPS.set_value(1)
        self.spinbuttonSH.set_value(1)
        self.spinbuttonHD.set_value(1)
        self.spinbuttonPC.set_value(1)
        self.spinbuttonST.set_value(1)
        self.spinbuttonBC.set_value(1)
        self.spinbuttonSP.set_value(1)
        self.spinbuttonTraining.set_value(1)


class AddClubDialog(Gtk.Dialog):
    state = False

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.set_resizable(False)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.connect("response", self.response_handler)

        self.buttonSave = widgets.Button()
        self.buttonSave.set_sensitive(False)
        self.buttonSave.connect("clicked", self.save_handler)
        action_area = self.get_action_area()
        action_area.add(self.buttonSave)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 0, 1, 1)

        label = widgets.Label("_Name")
        grid1.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid1.attach(self.entryName, 1, 0, 2, 1)

        label = widgets.Label("_Nickname")
        grid1.attach(label, 0, 1, 1, 1)
        self.entryNickname = Gtk.Entry()
        label.set_mnemonic_widget(self.entryNickname)
        grid1.attach(self.entryNickname, 1, 1, 2, 1)

        label = widgets.Label("_Manager")
        grid1.attach(label, 0, 2, 1, 1)
        self.entryManager = Gtk.Entry()
        label.set_mnemonic_widget(self.entryManager)
        grid1.attach(self.entryManager, 1, 2, 2, 1)

        label = widgets.Label("_Chairman")
        grid1.attach(label, 0, 3, 1, 1)
        self.entryChairman = Gtk.Entry()
        label.set_mnemonic_widget(self.entryChairman)
        grid1.attach(self.entryChairman, 1, 3, 2, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststoreStadiums = Gtk.ListStore(str, str)

        label = widgets.Label("_Stadium")
        grid1.attach(label, 0, 4, 1, 1)
        self.comboboxStadium = Gtk.ComboBox()
        self.comboboxStadium.set_model(self.liststoreStadiums)
        self.comboboxStadium.set_id_column(0)
        self.comboboxStadium.pack_start(cellrenderertext, True)
        self.comboboxStadium.add_attribute(cellrenderertext, "text", 1)
        label.set_mnemonic_widget(self.comboboxStadium)
        grid1.attach(self.comboboxStadium, 1, 4, 2, 1)

        label = widgets.Label("_Reputation")
        grid1.attach(label, 0, 5, 1, 1)
        self.spinbuttonReputation = Gtk.SpinButton.new_with_range(1, 20, 1)
        label.set_mnemonic_widget(self.spinbuttonReputation)
        grid1.attach(self.spinbuttonReputation, 1, 5, 1, 1)

        self.gridSquad = Gtk.Grid()
        self.gridSquad.set_row_spacing(5)
        self.gridSquad.set_column_spacing(5)
        grid.attach(self.gridSquad, 1, 0, 1, 1)

        frame = widgets.CommonFrame("Squad")
        self.gridSquad.attach(frame, 0, 0, 1, 4)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        frame.insert(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststorePlayers = Gtk.ListStore(int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststorePlayers)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_visible(False)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        grid.attach(buttonbox, 1, 0, 1, 1)

        buttonAdd = Gtk.Button.new_from_icon_name("gtk-add", Gtk.IconSize.BUTTON)
        buttonAdd.connect("clicked", self.add_player)
        buttonbox.add(buttonAdd)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove", Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.remove_player)
        buttonbox.add(self.buttonRemove)
        buttonClear = Gtk.Button.new_from_icon_name("gtk-clear", Gtk.IconSize.BUTTON)
        buttonClear.connect("clicked", self.clear_player)
        buttonbox.add(buttonClear)

        self.playerselectiondialog = PlayerSelectionDialog()

    def display(self, clubid=None):
        self.show_all()

        self.liststoreStadiums.clear()

        for stadiumid, stadium in data.stadiums.items():
            self.liststoreStadiums.append([str(stadiumid), stadium.name])

        if clubid is None:
            self.set_title("Add Club")
            self.buttonSave.set_label("_Add")
            self.gridSquad.hide()

            self.current = None
        else:
            self.set_title("Edit Club")
            self.buttonSave.set_label("_Edit")
            self.buttonSave.set_sensitive(True)

            self.populate(clubid)

            self.load_fields(clubid)

            self.current = clubid

        self.run()

    def save_handler(self, button):
        self.save_data(clubid=self.current)
        self.clear_fields()

        self.state = True

        self.hide()

    def save_data(self, clubid):
        if clubid is None:
            data.idnumbers.clubid += 1

            club = Club()
            data.clubs[data.idnumbers.clubid] = club
        else:
            club = data.clubs[clubid]

        club.name = self.entryName.get_text()
        club.nickname = self.entryNickname.get_text()
        club.manager = self.entryManager.get_text()
        club.chairman = self.entryChairman.get_text()
        club.stadium = int(self.comboboxStadium.get_active_id())
        club.reputation = self.spinbuttonReputation.get_value_as_int()

    def response_handler(self, dialog, response):
        self.clear_fields()

        self.hide()

    def load_fields(self, clubid):
        club = data.clubs[clubid]

        self.entryName.set_text(club.name)
        self.entryNickname.set_text(club.nickname)
        self.entryManager.set_text(club.manager)
        self.entryChairman.set_text(club.chairman)
        self.comboboxStadium.set_active_id(str(club.stadium))
        self.spinbuttonReputation.set_value(club.reputation)

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryNickname.set_text("")
        self.entryManager.set_text("")
        self.entryChairman.set_text("")
        self.comboboxStadium.set_active(-1)
        self.spinbuttonReputation.set_value(1)

    def add_player(self, button):
        playerid = self.playerselectiondialog.display(parent=self)

        if playerid is not None:
            data.players[playerid].club = self.current
            self.populate(self.current)

    def remove_player(self, button):
        if remove_dialog(index=0, parent=self):
            model, treeiter = self.treeselection.get_selected()
            playerid = model[treeiter][0]

            data.players[playerid].club = 0

        self.populate(clubid=self.current)

    def clear_player(self, button):
        for item in self.liststorePlayers:
            playerid = item[0]
            data.players[playerid].club = 0

        self.populate(clubid=self.current)

    def populate(self, clubid):
        self.liststorePlayers.clear()

        for playerid, player in data.players.items():
            if player.club == clubid:
                name = display.name(player)

                self.liststorePlayers.append([playerid, name])

    def selection_changed(self, treeselection):
        if treeselection.count_selected_rows() > 0:
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonRemove.set_sensitive(False)


class AddNationDialog(Gtk.Dialog):
    state = False

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.connect("response", self.response_handler)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        self.buttonSave = widgets.Button()
        self.buttonSave.connect("clicked", self.save_handler)
        action_area = self.get_action_area()
        action_area.add(self.buttonSave)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Denonym")
        grid.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        label.set_mnemonic_widget(self.entryDenonym)
        grid.attach(self.entryDenonym, 1, 1, 1, 1)

    def save_handler(self, button):
        self.save_data(nationid=self.current)
        self.clear_fields()

        self.state = True

        self.hide()

    def save_data(self, nationid):
        if nationid is None:
            data.idnumbers.nationid += 1

            nation = Nation()
            data.nations[data.idnumbers.nationid] = nation
        else:
            nation = data.nations[nationid]

        nation.name = self.entryName.get_text()
        nation.denonym = self.entryDenonym.get_text()

    def response_handler(self, dialog, response):
        self.hide()

    def display(self, nationid=None):
        if nationid is None:
            self.set_title("Add Nation")
            self.buttonSave.set_label("_Add")

            self.current = None
        else:
            self.set_title("Edit Nation")
            self.buttonSave.set_label("_Edit")
            self.buttonSave.set_sensitive(True)

            self.load_fields(nationid)

            self.current = nationid

        self.show_all()
        self.run()

    def load_fields(self, nationid):
        nation = data.nations[nationid]

        self.entryName.set_text(nation.name)
        self.entryDenonym.set_text(nation.denonym)

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryDenonym.set_text("")


class AddStadiumDialog(Gtk.Dialog):
    state = False

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.connect("response", self.response_handler)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        self.buttonSave = widgets.Button()
        self.buttonSave.connect("clicked", self.save_handler)
        action_area = self.get_action_area()
        action_area.add(self.buttonSave)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        grid.attach(self.entryName, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        grid.attach(notebook, 0, 1, 3, 1)

        grid1 = Gtk.Grid()
        grid1.set_border_width(5)
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        notebook.append_page(grid1, Gtk.Label("Stand"))

        self.capacities = []

        for count, stand in enumerate(("North", "West", "South", "East", "North West", "North East", "South West", "South East")):
            label = widgets.Label(stand)
            grid1.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_value(0)

            if count < 4:
                spinbutton.set_range(0, 15000)
            else:
                spinbutton.set_range(0, 3000)

            spinbutton.set_increments(1000, 1000)
            self.capacities.append(spinbutton)
            grid1.attach(spinbutton, 1, count, 1, 1)

        grid2 = Gtk.Grid()
        grid2.set_border_width(5)
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        notebook.append_page(grid2, Gtk.Label("Buildings"))

        self.buildings = []

        for count, building in enumerate(("Stall", "Programme Vendor", "Small Shop", "Large Shop", "Bar", "Burger Bar", "Cafe", "Restaurant")):
            label = widgets.Label(building)
            grid2.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_value(0)
            spinbutton.set_range(0, 8)
            spinbutton.set_increments(1, 1)
            self.buildings.append(spinbutton)
            grid2.attach(spinbutton, 1, count, 1, 1)

    def display(self, stadiumid=None):
        if stadiumid is None:
            self.set_title("Add Stadium")
            self.buttonSave.set_label("_Add")

            self.current = None
        else:
            self.set_title("Edit Stadium")
            self.buttonSave.set_label("_Edit")

            self.load_fields(stadiumid)

            self.current = stadiumid

        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        self.clear_fields()

        self.hide()

    def save_handler(self, button):
        self.save_data(stadiumid=self.current)
        self.clear_fields()

        self.state = True

        self.hide()

    def save_data(self, stadiumid):
        if stadiumid is None:
            data.idnumbers.stadiumid += 1

            stadium = Stadium()
            data.stadiums[data.idnumbers.stadiumid] = stadium
        else:
            stadium = data.stadiums[stadiumid]

        stadium.name = self.entryName.get_text()

    def load_fields(self, stadiumid):
        stadium = data.stadiums[stadiumid]

        self.entryName.set_text(stadium.name)

        for count, widget in enumerate(self.capacities):
            widget.set_value(stadium.stands[count])

        '''
        for count, widget in enumerate(buildings):
            widget.set_value(stadium.buildings[count])
        '''

    def clear_fields(self):
        self.entryName.set_text("")

        for count, widget in enumerate(self.capacities):
            widget.set_value(0)


class PlayerSelectionDialog(Gtk.Dialog):
    def __init__(self):
        def treeselection_changed(treeselection):
            if treeselection.count_selected_rows() == 0:
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.set_response_sensitive(Gtk.ResponseType.OK, True)

        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_default_size(-1, 250)
        self.set_title("Select Player")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststore = Gtk.ListStore(int, str)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.liststore)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def display(self, parent):
        self.set_transient_for(parent)
        self.populate(data.players)
        self.entrySearch.set_text("")

        self.set_focus(self.entrySearch)
        self.show_all()

        player = None

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()

            if treeiter:
                player = model[treeiter][0]

        self.hide()

        return player

    def activate_search(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            items = {}

            for playerid, player in data.players.items():
                both = "%s %s" % (player.first_name, player.second_name)

                for search in (player.second_name, player.first_name, player.common_name, both):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        items[playerid] = player

                        break

            self.populate(items)

    def clear_search(self, entry, icon, event):
        entry.set_text("")

        self.populate(data.players)

    def populate(self, data):
        self.liststore.clear()

        for playerid, player in data.items():
            name = display.name(player)
            self.liststore.append([playerid, name])


class ClubSelectionDialog(Gtk.Dialog):
    def __init__(self):
        def treeselection_changed(treeselection):
            if treeselection.count_selected_rows() == 0:
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.set_response_sensitive(Gtk.ResponseType.OK, True)

            model, treeiter = treeselection.get_selected()

            if treeiter:
                treepath = model.get_path(treeiter)
                treeview.scroll_to_cell(treepath)

        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_default_size(-1, 250)
        self.set_title("Select Club")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststore = Gtk.ListStore(int, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def activate_search(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            items = {}

            for clubid, club in data.clubs.items():
                for search in (club.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        items[clubid] = club

                        break

            self.populate(items)

    def clear_search(self, entry, icon, event):
        entry.set_text("")

        self.populate(data.clubs)

    def display(self, parent, clubid):
        self.set_transient_for(parent)
        self.populate(data.clubs)

        for item in self.treemodelsort:
            if item[0] == clubid:
                self.treeselection.select_iter(item.iter)

        self.set_focus(self.entrySearch)
        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            clubid = model[treeiter][0]

        self.hide()

        return clubid

    def populate(self, data):
        self.liststore.clear()

        for clubid, club in data.items():
            self.liststore.append([clubid, club.name])


class DateOfBirth(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(parent)
        self.set_title("Date of Birth")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        self.calendar = Gtk.Calendar()
        self.calendar.set_property("year", True)
        self.vbox.add(self.calendar)

    def display(self, date):
        year, month, day = list(map(int, date))

        self.calendar.select_day(day)
        self.calendar.select_month(month - 1, year)

        self.show_all()

        date_of_birth = year, month, day

        if self.run() == Gtk.ResponseType.OK:
            year, month, day = self.calendar.get_date()

            age = data.season - year

            if (month, day) > (8, 1):
                age -= 1

            if day < 10:
                day = "0%i" % (day)
            else:
                day = str(day)

            month += 1

            if month < 10:
                month = "0%i" % (month)
            else:
                month = str(month)

            date_of_birth = [year, month, day]

        self.hide()

        return date_of_birth


def remove_dialog(index, parent):
    item = ("Player", "Club", "Nation", "Stadium")[index]

    dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    dialog.set_transient_for(parent)
    dialog.set_title("Remove %s" % (item))
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Remove", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.CANCEL)
    dialog.set_markup("Remove %s from database?" % (item.lower()))

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        state = True

    dialog.destroy()

    return state


def open_dialog():
    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title("Open File")
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Open", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("Database")
    filefilter.add_pattern("*.db")
    dialog.add_filter(filefilter)

    filename = None

    if dialog.run() == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()

    return filename


def save_dialog():
    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title("Save File")
    dialog.set_action(Gtk.FileChooserAction.SAVE)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Save", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("Database")
    filefilter.add_pattern("*.db")
    dialog.add_filter(filefilter)

    filename = None

    if dialog.run() == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()

    return filename


def quit_dialog():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Quit Editor")
    messagedialog.add_button("_Do Not Quit", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Quit", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("Quit the data editor?")

    state = 0

    response = messagedialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        state = 1

    messagedialog.destroy()

    return state


def error(errorid):
    errors = {0: "Unable to delete club as a player is still assigned to it.",
              1: "Unable to delete nation as a player is still assigned to it.",
              2: "Unable to delete stadium as a club is still assigned to it.",
              }

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Error")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("<span size='12000'><b>Foreign key error</b></span>")
    messagedialog.format_secondary_text(errors[errorid])

    messagedialog.run()
    messagedialog.destroy()
