#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import unicodedata
import re

import data
import database
import dialogs
import display
import preferences
import widgets


def about():
    path = os.path.join("resources", "logo.svg")
    icon = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 64, 64)

    aboutdialog = Gtk.AboutDialog()
    aboutdialog.set_transient_for(widgets.window)
    aboutdialog.set_program_name("Editor")
    aboutdialog.set_comments("Data editor for OpenSoccerManager")
    aboutdialog.set_website("http://opensoccermanager.org/")
    aboutdialog.set_website_label("Website")
    aboutdialog.set_license_type(Gtk.License.GPL_3_0)
    aboutdialog.set_logo(icon)

    aboutdialog.run()
    aboutdialog.destroy()


class Preferences(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_title("Preferences")
        self.set_border_width(5)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        self.checkbuttonQuit = Gtk.CheckButton("_Display confirmation dialog when quitting")
        self.checkbuttonQuit.set_use_underline(True)
        self.checkbuttonQuit.connect("toggled", self.quit_toggled)
        grid.attach(self.checkbuttonQuit, 0, 0, 1, 1)

    def response_handler(self, widget, event):
        self.hide()

    def quit_toggled(self, checkbutton):
        data.options.confirm_quit = checkbutton.get_active()
        data.options["INTERFACE"]["ConfirmQuit"] = str(data.options.confirm_quit)

        data.options.write_file()

    def run(self):
        self.checkbuttonQuit.set_active(data.options.confirm_quit)

        self.show_all()


class NewDatabase(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("New Database")
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.add_button("C_ancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Create", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_Season")
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonSeason = Gtk.SpinButton.new_with_range(1950, 2049, 1)
        label.set_mnemonic_widget(self.spinbuttonSeason)
        grid.attach(self.spinbuttonSeason, 1, 0, 1, 1)

        label = widgets.Label("_Location")
        grid.attach(label, 0, 1, 1, 1)
        self.filechooserLocation = Gtk.FileChooserButton()
        self.filechooserLocation.set_hexpand(True)
        self.filechooserLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        label.set_mnemonic_widget(self.filechooserLocation)
        grid.attach(self.filechooserLocation, 1, 1, 2, 1)

    def display(self):
        self.show_all()

        filepath = None

        if self.run() == Gtk.ResponseType.OK:
            season = self.spinbuttonSeason.get_value_as_int()
            year = str(season)[2:4]
            year1 = str(season + 1)[2:4]
            data.season = season
            filename = "osm%s%s.db" % (year, year1)

            if self.filechooserLocation.get_current_folder() is not None:
                folder = self.filechooserLocation.get_current_folder()
                filepath = os.path.join(folder, filename)
            else:
                if self.filechooserLocation.get_filename() is not None:
                    folder = self.filechooserLocation.get_filename()
                    filepath = os.path.join(folder, filename)
                else:
                    filepath = filename

        self.hide()

        return filepath


class PlayerSelectionDialog(Gtk.Dialog):
    def __init__(self):
        def treeselection_changed(treeselection):
            if treeselection.count_selected_rows() == 0:
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.set_response_sensitive(Gtk.ResponseType.OK, True)

        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_default_size(-1, 250)
        self.set_title("Select Player")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststore = Gtk.ListStore(int, str)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.liststore)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def display(self, parent):
        self.set_transient_for(parent)
        self.populate(data.players)
        self.entrySearch.set_text("")

        self.set_focus(self.entrySearch)
        self.show_all()

        player = None

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()

            if treeiter:
                player = model[treeiter][0]

        self.hide()

        return player

    def activate_search(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            items = {}

            for playerid, player in data.players.items():
                both = "%s %s" % (player.first_name, player.second_name)

                for search in (player.second_name, player.first_name, player.common_name, both):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        items[playerid] = player

                        break

            self.populate(items)

    def clear_search(self, entry, icon, event):
        entry.set_text("")

        self.populate(data.players)

    def populate(self, data):
        self.liststore.clear()

        for playerid, player in data.items():
            name = display.name(player)
            self.liststore.append([playerid, name])


class ClubSelectionDialog(Gtk.Dialog):
    def __init__(self, parent):
        def treeselection_changed(treeselection):
            if treeselection.count_selected_rows() == 0:
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.set_response_sensitive(Gtk.ResponseType.OK, True)

            model, treeiter = treeselection.get_selected()

            if treeiter:
                treepath = model.get_path(treeiter)
                treeview.scroll_to_cell(treepath)

        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_default_size(-1, 250)
        self.set_transient_for(parent)
        self.set_title("Select Club")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststore = Gtk.ListStore(int, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def activate_search(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            items = {}

            for clubid, club in data.clubs.items():
                for search in (club.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        items[clubid] = club

                        break

            self.populate(items)

    def clear_search(self, entry, icon, event):
        entry.set_text("")

        self.populate(data.clubs)

    def display(self, clubid):
        self.populate(data.clubs)

        for item in self.treemodelsort:
            if item[0] == clubid:
                self.treeselection.select_iter(item.iter)

        self.set_focus(self.entrySearch)
        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            clubid = model[treeiter][0]

        self.hide()

        return clubid

    def populate(self, data):
        self.liststore.clear()

        for clubid, club in data.items():
            self.liststore.append([clubid, club.name])


class NationSelectionDialog(Gtk.Dialog):
    def __init__(self, parent):
        def treeselection_changed(treeselection):
            if treeselection.count_selected_rows() == 0:
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.set_response_sensitive(Gtk.ResponseType.OK, True)

            model, treeiter = treeselection.get_selected()

            if treeiter:
                treepath = model.get_path(treeiter)
                treeview.scroll_to_cell(treepath)

        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_default_size(-1, 250)
        self.set_transient_for(parent)
        self.set_title("Select Club")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()
        self.liststore = Gtk.ListStore(int, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def display(self, nationid):
        self.populate(data.nations)

        for item in self.treemodelsort:
            if item[0] == nationid:
                self.treeselection.select_iter(item.iter)

        self.set_focus(self.entrySearch)
        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            nationid = model[treeiter][0]

        self.hide()

        return nationid

    def activate_search(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            items = {}

            for nationid, nation in data.nations.items():
                for search in (nation.name,):
                    search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

                    if re.findall(criteria, search, re.IGNORECASE):
                        items[nationid] = nation

                        break

            self.populate(items)

    def clear_search(self, entry, icon, event):
        entry.set_text("")

        self.populate(data.nations)

    def populate(self, data):
        self.liststore.clear()

        for nationid, nation in data.items():
            self.liststore.append([nationid, nation.name])


class DateOfBirth(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(parent)
        self.set_title("Date of Birth")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        self.calendar = Gtk.Calendar()
        self.calendar.set_property("year", True)
        self.vbox.add(self.calendar)

    def display(self, date):
        if date != 0:
            year, month, day = list(map(int, date))

            self.calendar.select_day(day)
            self.calendar.select_month(month - 1, year)
        else:
            year, month, day = [data.season - 18, 1, 1]

            self.calendar.select_day(day)
            self.calendar.select_month(month - 1, year)

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            year, month, day = self.calendar.get_date()

            month += 1

        if day < 10:
            day = "0%i" % (day)
        else:
            day = str(day)

        if month < 10:
            month = "0%i" % (month)
        else:
            month = str(month)

        date_of_birth = [year, month, day]

        self.hide()

        return date_of_birth


def remove_dialog(index, parent):
    item = ("Player", "Club", "Nation", "Stadium")[index]

    dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    dialog.set_transient_for(parent)
    dialog.set_title("Remove %s" % (item))
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Remove", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.CANCEL)
    dialog.set_markup("Remove %s from database?" % (item.lower()))

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        state = True

    dialog.destroy()

    return state


def open_dialog():
    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title("Open File")
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Open", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("All Files")
    filefilter.add_pattern("*")
    dialog.add_filter(filefilter)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("Database Files")
    filefilter.add_pattern("*.db")
    dialog.add_filter(filefilter)
    dialog.set_filter(filefilter)

    filename = None

    if dialog.run() == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()

    return filename


def save_dialog():
    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title("Save File")
    dialog.set_action(Gtk.FileChooserAction.SAVE)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Save", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("All Files")
    filefilter.add_pattern("*")
    dialog.add_filter(filefilter)

    filefilter = Gtk.FileFilter()
    filefilter.set_name("Database Files")
    filefilter.add_pattern("*.db")
    dialog.add_filter(filefilter)
    dialog.set_filter(filefilter)

    filename = None

    if dialog.run() == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()

    return filename


def quit_dialog():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Quit Editor")
    messagedialog.add_button("_Do Not Quit", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Quit", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("Quit the data editor?")

    state = 0

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = 1

    messagedialog.destroy()

    return state


def error(errorid):
    errors = {0: "Unable to delete club as a player is still assigned to it.",
              1: "Unable to delete nation as a player is still assigned to it.",
              2: "Unable to delete stadium as a club is still assigned to it.",
              }

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Error")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("<span size='12000'><b>Foreign key error</b></span>")
    messagedialog.format_secondary_text(errors[errorid])

    messagedialog.run()
    messagedialog.destroy()
