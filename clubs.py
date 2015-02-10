#!/usrsel/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import display
import widgets


class Club:
    pass


class Clubs(Gtk.Grid):
    selected = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 2, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str, str, int)
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
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewcolumn.set_sort_column_id(1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Nickname", cellrenderertext, text=2)
        treeviewcolumn.set_sort_column_id(2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Manager", cellrenderertext, text=3)
        treeviewcolumn.set_sort_column_id(3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Chairman", cellrenderertext, text=4)
        treeviewcolumn.set_sort_column_id(4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Stadium", cellrenderertext, text=5)
        treeviewcolumn.set_sort_column_id(5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Reputation", cellrenderertext, text=6)
        treeviewcolumn.set_sort_column_id(6)
        treeview.append_column(treeviewcolumn)

        self.labelCount = Gtk.Label()
        self.labelCount.set_alignment(0, 0.5)
        self.attach(self.labelCount, 0, 1, 1, 1)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        clubid = model[path][0]

        dialogs.clubs.display(clubid)

        if dialogs.clubs.state:
            self.populate()

    def row_delete(self, treeview, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if dialogs.remove_dialog(index=1, parent=widgets.window):
                model, treeiter = self.treeselection.get_selected()
                clubid = model[treeiter][0]

                keys = [player.club for playerid, player in data.players.items()]

                if clubid in keys:
                    dialogs.error(0)
                else:
                    del(data.clubs[clubid])

                    self.populate()

    def selection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

    def populate(self):
        self.liststore.clear()

        count = 0

        for count, (clubid, club) in enumerate(data.clubs.items(), start=1):
            stadium = "%s" % (data.stadiums[club.stadium].name)

            self.liststore.append([clubid,
                                   club.name,
                                   club.nickname,
                                   club.manager,
                                   club.chairman,
                                   stadium,
                                   club.reputation])

        self.labelCount.set_label("%i Clubs in Database" % (count))

    def run(self):
        self.show_all()


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
        treemodelsort = Gtk.TreeModelSort(self.liststoreStadiums)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = widgets.Label("_Stadium")
        grid1.attach(label, 0, 4, 1, 1)
        self.comboboxStadium = Gtk.ComboBox()
        self.comboboxStadium.set_model(treemodelsort)
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

        self.playerselectiondialog = dialogs.PlayerSelectionDialog()

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
