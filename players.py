#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import re
import unicodedata

import calculator
import data
import dialogs
import display
import interface
import menu
import widgets


class Players(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.search.searchentry.connect("activate", self.search_activated)
        self.search.searchentry.connect("changed", self.search_changed)
        self.search.searchentry.connect("icon-press", self.search_cleared)
        self.search.treeview.connect("row-activated", self.player_activated)
        self.search.treeselection.connect("changed", self.player_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attach(self.attributes, 1, 0, 1, 1)

    def add_player(self):
        player = data.Player()
        data.players[999] = player

        self.populate_data(values=data.players)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if criteria is not "":
            values = {}

            for playerid, player in data.players.items():
                both = "%s %s" % (player.first_name, player.second_name)

                for search in (player.second_name, player.first_name, player.common_name, both):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[playerid] = player

                        break

            self.populate_data(values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data(data.players)

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(data.players)

    def player_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()
        self.playerid = model[treepath][0]

        player = data.players[self.playerid]
        self.attributes.playerid = self.playerid

        self.attributes.entryFirstName.set_text(player.first_name)
        self.attributes.entrySecondName.set_text(player.second_name)
        self.attributes.entryCommonName.set_text(player.common_name)

        self.date_of_birth = player.date_of_birth

        if self.date_of_birth:
            self.attributes.buttonDateOfBirth.set_label(self.date_of_birth)

        self.nationid = player.nationality

        if self.nationid:
            nationality = data.nations[self.nationid].name
            self.attributes.buttonNationality.set_label(nationality)

        self.attributes.populate_attributes()

    def player_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            widgets.toolbuttonRemove.set_sensitive(True)
            self.attributes.set_sensitive(True)
        else:
            self.selected = None
            widgets.toolbuttonRemove.set_sensitive(False)
            self.attributes.clear_fields()
            self.attributes.set_sensitive(False)

        print(self.selected)

    def populate_data(self, values):
        self.search.clear_data()

        for playerid, player in values.items():
            name = display.name(player)

            self.search.liststore.append([playerid, name])

    def run(self):
        self.populate_data(values=data.players)
        self.show_all()

        treepath = Gtk.TreePath.new_first()
        self.search.treeselection.select_path(treepath)
        column = self.search.treeviewcolumn

        if self.search.treeselection.path_is_selected(treepath):
            self.search.treeview.row_activated(treepath, column)


class Attributes(Gtk.Grid):
    def __init__(self):
        self.playerid = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_sensitive(False)

        commonframe = widgets.CommonFrame("Personal")
        self.attach(commonframe, 1, 0, 1, 1)

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        commonframe.insert(grid2)

        label = widgets.Label("First Name")
        grid2.attach(label, 0, 0, 1, 1)
        self.entryFirstName = Gtk.Entry()
        grid2.attach(self.entryFirstName, 1, 0, 1, 1)

        label = widgets.Label("Second Name")
        grid2.attach(label, 0, 1, 1, 1)
        self.entrySecondName = Gtk.Entry()
        grid2.attach(self.entrySecondName, 1, 1, 1, 1)

        label = widgets.Label("Common Name")
        grid2.attach(label, 0, 2, 1, 1)
        self.entryCommonName = Gtk.Entry()
        grid2.attach(self.entryCommonName, 1, 2, 1, 1)

        label = widgets.Label("Date Of Birth")
        grid2.attach(label, 0, 3, 1, 1)
        self.buttonDateOfBirth = Gtk.Button("")
        self.buttonDateOfBirth.connect("clicked", self.date_of_birth_clicked)
        grid2.attach(self.buttonDateOfBirth, 1, 3, 1, 1)

        label = widgets.Label("Nationality")
        grid2.attach(label, 0, 4, 1, 1)
        self.buttonNationality = Gtk.Button("")
        self.buttonNationality.connect("clicked", self.nation_clicked)
        grid2.attach(self.buttonNationality, 1, 4, 1, 1)

        commonframe = widgets.CommonFrame("Attributes")
        self.attach(commonframe, 1, 1, 1, 1)

        grid3 = Gtk.Grid()
        grid3.set_row_spacing(5)
        grid3.set_column_spacing(5)
        commonframe.insert(grid3)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 120)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        grid3.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreAttributes = Gtk.ListStore(int, int, str, str, int, int,
                                                 int, int, int, int, int, int,
                                                 int, int)
        cellrenderertext = Gtk.CellRendererText()

        self.treeview = Gtk.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.liststoreAttributes)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeview.connect("row-activated", self.attribute_activated)
        self.treeselectionAttribute = self.treeview.get_selection()
        self.treeselectionAttribute.connect("changed", self.attribute_changed)
        scrolledwindow.add(self.treeview)
        treeviewcolumn = Gtk.TreeViewColumn("Year", cellrenderertext, text=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=3)
        self.treeview.append_column(treeviewcolumn)

        for count, skill in enumerate(data.skill_short):
            label = Gtk.Label("%s" % (skill))
            label.set_tooltip_text("%s" % (data.skill[count]))
            label.show()

            cellrenderertext = Gtk.CellRendererText()

            treeviewcolumn = Gtk.TreeViewColumn()
            treeviewcolumn.set_widget(label)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", count + 4)
            self.treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Training", cellrenderertext, text=13)
        self.treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonAdd = Gtk.Button.new_from_icon_name("gtk-add", Gtk.IconSize.BUTTON)
        buttonAdd.connect("clicked", self.add_attribute)
        buttonbox.add(buttonAdd)
        self.buttonEdit = Gtk.Button.new_from_icon_name("gtk-edit", Gtk.IconSize.BUTTON)
        self.buttonEdit.set_sensitive(False)
        self.buttonEdit.connect("clicked", self.edit_attribute)
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove", Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.remove_attribute)
        buttonbox.add(self.buttonRemove)
        grid3.attach(buttonbox, 1, 0, 1, 1)

    def attribute_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonEdit.set_sensitive(True)
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonEdit.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def attribute_activated(self, treeview=None, treepath=None, treeviewcolumn=None):
        model, treeiter = self.treeselectionAttribute.get_selected()

        if treeiter:
            attributeid = model[treeiter][0]

            dialog = AttributeDialog(parent=widgets.window)
            dialog.display(playerid=self.playerid, attributeid=attributeid)

            self.populate_attributes()

    def date_of_birth_clicked(self, button):
        dialogDOB = dialogs.DateOfBirth(parent=widgets.window)

        if dialogDOB.display(self.date_of_birth):
            date = dialogDOB.date_of_birth
            self.buttonDateOfBirth.set_label(date)

            player = data.players[self.playerid]
            player.date_of_birth = date

    def nation_clicked(self, button):
        dialogNation = dialogs.NationSelectionDialog(parent=widgets.window)
        nationid = dialogNation.display(self.nationid)

        nationality = display.nation(nationid)
        self.buttonNationality.set_label(nationality)

        player = data.players[self.playerid]
        player.nationality = nationid

    def add_attribute(self, button):
        '''
        Launch dialog used to input new attribute values.
        '''
        dialog = AttributeDialog(parent=widgets.window)
        dialog.display()

    def edit_attribute(self, button):
        '''
        Run when edit button for selected attribute is clicked.
        '''
        self.attribute_activated()

    def remove_attribute(self, button):
        '''
        Delete selected attribute when delete is clicked.
        '''
        model, treeiter = self.treeselectionAttribute.get_selected()
        attributeid = model[treeiter][0]

        player = data.players[self.playerid]
        del player.attributes[attributeid]

        self.populate_attributes()

    def clear_fields(self):
        self.entryFirstName.set_text("")
        self.entrySecondName.set_text("")
        self.entryCommonName.set_text("")
        self.buttonDateOfBirth.set_label("")
        self.buttonNationality.set_label("")
        self.liststoreAttributes.clear()

    def populate_attributes(self):
        '''
        Populate attribute treeview with values for player id.
        '''
        self.liststoreAttributes.clear()

        player = data.players[self.playerid]

        for attributeid, attribute in player.attributes.items():
            club = display.club(attribute.club)

            self.liststoreAttributes.append([attributeid,
                                             attribute.year,
                                             club,
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
                                             attribute.training_value,
                                             ])

    def retrieve(self):
        first_name = self.entryFirstName.get_text()
        second_name = self.entrySecondName.get_text()
        common_name = self.entryCommonName.get_text()

        values = (first_name, second_name, common_name)

        return values


class AttributeDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)

        self.set_transient_for(parent)
        self.set_border_width(5)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        self.liststoreYear = Gtk.ListStore(str)
        cellrenderertext = Gtk.CellRendererText()

        label = widgets.Label("_Year")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBox()
        self.comboboxYear.set_model(self.liststoreYear)
        self.comboboxYear.set_id_column(0)
        self.comboboxYear.pack_start(cellrenderertext, True)
        self.comboboxYear.add_attribute(cellrenderertext, "text", 0)
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 2, 1)

        for year in data.years:
            year = str(year)
            self.liststoreYear.append([year])

        label = widgets.Label("_Club")
        grid.attach(label, 0, 1, 1, 1)
        self.buttonClub = Gtk.Button("")
        self.buttonClub.set_hexpand(True)
        self.buttonClub.connect("clicked", self.club_clicked)
        label.set_mnemonic_widget(self.buttonClub)
        grid.attach(self.buttonClub, 1, 1, 3, 1)
        self.checkbuttonFreeAgent = Gtk.CheckButton("_Free Agent")
        self.checkbuttonFreeAgent.set_use_underline(True)
        self.checkbuttonFreeAgent.connect("toggled", self.free_agent_toggled)
        grid.attach(self.checkbuttonFreeAgent, 4, 1, 1, 1)

        label = widgets.Label("Position")
        grid.attach(label, 0, 2, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 2, 1, 1)

        for position in data.positions:
            self.comboboxPosition.append(position, position)

        self.spinbuttonSkills = []

        for count, skill in enumerate(data.skill):
            label = widgets.Label("_%s" % (skill))
            grid.attach(label, 0, count + 3, 1, 1)
            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 99)
            spinbutton.set_increments(1, 10)
            label.set_mnemonic_widget(spinbutton)
            self.spinbuttonSkills.append(spinbutton)
            grid.attach(spinbutton, 1, count + 3, 1, 1)

        label = widgets.Label("_Training Value")
        grid.attach(label, 0, 12, 1, 1)
        self.spinbuttonTraining = Gtk.SpinButton()
        self.spinbuttonTraining.set_range(1, 10)
        self.spinbuttonTraining.set_increments(1, 1)
        label.set_mnemonic_widget(self.spinbuttonTraining)
        grid.attach(self.spinbuttonTraining, 1, 12, 1, 1)

    def club_clicked(self, button):
        model = self.comboboxYear.get_model()
        treeiter = self.comboboxYear.get_active()

        year = int(model[treeiter][0])

        club_dialog = dialogs.ClubSelectionDialog(parent=self)
        clubid = club_dialog.display(clubid=self.clubid, year=year)

        if clubid:
            player = data.players[self.playerid]
            attribute = player.attributes[self.attributeid]

            club = data.clubs[clubid].name
            button.set_label("%s" % (club))

            attribute.club = clubid

        club_dialog.destroy()

    def free_agent_toggled(self, checkbutton):
        if checkbutton.get_active():
            self.buttonClub.set_label("")
            self.buttonClub.set_sensitive(False)
        else:
            self.buttonClub.set_sensitive(True)

    def load_fields(self):
        player = data.players[self.playerid]
        attribute = player.attributes[self.attributeid]

        self.clubid = attribute.club

        year = str(attribute.year)
        self.comboboxYear.set_active_id(year)

        club = display.club(attribute.club)

        if attribute.club == 0:
            self.checkbuttonFreeAgent.set_active(True)
            self.buttonClub.set_label("")
            self.buttonClub.set_sensitive(False)
        else:
            self.buttonClub.set_label("%s" % (club))

        self.comboboxPosition.set_active_id(attribute.position)

        self.spinbuttonSkills[0].set_value(attribute.keeping)
        self.spinbuttonSkills[1].set_value(attribute.tackling)
        self.spinbuttonSkills[2].set_value(attribute.passing)
        self.spinbuttonSkills[3].set_value(attribute.shooting)
        self.spinbuttonSkills[4].set_value(attribute.heading)
        self.spinbuttonSkills[5].set_value(attribute.pace)
        self.spinbuttonSkills[6].set_value(attribute.stamina)
        self.spinbuttonSkills[7].set_value(attribute.ball_control)
        self.spinbuttonSkills[8].set_value(attribute.set_pieces)

        self.spinbuttonTraining.set_value(attribute.training_value)

    def save_fields(self):
        player = data.players[self.playerid]
        attribute = player.attributes[self.attributeid]

        model = self.comboboxYear.get_model()
        treeiter = self.comboboxYear.get_active()
        attribute.year = int(model[treeiter][0])

        if self.checkbuttonFreeAgent.get_active():
            attribute.club = 0

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

        attribute.training_value = self.spinbuttonTraining.get_value_as_int()

    def display(self, playerid=None, attributeid=None):
        if playerid:
            self.playerid = playerid
            self.attributeid = attributeid

            self.load_fields()

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            self.save_fields()

        self.destroy()
