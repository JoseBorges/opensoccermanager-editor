#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import menu
import widgets


class Nations(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 0, 2, 1)

        self.liststore = Gtk.ListStore(int, str, str)
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

        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewcolumn.set_sort_column_id(1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Denonym", cellrenderertext, text=2)
        treeviewcolumn.set_sort_column_id(2)
        treeview.append_column(treeviewcolumn)

        self.labelCount = Gtk.Label()
        self.labelCount.set_alignment(0, 0.5)
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
        nationid = model[path][0]

        nationid = [nationid]
        dialogs.nations.display(nationid)

        if dialogs.nations.state:
            self.populate()

    def row_edit_by_menu(self, menuitem):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            nationid = model[treepath][0]

            nationid = [nationid]
            dialogs.nations.display(nationid)

            if dialogs.nations.state:
                self.populate()

    def row_delete(self, treeview, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=2)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                nationid = [model[treepath][0] for treepath in treepath]

                keys = [player.nationality for player in data.players.values()]

                if [item for item in nationid if item in keys]:
                    dialogs.error(1)
                else:
                    for item in nationid:
                        del(data.nations[item])

                    data.unsaved = True

                    self.populate()

    def selection_changed(self, treeselection):
        model, treepath = treeselection.get_selected_rows()

        if treepath:
            self.selected = [model[treepath][0] for treepath in treepath]

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

    def populate(self, items=None):
        self.liststore.clear()

        if not items:
            items = data.nations
            dbcount = True
        else:
            dbcount = False

        count = 0

        for count, (nationid, nation) in enumerate(items.items(), start=1):
            self.liststore.append([nationid,
                                   nation.name,
                                   nation.denonym])

        if dbcount:
            self.labelCount.set_label("%i Nations in Database" % (count))

    def run(self):
        self.populate()

        self.show_all()


class AddNationDialog(Gtk.Dialog):
    def __init__(self):
        self.state = False

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

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_Name")
        grid.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        self.entryName.connect("changed", lambda w: self.save_button_handler())
        label.set_mnemonic_widget(self.entryName)
        grid.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Denonym")
        grid.attach(label, 0, 1, 1, 1)
        self.entryDenonym = Gtk.Entry()
        self.entryDenonym.connect("changed", lambda w: self.save_button_handler())
        label.set_mnemonic_widget(self.entryDenonym)
        grid.attach(self.entryDenonym, 1, 1, 1, 1)

    def display(self, nationid=None):
        self.show_all()

        self.clear_fields()

        if nationid is None:
            self.set_title("Add Nation")
            self.buttonSave.set_label("_Add")
            self.buttonSave.set_sensitive(False)

            self.current = None
        else:
            self.set_title("Edit Nation")
            self.buttonSave.set_label("_Edit")
            self.buttonSave.set_sensitive(True)

            self.checkbuttonMulti.set_visible(False)

            self.generator = nationid.__iter__()
            self.current = self.generator.__next__()

            self.load_fields(nationid=self.current)

        self.run()

    def save_handler(self, button):
        self.save_data(nationid=self.current)
        self.clear_fields()

        self.state = True

        if self.current:
            try:
                self.current = self.generator.__next__()
                self.load_fields(nationid=self.current)
            except StopIteration:
                self.hide()

        if self.checkbuttonMulti.get_visible():
            if not self.checkbuttonMulti.get_active():
                self.hide()

    def save_data(self, nationid):
        if nationid is None:
            data.idnumbers.nationid += 1

            nation = data.Nation()
            data.nations[data.idnumbers.nationid] = nation
        else:
            nation = data.nations[nationid]

        nation.name = self.entryName.get_text()
        nation.denonym = self.entryDenonym.get_text()

    def save_button_handler(self):
        sensitive = False

        if self.entryName.get_text_length() > 0:
            sensitive = True

        if sensitive:
            if self.entryDenonym.get_text_length() > 0:
                sensitive = True
            else:
                sensitive = False

        self.buttonSave.set_sensitive(sensitive)

    def response_handler(self, dialog, response):
        self.hide()

    def load_fields(self, nationid):
        nation = data.nations[nationid]

        self.entryName.set_text(nation.name)
        self.entryDenonym.set_text(nation.denonym)

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryDenonym.set_text("")
