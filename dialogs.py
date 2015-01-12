#!/usr/bin/env python

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os

import widgets
import data


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
    aboutdialog.set_license_type(Gtk.License.GPL_3_0)
    aboutdialog.set_logo(icon)

    aboutdialog.run()
    aboutdialog.destroy()


class AddPlayerDialog(Gtk.Dialog):
    playerid = None
    state = False

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.connect("response", self.response_handler)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        action_area = self.get_action_area()

        self.buttonSave = widgets.Button()
        self.buttonSave.connect("clicked", self.save_handler)
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

        label = widgets.Label("First Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryFirstName = Gtk.Entry()
        grid.attach(self.entryFirstName, 1, 0, 2, 1)
        label = widgets.Label("Second Name")
        grid.attach(label, 0, 1, 1, 1)
        self.entrySecondName = Gtk.Entry()
        grid.attach(self.entrySecondName, 1, 1, 2, 1)
        label = widgets.Label("Common Name")
        grid.attach(label, 0, 2, 1, 1)
        self.entryCommonName = Gtk.Entry()
        grid.attach(self.entryCommonName, 1, 2, 2, 1)

        label = widgets.Label("Date Of Birth")
        grid.attach(label, 0, 3, 1, 1)
        self.buttonDateOfBirth = widgets.Button()
        self.buttonDateOfBirth.connect("clicked", self.date_of_birth)
        grid.attach(self.buttonDateOfBirth, 1, 3, 1, 1)

        self.calendar = Gtk.Calendar()
        self.calendar.set_property("year", True)

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.Label("Club")
        grid.attach(label, 0, 4, 1, 1)
        self.comboboxClub = Gtk.ComboBox()
        self.comboboxClub.set_model(treemodelsortClub)
        self.comboboxClub.set_id_column(0)
        self.comboboxClub.pack_start(cellrenderertext, True)
        self.comboboxClub.add_attribute(cellrenderertext, "text", 1)
        grid.attach(self.comboboxClub, 1, 4, 1, 1)

        label = widgets.Label("Nationality")
        grid.attach(label, 0, 5, 1, 1)
        self.comboboxNationality = Gtk.ComboBox()
        self.comboboxNationality.set_model(treemodelsortNationality)
        self.comboboxNationality.set_id_column(0)
        self.comboboxNationality.pack_start(cellrenderertext, True)
        self.comboboxNationality.add_attribute(cellrenderertext, "text", 1)
        grid.attach(self.comboboxNationality, 1, 5, 1, 1)

        label = widgets.Label("Position")
        grid.attach(label, 0, 6, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        grid.attach(self.comboboxPosition, 1, 6, 1, 1)

        for position in ("GK", "DL", "DR", "DC", "D", "ML", "MR", "MC", "M", "AS", "AF"):
            self.comboboxPosition.append(position, position)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 7, 6, 1)

        label = widgets.Label("Keeping")
        grid1.attach(label, 0, 0, 1, 1)
        self.spinbuttonKP = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonKP, 1, 0, 1, 1)

        label = widgets.Label("Tackling")
        grid1.attach(label, 0, 1, 1, 1)
        self.spinbuttonTK = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonTK, 1, 1, 1, 1)

        label = widgets.Label("Passing")
        grid1.attach(label, 0, 2, 1, 1)
        self.spinbuttonPS = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonPS, 1, 2, 1, 1)

        label = widgets.Label("Shooting")
        grid1.attach(label, 2, 0, 1, 1)
        self.spinbuttonSH = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonSH, 3, 0, 1, 1)

        label = widgets.Label("Heading")
        grid1.attach(label, 2, 1, 1, 1)
        self.spinbuttonHD = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonHD, 3, 1, 1, 1)

        label = widgets.Label("Pace")
        grid1.attach(label, 2, 2, 1, 1)
        self.spinbuttonPC = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonPC, 3, 2, 1, 1)

        label = widgets.Label("Stamina")
        grid1.attach(label, 4, 0, 1, 1)
        self.spinbuttonST = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonST, 5, 0, 1, 1)

        label = widgets.Label("Ball Control")
        grid1.attach(label, 4, 1, 1, 1)
        self.spinbuttonBC = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonBC, 5, 1, 1, 1)

        label = widgets.Label("Set Pieces")
        grid1.attach(label, 4, 2, 1, 1)
        self.spinbuttonSP = Gtk.SpinButton.new_with_range(1, 99, 1)
        grid1.attach(self.spinbuttonSP, 5, 2, 1, 1)

        label = widgets.Label("Training Value")
        grid.attach(label, 0, 8, 1, 1)
        self.spinbuttonTraining = Gtk.SpinButton.new_with_range(1, 10, 1)
        grid.attach(self.spinbuttonTraining, 1, 8, 1, 1)

    def date_of_birth(self, button):
        dialog = Gtk.Dialog()
        dialog.set_transient_for(self)
        dialog.set_title("Date Of Birth")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.vbox.add(self.calendar)

        dialog.show_all()

        if dialog.run() == Gtk.ResponseType.OK:
            year, month, day = self.calendar.get_date()

            if day < 10:
                day = "0%i" % (day)

            month = month + 1

            if month < 10:
                month = "0%i" % (month)

            date_of_birth = "%i-%s-%s" % (year, month, day)
            self.buttonDateOfBirth.set_label("%s" % (date_of_birth))

        dialog.destroy()

    def response_handler(self, dialog, response):
        self.hide()

    def save_handler(self, button):
        self.save_data(self.current)
        self.clear_fields()

        self.state = True

        try:
            self.current = self.generator.__next__()
            self.load_fields(self.current)
        except StopIteration:
            self.hide()

        if self.checkbuttonMulti.get_visible():
            if not self.checkbuttonMulti.get_active():
                self.hide()

    def save_data(self, playerid):
        if self.playerid is None:
            data.idnumbers.playerid += 1

            player = Player()
            data.players[data.idnumbers.playerid] = player
        else:
            player = data.players[playerid]

        player.first_name = self.entryFirstName.get_text()
        player.second_name = self.entrySecondName.get_text()
        player.common_name = self.entryCommonName.get_text()
        player.club = int(self.comboboxClub.get_active_id())
        player.nationality = int(self.comboboxNationality.get_active_id())

        year, month, day = self.calendar.get_date()

        if day < 10:
            day = "0%i" % (day)

        month = month + 1

        if month < 10:
            month = "0%i" % (month)

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

    def display(self, playerid):
        self.state = False
        self.playerid = playerid

        self.liststoreClub.clear()
        self.liststoreNationality.clear()

        for clubid, club in data.clubs.items():
            self.liststoreClub.append([str(clubid), club.name])

        for nationid, nation in data.nations.items():
            self.liststoreNationality.append([str(nationid), nation.name])

        buttonSave = self.get_widget_for_response(Gtk.ResponseType.OK)

        self.show_all()

        if playerid is None:
            self.set_title("Add Player")
            self.buttonSave.set_label("_Add")

            self.clear_fields()
        else:
            self.set_title("Edit Player")
            self.buttonSave.set_label("_Edit")
            self.checkbuttonMulti.set_visible(False)

            self.generator = self.playerid.__iter__()
            self.current = self.generator.__next__()

            self.load_fields(self.current)

        self.run()

    def load_fields(self, playerid):
        player = data.players[playerid]

        self.entryFirstName.set_text(player.first_name)
        self.entrySecondName.set_text(player.second_name)
        self.entryCommonName.set_text(player.common_name)
        self.buttonDateOfBirth.set_label("%s" % (player.date_of_birth))
        self.comboboxClub.set_active_id(str(player.club))
        self.comboboxNationality.set_active_id(str(player.nationality))

        date = player.date_of_birth.split("-")
        date_of_birth = list(map(int, date))

        self.calendar.select_day(date_of_birth[2])
        self.calendar.select_month(date_of_birth[1] - 1, date_of_birth[0])

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
        self.comboboxClub.set_active(-1)
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


def add_club_dialog(clubid=None):
    if clubid is None:
        title = "Add Club"
        button = "_Add"
    else:
        title = "Edit Club"
        button = "_Edit"

    dialog = Gtk.Dialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title(title)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button(button, Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    liststore = Gtk.ListStore(str, str)
    [liststore.append([str(stadiumid), stadium.name]) for stadiumid, stadium in data.stadiums.items()]

    label = widgets.Label("Name")
    grid.attach(label, 0, 0, 1, 1)
    entryName = Gtk.Entry()
    grid.attach(entryName, 1, 0, 1, 1)

    label = widgets.Label("Nickname")
    grid.attach(label, 0, 1, 1, 1)
    entryNickname = Gtk.Entry()
    grid.attach(entryNickname, 1, 1, 1, 1)

    label = widgets.Label("Manager")
    grid.attach(label, 0, 2, 1, 1)
    entryManager = Gtk.Entry()
    grid.attach(entryManager, 1, 2, 1, 1)

    label = widgets.Label("Chairman")
    grid.attach(label, 0, 3, 1, 1)
    entryChairman = Gtk.Entry()
    grid.attach(entryChairman, 1, 3, 1, 1)

    label = widgets.Label("Stadium")
    grid.attach(label, 0, 4, 1, 1)
    comboboxStadium = Gtk.ComboBox()
    comboboxStadium.set_id_column(0)
    comboboxStadium.set_model(liststore)
    cellrenderertext = Gtk.CellRendererText()
    comboboxStadium.pack_start(cellrenderertext, True)
    comboboxStadium.add_attribute(cellrenderertext, "text", 1)
    grid.attach(comboboxStadium, 1, 4, 1, 1)

    label = widgets.Label("Reputation")
    grid.attach(label, 0, 5, 1, 1)
    spinbuttonReputation = Gtk.SpinButton.new_with_range(1, 20, 1)
    grid.attach(spinbuttonReputation, 1, 5, 1, 1)

    if clubid is not None:
        club = data.clubs[clubid]

        entryName.set_text(club.name)
        entryNickname.set_text(club.nickname)
        entryManager.set_text(club.manager)
        entryChairman.set_text(club.chairman)
        comboboxStadium.set_active_id(str(club.stadium))
        spinbuttonReputation.set_value(club.reputation)

    dialog.show_all()

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        if clubid is not None:
            club = data.clubs[clubid]
        else:
            data.idnumbers.clubid += 1

            club = Club()
            data.clubs[data.idnumbers.clubid] = club

        club.name = entryName.get_text()
        club.nickname = entryNickname.get_text()
        club.manager = entryManager.get_text()
        club.chairman = entryChairman.get_text()
        club.stadium = int(comboboxStadium.get_active_id())
        club.reputation = spinbuttonReputation.get_value_as_int()

        state = True

    dialog.destroy()

    return state


def add_nation_dialog(nationid=None):
    if nationid is None:
        title = "Add Nation"
        button = "_Add"
    else:
        title = "Edit Nation"
        button = "_Edit"

    dialog = Gtk.Dialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title(title)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button(button, Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.Label("Name")
    grid.attach(label, 0, 0, 1, 1)
    entryName = Gtk.Entry()
    grid.attach(entryName, 1, 0, 1, 1)

    label = widgets.Label("Denonym")
    grid.attach(label, 0, 1, 1, 1)
    entryDenonym = Gtk.Entry()
    grid.attach(entryDenonym, 1, 1, 1, 1)

    if nationid is not None:
        nation = data.nations[nationid]

        entryName.set_text(nation.name)
        entryDenonym.set_text(nation.denonym)

    dialog.show_all()

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        if nationid is not None:
            nation = data.nations[nationid]
        else:
            data.idnumbers.nationid += 1

            nation = Nation()
            data.nations[data.idnumbers.nationid] = nation

        nation.name = entryName.get_text()
        nation.denonym = entryDenonym.get_text()

        state = True

    dialog.destroy()

    return state


def add_stadium_dialog(stadiumid=None):
    if stadiumid is None:
        title = "Add Stadium"
        button = "_Add"
    else:
        title = "Edit Stadium"
        button = "_Edit"

        stadium = data.stadiums[stadiumid]

    dialog = Gtk.Dialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title(title)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button(button, Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.Label("Name")
    grid.attach(label, 0, 0, 1, 1)
    entryName = Gtk.Entry()
    grid.attach(entryName, 1, 0, 1, 1)

    notebook = Gtk.Notebook()
    notebook.set_hexpand(True)
    grid.attach(notebook, 0, 1, 3, 1)

    grid1 = Gtk.Grid()
    grid1.set_border_width(5)
    grid1.set_row_spacing(5)
    grid1.set_column_spacing(5)
    notebook.append_page(grid1, Gtk.Label("Stand"))

    capacities = []

    for count, stand in enumerate(("North", "West", "South", "East", "North West", "North East", "South West", "South East")):
        label = widgets.Label(stand)
        grid1.attach(label, 0, count, 1, 1)

        spinbutton = Gtk.SpinButton()

        if count < 4:
            spinbutton.set_range(0, 15000)
        else:
            spinbutton.set_range(0, 3000)

        spinbutton.set_increments(1000, 1000)
        spinbutton.set_value(stadium.stands[count])

        grid1.attach(spinbutton, 1, count, 1, 1)

    grid2 = Gtk.Grid()
    grid2.set_border_width(5)
    grid2.set_row_spacing(5)
    grid2.set_column_spacing(5)
    notebook.append_page(grid2, Gtk.Label("Buildings"))

    buildings = []

    for count, building in enumerate(("Stall", "Programme Vendor", "Small Shop", "Large Shop", "Bar", "Burger Bar", "Cafe", "Restaurant")):
        label = widgets.Label(building)
        grid2.attach(label, 0, count, 1, 1)

        spinbutton = Gtk.SpinButton()
        spinbutton.set_range(0, 8)
        spinbutton.set_increments(1, 1)
        spinbutton.set_value(stadium.buildings[count])
        buildings.append(spinbutton)
        grid2.attach(spinbutton, 1, count, 1, 1)

    if stadiumid is not None:
        entryName.set_text(stadium.name)

    dialog.show_all()

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        if stadiumid is not None:
            stadium = data.stadiums[stadiumid]
        else:
            data.idnumbers.stadiumid += 1

            stadium = Stadium()
            data.stadiums[data.idnumbers.stadiumid] = stadium

        stadium.name = entryName.get_text()
        stadium.capacity = 0

        state = True

    dialog.destroy()

    return state


def remove_dialog(index):
    item = ("Player", "Club", "Nation", "Stadium")[index]

    dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    dialog.set_transient_for(widgets.window)
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
    dialog.set_title("Open File")
    dialog.set_transient_for(widgets.window)
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Open", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    filename = None

    if dialog.run() == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()

    return filename


def error(errorid):
    errors = {0: "Unable to delete club as a player is still assigned to it.",
              1: "Unable to delete nation as a player is still assigned to it."}

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Error")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("Foreign key error")
    messagedialog.format_secondary_text(errors[errorid])

    messagedialog.run()
    messagedialog.destroy()
