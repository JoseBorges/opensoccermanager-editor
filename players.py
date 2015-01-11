#!/usr/bin/env python

from gi.repository import Gtk

import widgets
import database
import data
import dialogs


class Players(Gtk.Grid):
    selected = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str, str,
                                       str, str, int, int, int, int,
                                       int, int, int, int, int, int)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.connect("row-activated", self.row_activated)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("First Name", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Second Name", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Common Name", cellrenderertext, text=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Date of Birth", cellrenderertext, text=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Nation", cellrenderertext, text=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=7)
        treeview.append_column(treeviewcolumn)

        for count, item in enumerate(data.skill, start=8):
            label = Gtk.Label(data.skill_short[count - 8])
            label.set_tooltip_text(item)
            label.show()
            treeviewcolumn = Gtk.TreeViewColumn()
            treeviewcolumn.set_widget(label)
            treeviewcolumn.pack_start(cellrenderertext, True)
            treeviewcolumn.add_attribute(cellrenderertext, "text", count)
            treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Training", cellrenderertext, text=17)
        treeview.append_column(treeviewcolumn)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        playerid = model[path][0]

        widgets.players_dialog.display(playerid)

        if widgets.players_dialog.state:
            self.populate()

    def selection_changed(self, treeselection):
        model, treeiter = self.treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = 0
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

    def populate(self):
        self.liststore.clear()

        for playerid, player in data.players.items():
            club = data.clubs[player.club].name
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
        self.selection_changed(self.treeselection)

        self.show_all()
