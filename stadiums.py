#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import widgets


class Stadiums(Gtk.Grid):
    selected = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, int, int, int, int, int, int, int, int, int)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.connect("key-press-event", self.row_delete)
        treeview.connect("row-activated", self.row_activated)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Capacity", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North", cellrenderertext, text=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("West", cellrenderertext, text=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South", cellrenderertext, text=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("East", cellrenderertext, text=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North West", cellrenderertext, text=7)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North East", cellrenderertext, text=8)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South West", cellrenderertext, text=9)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South East", cellrenderertext, text=10)
        treeview.append_column(treeviewcolumn)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        stadiumid = model[path][0]

        state = dialogs.add_stadium_dialog(stadiumid)

        if state:
            self.populate()

    def row_delete(self, treeview, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if dialogs.remove_dialog(3):
                model, treeiter = self.treeselection.get_selected()
                stadiumid = model[treeiter][0]
                del(data.stadiums[stadiumid])

                self.populate()

    def selection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

    def populate(self):
        self.liststore.clear()

        for stadiumid, stadium in data.stadiums.items():
            self.liststore.append([stadiumid,
                                   stadium.name,
                                   stadium.capacity,
                                   stadium.stands[0],
                                   stadium.stands[1],
                                   stadium.stands[2],
                                   stadium.stands[3],
                                   stadium.stands[4],
                                   stadium.stands[5],
                                   stadium.stands[6],
                                   stadium.stands[7],
                                   ])

    def run(self):
        self.show_all()
