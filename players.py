#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import calculator
import data
import dialogs
import display
import menu
import widgets


class Players(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 2, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str, int, str,
                                       str, str, int, int, int, int,
                                       int, int, int, int, int, int, int, str, int, str)

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

        treeviewcolumn = widgets.TreeViewColumn(title="First Name",
                                                column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Second Name",
                                                column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Common Name",
                                                column=3)
        treeview.append_column(treeviewcolumn)
        self.treeviewcolumnDateOfBirth = widgets.TreeViewColumn(title="Date of Birth",
                                                column=4)
        treeview.append_column(self.treeviewcolumnDateOfBirth)
        self.treeviewcolumnAge = widgets.TreeViewColumn(title="Age",
                                                column=5)
        treeview.append_column(self.treeviewcolumnAge)
        treeviewcolumn = widgets.TreeViewColumn(title="Club",
                                                column=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nation",
                                                column=7)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position",
                                                column=8)
        treeview.append_column(treeviewcolumn)

        for count, item in enumerate(data.skill, start=9):
            label = Gtk.Label(data.skill_short[count - 9])
            label.set_tooltip_text(item)
            label.show()
            treeviewcolumn = widgets.TreeViewColumn(None, column=count)
            treeviewcolumn.set_widget(label)
            treeview.append_column(treeviewcolumn)

        treeviewcolumn = widgets.TreeViewColumn(title="Training",
                                                column=18)
        treeview.append_column(treeviewcolumn)

        cellrenderertext = Gtk.CellRendererText()
        self.treeviewcolumnValue = Gtk.TreeViewColumn("Est. Value", cellrenderertext, text=20)
        self.treeviewcolumnValue.set_sort_column_id(19)
        treeview.append_column(self.treeviewcolumnValue)
        self.treeviewcolumnWage = Gtk.TreeViewColumn("Est. Wage", cellrenderertext, text=22)
        self.treeviewcolumnWage.set_sort_column_id(21)
        treeview.append_column(self.treeviewcolumnWage)

        self.labelCount = widgets.Label()
        self.attach(self.labelCount, 0, 1, 1, 1)

        self.labelSelected = widgets.Label()
        self.labelSelected.set_hexpand(True)
        self.attach(self.labelSelected, 1, 1, 1, 1)

        # Context menu
        contextmenu = menu.ContextMenu()
        contextmenu.menuitemEdit.connect("activate", self.row_edit_by_menu)
        contextmenu.menuitemRemove.connect("activate", self.row_delete)
        treeview.connect("button-press-event", self.context_menu, contextmenu)

    def context_menu(self, treeview, event, contextmenu):
        if event.button == 3:
            contextmenu.show_all()
            contextmenu.popup(None, None, None, None, event.button, event.time)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        playerid = model[path][0]

        playerid = [playerid]
        dialogs.players.display(playerid)

        if dialogs.players.state:
            self.populate()

    def row_edit_by_menu(self, menuitem):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            playerid = model[treepath][0]

            playerid = [playerid]
            dialogs.players.display(playerid)

            if dialogs.players.state:
                self.populate()

    def row_delete(self, widget, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=0)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()

                for item in treepath:
                    playerid = model[item][0]
                    del(data.players[playerid])
                    data.unsaved = True

                self.populate()

    def selection_changed(self, treeselection):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            self.selected = [model[item][0] for item in treepath]

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

    def toggle_age_column(self):
        if data.options.show_age:
            self.treeviewcolumnAge.set_visible(True)
            self.treeviewcolumnDateOfBirth.set_visible(False)
        else:
            self.treeviewcolumnAge.set_visible(False)
            self.treeviewcolumnDateOfBirth.set_visible(True)

    def toggle_value_wage_column(self):
        if data.options.show_value_wage:
            self.treeviewcolumnValue.set_visible(True)
            self.treeviewcolumnWage.set_visible(True)
        else:
            self.treeviewcolumnValue.set_visible(False)
            self.treeviewcolumnWage.set_visible(False)

    def populate(self, items=None):
        self.liststore.clear()

        if items is None:
            items = data.players
            dbcount = True
        else:
            dbcount = False

        count = 0

        for count, (playerid, player) in enumerate(items.items(), start=1):
            club = display.club(player)
            nationality = display.nation(player)

            value = calculator.value(playerid)
            display_value = display.value(value)
            wage = calculator.wage(playerid)
            display_wage = display.wage(wage)

            self.liststore.append([playerid,
                                   player.first_name,
                                   player.second_name,
                                   player.common_name,
                                   player.date_of_birth,
                                   player.age,
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
                                   player.training_value,
                                   value,
                                   display_value,
                                   wage,
                                   display_wage])

        if dbcount:
            self.labelCount.set_label("%i Players in Database" % (count))

    def run(self):
        self.populate()

        self.show_all()

        self.toggle_age_column()
        self.toggle_value_wage_column()


class AddPlayerDialog(Gtk.Dialog):
    def __init__(self):
        self.date = None
        self.state = False
        self.selected_club = 0
        self.selected_nation = 0

        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.set_resizable(False)
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
        self.entryFirstName.connect("changed", self.name_change)
        label.set_mnemonic_widget(self.entryFirstName)
        grid.attach(self.entryFirstName, 1, 0, 2, 1)
        label = widgets.Label("_Second Name")
        grid.attach(label, 0, 1, 1, 1)
        self.entrySecondName = Gtk.Entry()
        self.entrySecondName.connect("changed", self.name_change)
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
        self.buttonDateOfBirth.connect("clicked", self.date_of_birth_change)
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
        self.checkbuttonFreeAgent.connect("toggled", self.free_agent_change)
        grid1.attach(self.checkbuttonFreeAgent, 1, 4, 1, 1)
        self.buttonClub = widgets.Button()
        self.buttonClub.set_hexpand(True)
        self.buttonClub.connect("clicked", self.club_change)
        label.set_mnemonic_widget(self.buttonClub)
        grid1.attach(self.buttonClub, 2, 4, 1, 1)

        label = widgets.Label("_Nationality")
        grid.attach(label, 0, 5, 1, 1)
        self.buttonNation = widgets.Button()
        self.buttonNation.connect("clicked", self.nation_change)
        label.set_mnemonic_widget(self.buttonNation)
        grid.attach(self.buttonNation, 1, 5, 1, 1)

        label = widgets.Label("_Position")
        grid.attach(label, 0, 6, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.connect("changed", self.position_change)
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 6, 1, 1)

        for position in data.positions:
            self.comboboxPosition.append(position, position)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 7, 6, 1)

        self.skills = []

        row = 0
        column = 0

        for item in data.skill:
            label = widgets.Label("_%s" % (item))
            grid1.attach(label, column, row, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(1, 99)
            spinbutton.set_increments(1, 10)
            label.set_mnemonic_widget(spinbutton)
            self.skills.append(spinbutton)
            grid1.attach(spinbutton, column + 1, row, 1, 1)

            row += 1

            if row in (3, 6):
                column = (column + 1) * 2
                row = 0

        label = widgets.Label("Training _Value")
        grid.attach(label, 0, 8, 1, 1)
        self.spinbuttonTraining = Gtk.SpinButton.new_with_range(1, 10, 1)
        label.set_mnemonic_widget(self.spinbuttonTraining)
        grid.attach(self.spinbuttonTraining, 1, 8, 1, 1)

        self.clubselectiondialog = dialogs.ClubSelectionDialog(parent=self)
        self.nationselectiondialog = dialogs.NationSelectionDialog(parent=self)
        self.dob = dialogs.DateOfBirth(parent=self)

    def name_change(self, entry):
        self.save_button_handler()

    def date_of_birth_change(self, button):
        state = self.dob.display(date=self.date)

        if state:
            if self.dob.date_of_birth:
                year, month, day = self.dob.date_of_birth

                if month < 10:
                    month = "0%i" % (month)
                else:
                    month = str(month)

                if day < 10:
                    day = "0%i" % (day)
                else:
                    day = str(day)

                date = "%i-%s-%s" % (year, month, day)
                self.buttonDateOfBirth.set_label("%s" % (date))

                year, month, day = self.dob.date_of_birth
                age = data.season - year

                if (month, day) > (8, 1):
                    age -= 1

                self.labelAge.set_label("Age: %i" % (age))

        self.date = None

        self.save_button_handler()

    def free_agent_change(self, checkbutton):
        if checkbutton.get_active():
            self.buttonClub.set_sensitive(False)
            self.buttonClub.set_label("")
        else:
            self.buttonClub.set_sensitive(True)

        self.save_button_handler()

    def club_change(self, button):
        if self.current:
            clubid = data.players[self.current].club

            if self.selected_club != clubid:
                clubid = self.selected_club
        else:
            clubid = None

        clubid = self.clubselectiondialog.display(clubid=clubid)

        if clubid:
            self.selected_club = clubid
            self.buttonClub.set_label("%s" % (data.clubs[clubid].name))
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

        self.save_button_handler()

    def nation_change(self, button):
        if self.selected_nation != 0:
            nationid = self.selected_nation
        else:
            nationid = None

        nationid = self.nationselectiondialog.display(nationid=nationid)

        if nationid:
            self.selected_nation = nationid
            self.buttonNation.set_label("%s" % (data.nations[nationid].name))
        else:
            self.selected_nation = 0
            self.buttonNation.set_label("")

        self.save_button_handler()

    def position_change(self, combobox):
        self.save_button_handler()

    def save_button_handler(self):
        sensitive = False

        if self.entryFirstName.get_text_length() > 0 and self.entrySecondName.get_text_length() > 0:
            sensitive = True

        if sensitive:
            if self.dob.date_of_birth is not None:
                sensitive = True
            else:
                sensitive = False

        if sensitive:
            if self.selected_nation != 0:
                sensitive = True
            else:
                sensitive = False

        if sensitive:
            if self.comboboxPosition.get_active_id() is not None:
                sensitive = True
            else:
                sensitive = False

        self.buttonSave.set_sensitive(sensitive)

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
                self.load_fields(playerid=self.current)
            except StopIteration:
                self.hide()

        if self.checkbuttonMulti.get_visible():
            if not self.checkbuttonMulti.get_active():
                self.hide()

    def save_data(self, playerid):
        if not playerid:
            data.idnumbers.playerid += 1

            player = data.Player()
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

        year, month, day = self.dob.date_of_birth

        if month < 10:
            month = "0%i" % (month)
        else:
            month = str(month)

        if day < 10:
            day = "0%i" % (day)
        else:
            day = str(day)

        player.date_of_birth = ("%i-%s-%s" % (year, month, day))

        player.position = self.comboboxPosition.get_active_id()
        player.keeping = self.skills[0].get_value_as_int()
        player.tackling = self.skills[1].get_value_as_int()
        player.passing = self.skills[2].get_value_as_int()
        player.shooting = self.skills[3].get_value_as_int()
        player.heading = self.skills[4].get_value_as_int()
        player.pace = self.skills[5].get_value_as_int()
        player.stamina = self.skills[6].get_value_as_int()
        player.ball_control = self.skills[7].get_value_as_int()
        player.set_pieces = self.skills[8].get_value_as_int()
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
            self.checkbuttonFreeAgent.set_active(True)

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
        self.date = list(map(int, player.date_of_birth.split("-")))

        if player.club != 0:
            self.selected_club = player.club
            self.buttonClub.set_label("%s" % (data.clubs[player.club].name))
            self.checkbuttonFreeAgent.set_active(False)
        else:
            self.selected_club = 0
            self.buttonClub.set_label("")
            self.checkbuttonFreeAgent.set_active(True)

        self.selected_nation = player.nationality
        nation = display.nation(player)
        self.buttonNation.set_label("%s" % (nation))

        age = display.age(player.date_of_birth)
        self.labelAge.set_label("Age: %i" % (age))

        self.comboboxPosition.set_active_id(player.position)
        self.skills[0].set_value(player.keeping)
        self.skills[1].set_value(player.tackling)
        self.skills[2].set_value(player.passing)
        self.skills[3].set_value(player.shooting)
        self.skills[4].set_value(player.heading)
        self.skills[5].set_value(player.pace)
        self.skills[6].set_value(player.stamina)
        self.skills[7].set_value(player.ball_control)
        self.skills[8].set_value(player.set_pieces)
        self.spinbuttonTraining.set_value(player.training_value)

        self.buttonSave.set_sensitive(True)

    def clear_fields(self):
        self.entryFirstName.set_text("")
        self.entrySecondName.set_text("")
        self.entryCommonName.set_text("")
        self.buttonDateOfBirth.set_label("")
        self.labelAge.set_label("")
        self.buttonClub.set_label("")
        self.buttonNation.set_label("")

        self.comboboxPosition.set_active(-1)

        for count in range(0, 9):
            self.skills[count].set_value(1)

        self.spinbuttonTraining.set_value(1)
