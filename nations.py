#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import widgets


class Nation:
    pass


class Nations(Gtk.Grid):
    selected = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str)
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
        treeviewcolumn = Gtk.TreeViewColumn("Denonym", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)

        self.labelCount = Gtk.Label()
        self.labelCount.set_alignment(0, 0.5)
        self.attach(self.labelCount, 0, 1, 1, 1)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        nationid = model[path][0]

        dialogs.nations.display(nationid)

        if dialogs.nations.state:
            self.populate()

    def row_delete(self, treeview, event):
        key = Gdk.keyval_name(event.keyval)

        if key == "Delete":
            if dialogs.remove_dialog(index=2, parent=widgets.window):
                model, treeiter = self.treeselection.get_selected()
                nationid = model[treeiter][0]

                keys = [player.nationality for playerid, player in data.players.items()]

                if nationid in keys:
                    dialogs.error(1)
                else:
                    del(data.nations[nationid])

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

        for count, (nationid, nation) in enumerate(data.nations.items(), start=1):
            self.liststore.append([nationid,
                                   nation.name,
                                   nation.denonym])

        self.labelCount.set_label("%i Nations in Database" % (count))

    def run(self):
        self.show_all()


class AddNationDialog(Gtk.Dialog):
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

        label = widgets.Label("_Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        label.set_mnemonic_widget(self.entryName)
        grid.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Denonym")
        grid.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        label.set_mnemonic_widget(self.entryDenonym)
        grid.attach(self.entryDenonym, 1, 1, 1, 1)

    def save_handler(self, button):
        self.save_data(nationid=self.current)
        self.clear_fields()

        self.state = True

        self.hide()

    def save_data(self, nationid):
        if nationid is None:
            data.idnumbers.nationid += 1

            nation = Nation()
            data.nations[data.idnumbers.nationid] = nation
        else:
            nation = data.nations[nationid]

        nation.name = self.entryName.get_text()
        nation.denonym = self.entryDenonym.get_text()

    def response_handler(self, dialog, response):
        self.hide()

    def display(self, nationid=None):
        if nationid is None:
            self.set_title("Add Nation")
            self.buttonSave.set_label("_Add")

            self.current = None
        else:
            self.set_title("Edit Nation")
            self.buttonSave.set_label("_Edit")
            self.buttonSave.set_sensitive(True)

            self.load_fields(nationid)

            self.current = nationid

        self.show_all()
        self.run()

    def load_fields(self, nationid):
        nation = data.nations[nationid]

        self.entryName.set_text(nation.name)
        self.entryDenonym.set_text(nation.denonym)

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryDenonym.set_text("")
