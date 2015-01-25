#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import display
import widgets


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
        treeview.connect("key-press-event", self.row_delete)
        treeview.connect("row-activated", self.row_activated)
        self.treeselection = treeview.get_selection()
        self.treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = widgets.TreeViewColumn(title="First Name", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Second Name", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Common Name", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Date of Birth", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nation", column=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=7)
        treeview.append_column(treeviewcolumn)

        for count, item in enumerate(data.skill, start=8):
            label = Gtk.Label(data.skill_short[count - 8])
            label.set_tooltip_text(item)
            label.show()
            treeviewcolumn = widgets.TreeViewColumn(title="", column=count)
            treeviewcolumn.set_widget(label)
            treeview.append_column(treeviewcolumn)

        treeviewcolumn = widgets.TreeViewColumn(title="Training", column=17)
        treeview.append_column(treeviewcolumn)

        self.labelCount = widgets.Label()
        self.attach(self.labelCount, 0, 1, 1, 1)

        self.labelSelected = widgets.Label()
        self.labelSelected.set_hexpand(True)
        self.attach(self.labelSelected, 1, 1, 1, 1)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        playerid = model[path][0]

        playerid = [playerid]
        dialogs.players.display(playerid)

        if dialogs.players.state:
            self.populate()

    def row_delete(self, treeview, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if dialogs.remove_dialog(index=0, parent=widgets.window):
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

            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None
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

    def run(self):
        self.show_all()
