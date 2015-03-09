#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import menu
import widgets


class Stadiums(Gtk.Grid):
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

        self.liststore = Gtk.ListStore(int, str, int, int, int, int,
                                       int, int, int, int, int)
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

        treeviewcolumn = Gtk.TreeViewColumn("Name",
                                            cellrenderertext,
                                            text=1)
        treeviewcolumn.set_sort_column_id(1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Capacity",
                                            cellrenderertext,
                                            text=2)
        treeviewcolumn.set_sort_column_id(2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North",
                                            cellrenderertext,
                                            text=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("West",
                                            cellrenderertext,
                                            text=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South",
                                            cellrenderertext,
                                            text=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("East",
                                            cellrenderertext,
                                            text=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North West",
                                            cellrenderertext,
                                            text=7)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("North East",
                                            cellrenderertext,
                                            text=8)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South West",
                                            cellrenderertext,
                                            text=9)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("South East",
                                            cellrenderertext,
                                            text=10)
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
        stadiumid = model[path][0]

        stadiumid = [stadiumid]
        dialogs.stadiums.display(stadiumid)

        if dialogs.stadiums.state:
            self.populate()

    def row_edit_by_menu(self, menuitem):
        model, treepath = self.treeselection.get_selected_rows()

        if treepath:
            stadiumid = model[treepath][0]

            stadiumid = [stadiumid]
            dialogs.stadiums.display(stadiumid)

            if dialogs.stadiums.state:
                self.populate()

    def row_delete(self, treeview, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=3)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                stadiumid = [model[treepath][0] for treepath in treepath]

                keys = [club.stadium for club in data.clubs.values()]

                if [item for item in stadiumid if item in keys]:
                    dialogs.error(2)
                else:
                    for item in stadium:
                        del(data.stadiums[item])

                    data.unsaved = True

                    self.populate()

    def selection_changed(self, treeselection):
        model, treepath = treeselection.get_selected_rows()

        if treepath:
            self.selected = [model[item][0] for item in treepath]

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

        if items is None:
            items = data.stadiums
            dbcount = True
        else:
            dbcount = False

        count = 0

        for count, (stadiumid, stadium) in enumerate(items.items(), start=1):
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

        if dbcount:
            self.labelCount.set_label("%i Stadiums in Database" % (count))

    def run(self):
        self.show_all()


class AddStadiumDialog(Gtk.Dialog):
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

        grid1 = Gtk.Grid()
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 0, 3, 1)

        label = widgets.Label("_Name")
        grid1.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        self.entryName.connect("changed", lambda w: self.save_button_handler())
        label.set_mnemonic_widget(self.entryName)
        grid1.attach(self.entryName, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        grid.attach(notebook, 0, 1, 3, 1)

        grid1 = Gtk.Grid()
        grid1.set_border_width(5)
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        label = widgets.Label("_Stands")
        notebook.append_page(grid1, label)

        self.capacities = []
        self.seating = []
        self.roofs = []
        self.boxes = []

        for count, stand in enumerate(("North", "East", "South", "West", "North East", "North West", "South East", "South West")):
            label = widgets.Label("_%s" % (stand))
            grid1.attach(label, 0, count, 1, 1)

            spinbuttonCapacity = Gtk.SpinButton()
            spinbuttonCapacity.set_value(0)
            spinbuttonCapacity.set_increments(1000, 1000)
            spinbuttonCapacity.set_snap_to_ticks(True)
            label.set_mnemonic_widget(spinbuttonCapacity)
            self.capacities.append(spinbuttonCapacity)
            grid1.attach(spinbuttonCapacity, 1, count, 1, 1)

            radiobuttonStanding = Gtk.RadioButton("_Standing")
            radiobuttonStanding.set_use_underline(True)
            grid1.attach(radiobuttonStanding, 2, count, 1, 1)
            radiobuttonSeating = Gtk.RadioButton("_Seating")
            radiobuttonSeating.set_use_underline(True)
            radiobuttonSeating.join_group(radiobuttonStanding)
            self.seating.append([radiobuttonStanding, radiobuttonSeating])
            grid1.attach(radiobuttonSeating, 3, count, 1, 1)

            checkbuttonRoof = Gtk.CheckButton("_Roof")
            checkbuttonRoof.set_use_underline(True)
            self.roofs.append(checkbuttonRoof)
            grid1.attach(checkbuttonRoof, 4, count, 1, 1)

            if count < 4:
                spinbuttonCapacity.set_range(0, 15000)

                label = widgets.Label("_Box")
                grid1.attach(label, 5, count, 1, 1)

                spinbuttonBox = Gtk.SpinButton()
                spinbuttonBox.set_value(0)
                spinbuttonBox.set_range(0, 500)
                spinbuttonBox.set_increments(250, 250)
                spinbuttonBox.set_snap_to_ticks(True)
                label.set_mnemonic_widget(spinbuttonBox)
                self.boxes.append(spinbuttonBox)
                grid1.attach(spinbuttonBox, 6, count, 1, 1)
            else:
                spinbuttonCapacity.set_range(0, 3000)

        grid2 = Gtk.Grid()
        grid2.set_border_width(5)
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        label = widgets.Label("_Buildings")
        notebook.append_page(grid2, label)

        self.buildings = []

        for count, building in enumerate(("Stall", "Programme Vendor", "Small Shop", "Large Shop", "Bar", "Burger Bar", "Cafe", "Restaurant")):
            label = widgets.Label("_%s" % (building))
            grid2.attach(label, 0, count, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_value(0)
            spinbutton.set_range(0, 8)
            spinbutton.set_increments(1, 1)
            label.set_mnemonic_widget(spinbutton)
            self.buildings.append(spinbutton)
            grid2.attach(spinbutton, 1, count, 1, 1)

    def display(self, stadiumid=None):
        self.show_all()

        if not stadiumid:
            self.set_title("Add Stadium")
            self.buttonSave.set_label("_Add")
            self.buttonSave.set_sensitive(False)

            self.current = None
        else:
            self.set_title("Edit Stadium")
            self.buttonSave.set_label("_Edit")

            self.checkbuttonMulti.set_visible(False)

            self.generator = stadiumid.__iter__()
            self.current = self.generator.__next__()

            self.load_fields(stadiumid=self.current)

        self.run()

    def response_handler(self, dialog, response):
        self.clear_fields()

        self.hide()

    def save_handler(self, button):
        self.save_data(stadiumid=self.current)
        self.clear_fields()

        self.state = True

        if self.current:
            try:
                self.current = self.generator.__next__()
                self.load_fields(stadiumid=self.current)
            except StopIteration:
                self.hide()

        if self.checkbuttonMulti.get_visible():
            if not self.checkbuttonMulti.get_active():
                self.hide()

    def save_data(self, stadiumid):
        if not stadiumid:
            data.idnumbers.stadiumid += 1

            stadium = data.Stadium()
            data.stadiums[data.idnumbers.stadiumid] = stadium
        else:
            stadium = data.stadiums[stadiumid]

        stadium.name = self.entryName.get_text()

        capacity = 0

        for spinbutton in self.capacities:
            capacity += spinbutton.get_value_as_int()

        for spinbutton in self.boxes:
            capacity += spinbutton.get_value_as_int()

        stadium.capacity = capacity
        stadium.stands = [widget.get_value_as_int() for widget in self.capacities]

        stadium.seating = []

        for widget in self.seating:
            if widget[0].get_active():
                stadium.seating.append(False)
            else:
                stadium.seating.append(True)

        stadium.roof = [widget.get_active() for widget in self.roofs]
        stadium.box = [widget.get_value_as_int() for widget in self.boxes]
        stadium.buildings = [widget.get_value_as_int() for widget in self.buildings]

    def load_fields(self, stadiumid):
        stadium = data.stadiums[stadiumid]

        self.entryName.set_text(stadium.name)

        for count, widget in enumerate(self.capacities):
            widget.set_value(stadium.stands[count])

        for count, widget in enumerate(self.boxes):
            widget.set_value(stadium.box[count])

        for count, widget in enumerate(self.seating):
            if stadium.seating[count]:
                widget[1].set_active(True)
            else:
                widget[0].set_active(True)

        for count, widget in enumerate(self.roofs):
            widget.set_active(stadium.roof[count])

        for count, widget in enumerate(self.buildings):
            widget.set_value(stadium.buildings[count])

    def clear_fields(self):
        self.entryName.set_text("")

        for widget in self.capacities:
            widget.set_value(0)

        for widget in self.boxes:
            widget.set_value(0)

        for widget in self.seating:
            widget[0].set_active(True)

        for widget in self.roofs:
            widget.set_active(False)

        for widget in self.buildings:
            widget.set_value(0)

    def save_button_handler(self):
        if self.entryName.get_text_length() > 0:
            sensitive = True
        else:
            sensitive = False

        self.buttonSave.set_sensitive(sensitive)
