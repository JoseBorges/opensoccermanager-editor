#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import widgets


class Stadium:
    pass


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

        self.labelCount = Gtk.Label()
        self.labelCount.set_alignment(0, 0.5)
        self.attach(self.labelCount, 0, 1, 1, 1)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        stadiumid = model[path][0]

        dialogs.stadiums.display(stadiumid)

        if dialogs.stadiums.state:
            self.populate()

    def row_delete(self, treeview, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if dialogs.remove_dialog(index=3, parent=widgets.window):
                model, treeiter = self.treeselection.get_selected()
                stadiumid = model[treeiter][0]

                keys = [club.stadium for clubid, club in data.clubs.items()]

                if stadiumid in keys:
                    dialogs.error(2)
                else:
                    del(data.stadiums[stadiums.selected])

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

        for count, (stadiumid, stadium) in enumerate(data.stadiums.items(), start=1):
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

        self.labelCount.set_label("%i Stadiums in Database" % (count))

    def run(self):
        self.show_all()


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

        for count, widget in enumerate(self.buildings):
            widget.set_value(stadium.buildings[count])

    def clear_fields(self):
        self.entryName.set_text("")

        for count, widget in enumerate(self.capacities):
            widget.set_value(0)
