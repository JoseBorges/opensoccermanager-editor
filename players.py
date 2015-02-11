#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import display
import widgets


class Player:
    pass


class Players(Gtk.Grid):
    selected = None

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 2, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str, str,
                                       str, str, int, int, int, int,
                                       int, int, int, int, int, int)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_clickable(True)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeview.connect("key-press-event", self.row_delete)
        treeview.connect("row-activated", self.row_activated)
        self.treeselection = treeview.get_selection()
        self.treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = widgets.TreeViewColumn(title="First Name", column=1)
        treeviewcolumn.set_sort_column_id(1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Second Name", column=2)
        treeviewcolumn.set_sort_column_id(2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Common Name", column=3)
        treeviewcolumn.set_sort_column_id(3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Date of Birth", column=4)
        treeviewcolumn.set_sort_column_id(4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=5)
        treeviewcolumn.set_sort_column_id(5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nation", column=6)
        treeviewcolumn.set_sort_column_id(6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=7)
        treeviewcolumn.set_sort_column_id(7)
        treeview.append_column(treeviewcolumn)

        for count, item in enumerate(data.skill, start=8):
            label = Gtk.Label(data.skill_short[count - 8])
            label.set_tooltip_text(item)
            label.show()
            treeviewcolumn = widgets.TreeViewColumn(title="", column=count)
            treeviewcolumn.set_widget(label)
            treeviewcolumn.set_sort_column_id(count)
            treeview.append_column(treeviewcolumn)

        treeviewcolumn = widgets.TreeViewColumn(title="Training", column=17)
        treeviewcolumn.set_sort_column_id(17)
        treeview.append_column(treeviewcolumn)

        self.labelCount = widgets.Label()
        self.attach(self.labelCount, 0, 1, 1, 1)

        self.labelSelected = widgets.Label()
        self.labelSelected.set_hexpand(True)
        self.attach(self.labelSelected, 1, 1, 1, 1)

        # Context menu
        contextmenu = Gtk.Menu()
        menuitem = widgets.MenuItem("_Edit Item")
        menuitem.connect("activate", self.row_edit_by_menu)
        contextmenu.append(menuitem)
        menuitem = widgets.MenuItem("_Remove Item")
        menuitem.connect("activate", self.row_delete_by_menu)
        contextmenu.append(menuitem)
        treeview.connect("button-press-event", self.context_menu, contextmenu)

    def context_menu(self, treeview, event, contextmenu):
        if event.button == 3:
            contextmenu.show_all()
            contextmenu.popup(None, None, None, None, event.button, event.time)

    def row_edit_by_menu(self, menuitem):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            playerid = model[treepath][0]

            playerid = [playerid]
            dialogs.players.display(playerid)

            if dialogs.players.state:
                self.populate()

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        playerid = model[path][0]

        playerid = [playerid]
        dialogs.players.display(playerid)

        if dialogs.players.state:
            self.populate()

    def row_delete_by_menu(self, menuitem):
        if data.options.confirm_remove:
            state = dialogs.remove_dialog(index=0, parent=widgets.window)
        else:
            state = True

        if state:
            model, treepath = self.treeselection.get_selected_rows()

            for item in treepath:
                playerid = model[item][0]
                del(data.players[playerid])

            self.populate()

    def row_delete(self, widget, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=0, parent=widgets.window)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()

                for item in treepath:
                    playerid = model[item][0]
                    del(data.players[playerid])

                self.populate()

    def selection_changed(self, treeselection):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            self.selected = []

            for item in treepath:
                value = model[item][0]
                self.selected.append(value)

            widgets.window.menuitemEdit.set_sensitive(True)
            widgets.window.menuitemRemove.set_sensitive(True)
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None
            widgets.window.menuitemEdit.set_sensitive(False)
            widgets.window.menuitemRemove.set_sensitive(False)
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

        count = self.treeselection.count_selected_rows()

        if count == 0:
            self.labelSelected.set_label("")
        elif count == 1:
            self.labelSelected.set_label("(1 Item Selected)")
        else:
            self.labelSelected.set_label("(%i Items Selected)" % (count))

    def populate(self):
        self.liststore.clear()

        count = 0

        for count, (playerid, player) in enumerate(data.players.items(), start=1):
            club = display.club(player)
            nationality = data.nations[player.nationality].name

            self.liststore.append([playerid,
                                   player.first_name,
                                   player.second_name,
                                   player.common_name,
                                   player.date_of_birth,
                                   club,
                                   nationality,
                                   player.position,
                                   player.keeping,
                                   player.tackling,
                                   player.passing,
                                   player.shooting,
                                   player.heading,
                                   player.pace,
                                   player.stamina,
                                   player.ball_control,
                                   player.set_pieces,
                                   player.training_value])

        self.labelCount.set_label("%i Players in Database" % (count))

    def populate_search(self, values):
        self.liststore.clear()

        for playerid, player in values.items():
            club = display.club(player)
            nationality = data.nations[player.nationality].name

            self.liststore.append([playerid,
                                   player.first_name,
                                   player.second_name,
                                   player.common_name,
                                   player.date_of_birth,
                                   club,
                                   nationality,
                                   player.position,
                                   player.keeping,
                                   player.tackling,
                                   player.passing,
                                   player.shooting,
                                   player.heading,
                                   player.pace,
                                   player.stamina,
                                   player.ball_control,
                                   player.set_pieces,
                                   player.training_value])

    def run(self):
        self.populate()

        self.show_all()


class AddPlayerDialog(Gtk.Dialog):
    state = False

    def __init__(self):
        def free_agent_changed(checkbutton):
            if checkbutton.get_active():
                self.buttonClub.set_sensitive(False)
                self.buttonClub.set_label("")
            else:
                self.buttonClub.set_sensitive(True)

        self.date = 0
        self.selected_club = 0
        self.selected_nation = 0

        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.connect("response", self.response_handler)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        self.buttonSave = widgets.Button()
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

        label = widgets.Label("_Nationality")
        grid.attach(label, 0, 5, 1, 1)
        self.buttonNation = widgets.Button()
        label.set_mnemonic_widget(self.buttonNation)
        self.buttonNation.connect("clicked", self.nation_change)
        grid.attach(self.buttonNation, 1, 5, 1, 1)

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

        self.clubselectiondialog = dialogs.ClubSelectionDialog(parent=self)
        self.nationselectiondialog = dialogs.NationSelectionDialog(parent=self)
        self.dob = dialogs.DateOfBirth(parent=self)

    def club_change(self, button):
        if self.current is not None:
            clubid = data.players[self.current].club

            if self.selected_club != clubid:
                clubid = self.selected_club
        else:
            clubid = None

        clubid = self.clubselectiondialog.display(clubid=clubid)

        if clubid is not None:
            self.selected_club = clubid
            self.buttonClub.set_label("%s" % (data.clubs[clubid].name))
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

    def nation_change(self, button):
        if self.selected_nation != 0:
            nationid = self.selected_nation
        else:
            nationid = None

        nationid = self.nationselectiondialog.display(nationid=nationid)

        if nationid is not None:
            self.selected_nation = nationid
            self.buttonNation.set_label("%s" % (data.nations[nationid].name))
            self.buttonSave.set_sensitive(True)
        else:
            self.selected_nation = 0
            self.buttonNation.set_label("")
            self.buttonSave.set_sensitive(False)

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

        player.nationality = self.selected_nation

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
            self.buttonSave.set_sensitive(False)

            self.current = None
        else:
            self.set_title("Edit Player")
            self.buttonSave.set_label("_Edit")
            self.buttonSave.set_sensitive(True)
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
            self.checkbuttonFreeAgent.set_active(False)
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

        self.selected_nation = player.nationality
        self.buttonNation.set_label("%s" % (data.nations[player.nationality].name))

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
        self.buttonNation.set_label("")

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
