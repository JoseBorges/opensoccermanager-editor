#!/usrsel/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager-Editor is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager-Editor is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager-Editor.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk
from gi.repository import Gdk
import re
import unicodedata

import data
import dialogs
import display
import interface
import menu
import widgets


class Clubs(Gtk.Grid):
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
        self.search.treeview.connect("row-activated", self.club_activated)
        self.search.treeselection.connect("changed", self.club_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attributes.entryName.connect("focus-out-event", self.name_changed)
        self.attach(self.attributes, 1, 0, 1, 1)

    def add_club(self):
        '''
        Add the club to the data structure, and append to search interface.
        '''
        club = data.Club()
        clubid = data.idnumbers.request_clubid()
        data.clubs[clubid] = club

        child_treeiter = self.search.liststore.append([clubid, ""])
        treeiter = self.search.treemodelsort.convert_child_iter_to_iter(child_treeiter)
        treepath = self.search.treemodelsort.get_path(treeiter[1])

        self.search.treeview.scroll_to_cell(treepath)
        self.search.treeview.set_cursor_on_cell(treepath, None, None, False)

        self.attributes.clear_fields()
        self.attributes.entryName.grab_focus()

    def name_changed(self, entry, event):
        '''
        Update list with new name of club.
        '''
        name = entry.get_text()

        model, treeiter = self.search.treeselection.get_selected()
        liststore = model.get_model()
        child_treeiter = model.convert_iter_to_child_iter(treeiter)

        liststore[child_treeiter][1] = name
        data.clubs[self.selected].name = name

        # Get new position of modified item
        model, treeiter = self.search.treeselection.get_selected()
        treepath = model.get_path(treeiter)
        self.search.treeview.scroll_to_cell(treepath)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if criteria is not "":
            values = {}

            for clubid, club in data.clubs.items():
                for search in (club.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[clubid] = club

                        break

            self.populate_data(values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data(data.clubs)

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(data.clubs)

    def club_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()
        self.clubid = model[treepath][0]

        club = data.clubs[self.clubid]
        self.attributes.clubid = self.clubid

        self.attributes.entryName.set_text(club.name)
        self.attributes.entryNickname.set_text(club.nickname)

        self.attributes.populate_attributes()

    def club_changed(self, treeselection):
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

    def populate_data(self, values):
        self.search.clear_data()

        for clubid, club in values.items():
            self.search.liststore.append([clubid, club.name])

    def run(self):
        self.populate_data(values=data.clubs)
        self.show_all()

        treepath = Gtk.TreePath.new_first()
        self.search.treeselection.select_path(treepath)
        column = self.search.treeviewcolumn

        if self.search.treeselection.path_is_selected(treepath):
            self.search.treeview.row_activated(treepath, column)


class Attributes(Gtk.Grid):
    def __init__(self):
        self.clubid = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_sensitive(False)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        grid.attach(grid1, 0, 0, 1, 1)

        label = widgets.Label("_Name")
        grid1.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        grid1.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("_Nickname")
        grid1.attach(label, 0, 1, 1, 1)
        self.entryNickname = Gtk.Entry()
        grid1.attach(self.entryNickname, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Attributes")
        grid.attach(commonframe, 0, 1, 1, 1)

        self.liststoreAttributes = Gtk.ListStore(int, int, str, str, str, int)
        cellrenderertext = Gtk.CellRendererText()

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        commonframe.insert(grid2)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 120)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        grid2.attach(scrolledwindow, 0, 0, 1, 1)

        self.treeview = Gtk.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.liststoreAttributes)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeview.connect("row-activated", self.attribute_activated)
        self.treeselectionAttribute = self.treeview.get_selection()
        self.treeselectionAttribute.connect("changed", self.attribute_changed)
        scrolledwindow.add(self.treeview)
        treeviewcolumn = widgets.TreeViewColumn("Year", column=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Manager", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Chairman", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Stadium", column=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Reputation", column=5)
        self.treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonAdd = Gtk.Button.new_from_icon_name("gtk-add",
                                                  Gtk.IconSize.BUTTON)
        buttonAdd.connect("clicked", self.add_attribute)
        buttonbox.add(buttonAdd)
        self.buttonEdit = Gtk.Button.new_from_icon_name("gtk-edit",
                                                        Gtk.IconSize.BUTTON)
        self.buttonEdit.set_sensitive(False)
        self.buttonEdit.connect("clicked", self.edit_attribute)
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove",
                                                          Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.remove_attribute)
        buttonbox.add(self.buttonRemove)
        grid2.attach(buttonbox, 1, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 1, 1, 1)
        self.buttonReset = widgets.Button("_Reset")
        buttonbox.add(self.buttonReset)
        self.buttonSave = widgets.Button("_Save")
        buttonbox.add(self.buttonSave)

    def add_attribute(self, button):
        '''
        Launch dialog used to input new attribute values.
        '''
        dialog = AttributeDialog(parent=widgets.window)
        dialog.clubid = self.clubid
        dialog.stadiumid = None
        dialog.year = None
        dialog.display()

        self.populate_attributes()

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

        if dialogs.remove_dialog(index=4):
            attributeid = model[treeiter][0]
            club = data.clubs[self.clubid]
            del club.attributes[attributeid]

            self.populate_attributes()

    def attribute_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonEdit.set_sensitive(True)
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonEdit.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def attribute_activated(self, widget=None, treepath=None, treeviewcolumn=None):
        model, treeiter = self.treeselectionAttribute.get_selected()

        if treeiter:
            attributeid = model[treeiter][0]

            dialog = AttributeDialog(parent=widgets.window)
            dialog.display(clubid=self.clubid, attributeid=attributeid)

            self.populate_attributes()

    def clear_fields(self):
        self.entryName.set_text("")
        self.entryNickname.set_text("")
        self.liststoreAttributes.clear()

    def populate_attributes(self):
        '''
        Populate attribute treeview with values for player id.
        '''
        self.liststoreAttributes.clear()

        club = data.clubs[self.clubid]

        for attributeid, attribute in club.attributes.items():
            stadium = data.stadiums[attribute.stadium].name

            self.liststoreAttributes.append([attributeid,
                                             attribute.year,
                                             attribute.manager,
                                             attribute.chairman,
                                             stadium,
                                             attribute.reputation
                                             ])


class AttributeDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(parent)
        self.set_border_width(5)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        self.liststoreYear = Gtk.ListStore(str)

        for year in data.years:
            year = str(year)
            self.liststoreYear.append([year])

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.Label("_Year")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxYear = Gtk.ComboBox()
        self.comboboxYear.set_model(self.liststoreYear)
        self.comboboxYear.set_id_column(0)
        self.comboboxYear.set_active(0)
        self.comboboxYear.pack_start(cellrenderertext, True)
        self.comboboxYear.add_attribute(cellrenderertext, "text", 0)
        label.set_mnemonic_widget(self.comboboxYear)
        grid.attach(self.comboboxYear, 1, 0, 1, 1)

        label = widgets.Label("_Manager")
        grid.attach(label, 0, 1, 1, 1)
        self.entryManager = Gtk.Entry()
        label.set_mnemonic_widget(self.entryManager)
        grid.attach(self.entryManager, 1, 1, 2, 1)

        label = widgets.Label("_Chairman")
        grid.attach(label, 0, 2, 1, 1)
        self.entryChairman = Gtk.Entry()
        label.set_mnemonic_widget(self.entryChairman)
        grid.attach(self.entryChairman, 1, 2, 2, 1)

        label = widgets.Label("_Stadium")
        grid.attach(label, 0, 3, 1, 1)
        self.buttonStadium = Gtk.Button("")
        self.buttonStadium.connect("clicked", self.stadium_clicked)
        label.set_mnemonic_widget(self.buttonStadium)
        grid.attach(self.buttonStadium, 1, 3, 2, 1)

        label = widgets.Label("_Reputation")
        grid.attach(label, 0, 4, 1, 1)
        self.spinbuttonReputation = Gtk.SpinButton.new_with_range(1, 20, 1)
        label.set_mnemonic_widget(self.spinbuttonReputation)
        grid.attach(self.spinbuttonReputation, 1, 4, 1, 1)

    def stadium_clicked(self, button):
        model = self.comboboxYear.get_model()
        treeiter = self.comboboxYear.get_active()

        year = int(model[treeiter][0])

        dialog = dialogs.StadiumSelectionDialog()
        dialog.set_transient_for(widgets.window)
        stadiumid = dialog.display(stadiumid=self.stadiumid, year=self.year)

        if stadiumid:
            club = data.clubs[self.clubid]
            self.attributeid = data.idnumbers.request_clubattrid()
            club.attributes[self.attributeid] = data.Attributes()
            attribute = club.attributes[self.attributeid]

            stadium = data.stadiums[stadiumid].name
            button.set_label("%s" % (stadium))

            attribute.stadium = stadiumid

        dialog.destroy()

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.save_fields()

        self.destroy()

    def load_fields(self):
        club = data.clubs[self.clubid]
        attribute = club.attributes[self.attributeid]

        year = str(attribute.year)
        stadium = data.stadiums[attribute.stadium].name

        self.comboboxYear.set_active_id(year)
        self.entryManager.set_text(attribute.manager)
        self.entryChairman.set_text(attribute.chairman)
        self.buttonStadium.set_label(stadium)
        self.spinbuttonReputation.set_value(attribute.reputation)

        self.year = year
        self.stadiumid = attribute.stadium

    def save_fields(self):
        club = data.clubs[self.clubid]
        attribute = club.attributes[self.attributeid]

        model = self.comboboxYear.get_model()
        treeiter = self.comboboxYear.get_active()
        attribute.year = int(model[treeiter][0])

        attribute.manager = self.entryManager.get_text()
        attribute.chairman = self.entryChairman.get_text()
        attribute.reputation = self.spinbuttonReputation.get_value_as_int()
        attribute.stadium = self.stadiumid

    def display(self, clubid=None, attributeid=None):
        self.show_all()

        if clubid:
            self.clubid = clubid
            self.attributeid = attributeid

            self.load_fields()

        self.run()
