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


def add_player_dialog(playerid=None):
    def date_of_birth(button):
        dialog = Gtk.Dialog()
        dialog.set_title("Date Of Birth")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        dialog.vbox.add(calendar)

        dialog.show_all()

        if dialog.run() == Gtk.ResponseType.OK:
            year, month, day = calendar.get_date()

            if day < 10:
                day = "0%i" % (day)
            else:
                day = "%i" % (day)

            month = month + 1

            if month < 10:
                month = "0%i" % (month)
            else:
                month = "%i" % (month)

            date_of_birth = "%i-%s-%s" % (year, month, day)

            buttonDateOfBirth.set_label("%s" % (date_of_birth))

        dialog.destroy()

    if playerid is None:
        title = "Add Player"
        button = "_Add"
    else:
        title = "Edit Player"
        button = "_Edit"

    liststoreClub = Gtk.ListStore(str, str)
    treemodelsort = Gtk.TreeModelSort(liststoreClub)
    treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

    for clubid, club in data.clubs.items():
        liststoreClub.append([str(clubid), club.name])

    liststoreNationality = Gtk.ListStore(str, str)

    for nationid, nation in data.nations.items():
        liststoreNationality.append([str(nationid), nation.name])

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

    label = widgets.Label("First Name")
    grid.attach(label, 0, 0, 1, 1)
    entryFirstName = Gtk.Entry()
    grid.attach(entryFirstName, 1, 0, 2, 1)
    label = widgets.Label("Second Name")
    grid.attach(label, 0, 1, 1, 1)
    entrySecondName = Gtk.Entry()
    grid.attach(entrySecondName, 1, 1, 2, 1)
    label = widgets.Label("Common Name")
    grid.attach(label, 0, 2, 1, 1)
    entryCommonName = Gtk.Entry()
    grid.attach(entryCommonName, 1, 2, 2, 1)

    label = widgets.Label("Date Of Birth")
    grid.attach(label, 0, 3, 1, 1)
    buttonDateOfBirth = widgets.Button()
    buttonDateOfBirth.connect("clicked", date_of_birth)
    grid.attach(buttonDateOfBirth, 1, 3, 1, 1)

    calendar = Gtk.Calendar()
    calendar.set_property("year", True)

    cellrenderertext = Gtk.CellRendererText()

    label = widgets.Label("Club")
    grid.attach(label, 0, 4, 1, 1)
    comboboxClub = Gtk.ComboBox()
    comboboxClub.set_model(treemodelsort)
    comboboxClub.set_id_column(0)
    comboboxClub.pack_start(cellrenderertext, True)
    comboboxClub.add_attribute(cellrenderertext, "text", 1)
    grid.attach(comboboxClub, 1, 4, 1, 1)

    label = widgets.Label("Nationality")
    grid.attach(label, 0, 5, 1, 1)
    comboboxNationality = Gtk.ComboBox()
    comboboxNationality.set_model(liststoreNationality)
    comboboxNationality.set_id_column(0)
    comboboxNationality.pack_start(cellrenderertext, True)
    comboboxNationality.add_attribute(cellrenderertext, "text", 1)
    grid.attach(comboboxNationality, 1, 5, 1, 1)

    label = widgets.Label("Position")
    grid.attach(label, 0, 6, 1, 1)
    comboboxPosition = Gtk.ComboBoxText()
    grid.attach(comboboxPosition, 1, 6, 1, 1)

    for position in ("GK", "DL", "DR", "DC", "D", "ML", "MR", "MC", "M", "AS", "AF"):
        comboboxPosition.append(position, position)

    grid1 = Gtk.Grid()
    grid1.set_row_spacing(5)
    grid1.set_column_spacing(5)
    grid.attach(grid1, 0, 7, 6, 1)

    spinbuttons = []

    label = widgets.Label("Keeping")
    grid1.attach(label, 0, 0, 1, 1)
    spinbuttonKP = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonKP, 1, 0, 1, 1)
    spinbuttons.append(spinbuttonKP)

    label = widgets.Label("Tackling")
    grid1.attach(label, 0, 1, 1, 1)
    spinbuttonTK = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonTK, 1, 1, 1, 1)
    spinbuttons.append(spinbuttonTK)

    label = widgets.Label("Passing")
    grid1.attach(label, 0, 2, 1, 1)
    spinbuttonPS = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonPS, 1, 2, 1, 1)
    spinbuttons.append(spinbuttonPS)

    label = widgets.Label("Shooting")
    grid1.attach(label, 2, 0, 1, 1)
    spinbuttonSH = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonSH, 3, 0, 1, 1)
    spinbuttons.append(spinbuttonSH)

    label = widgets.Label("Heading")
    grid1.attach(label, 2, 1, 1, 1)
    spinbuttonHD = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonHD, 3, 1, 1, 1)
    spinbuttons.append(spinbuttonHD)

    label = widgets.Label("Pace")
    grid1.attach(label, 2, 2, 1, 1)
    spinbuttonPC = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonPC, 3, 2, 1, 1)
    spinbuttons.append(spinbuttonPC)

    label = widgets.Label("Stamina")
    grid1.attach(label, 4, 0, 1, 1)
    spinbuttonST = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonST, 5, 0, 1, 1)
    spinbuttons.append(spinbuttonST)

    label = widgets.Label("Ball Control")
    grid1.attach(label, 4, 1, 1, 1)
    spinbuttonBC = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonBC, 5, 1, 1, 1)
    spinbuttons.append(spinbuttonBC)

    label = widgets.Label("Set Pieces")
    grid1.attach(label, 4, 2, 1, 1)
    spinbuttonSP = Gtk.SpinButton.new_with_range(1, 99, 1)
    grid1.attach(spinbuttonSP, 5, 2, 1, 1)
    spinbuttons.append(spinbuttonSP)

    label = widgets.Label("Training Value")
    grid.attach(label, 0, 8, 1, 1)
    spinbuttonTraining = Gtk.SpinButton.new_with_range(1, 10, 1)
    grid.attach(spinbuttonTraining, 1, 8, 1, 1)

    state = False

    if playerid is not None:
        player = data.players[playerid]

        entryFirstName.set_text(player.first_name)
        entrySecondName.set_text(player.second_name)
        entryCommonName.set_text(player.common_name)
        buttonDateOfBirth.set_label("%s" % (player.date_of_birth))
        comboboxClub.set_active_id(str(player.club))
        comboboxNationality.set_active_id(str(player.nationality))

        date = player.date_of_birth.split("-")
        date_of_birth = list(map(int, date))

        calendar.select_day(date_of_birth[2])
        calendar.select_month(date_of_birth[1] - 1, date_of_birth[0])

        comboboxPosition.set_active_id(player.position)

        spinbuttons[0].set_value(player.keeping)
        spinbuttons[1].set_value(player.tackling)
        spinbuttons[2].set_value(player.passing)
        spinbuttons[3].set_value(player.shooting)
        spinbuttons[4].set_value(player.heading)
        spinbuttons[5].set_value(player.pace)
        spinbuttons[6].set_value(player.stamina)
        spinbuttons[7].set_value(player.ball_control)
        spinbuttons[8].set_value(player.set_pieces)
        spinbuttonTraining.set_value(player.training_value)

    dialog.show_all()

    if dialog.run() == Gtk.ResponseType.OK:
        if playerid is not None:
            player = data.players[playerid]
        else:
            data.idnumbers.playerid += 1

            player = Player()
            data.players[data.idnumbers.playerid] = player

        player.first_name = entryFirstName.get_text()
        player.second_name = entrySecondName.get_text()
        player.common_name = entryCommonName.get_text()
        player.club = int(comboboxClub.get_active_id())
        player.nationality = int(comboboxNationality.get_active_id())

        year, month, day = calendar.get_date()

        if day < 10:
            day = "0%i" % (day)
        else:
            day = "%i" % (day)

        month = month + 1

        if month < 10:
            month = "0%i" % (month)
        else:
            month = "%i" % (month)

        player.date_of_birth = ("%i-%s-%s" % (year, month, day))

        player.position = comboboxPosition.get_active_id()

        player.keeping = spinbuttonKP.get_value_as_int()
        player.tackling = spinbuttonTK.get_value_as_int()
        player.passing = spinbuttonPS.get_value_as_int()
        player.shooting = spinbuttonSH.get_value_as_int()
        player.heading = spinbuttonHD.get_value_as_int()
        player.pace = spinbuttonPC.get_value_as_int()
        player.stamina = spinbuttonST.get_value_as_int()
        player.ball_control = spinbuttonBC.get_value_as_int()
        player.set_pieces = spinbuttonSP.get_value_as_int()
        player.training_value = spinbuttonTraining.get_value_as_int()

        state = True

    dialog.destroy()

    return state


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
