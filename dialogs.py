#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import unicodedata
import re
import csv

import data
import database
import dialogs
import display
import filters
import preferences
import widgets


class AboutDialog(Gtk.AboutDialog):
    def __init__(self):
        Gtk.AboutDialog.__init__(self)

        path = os.path.join("resources", "logo.svg")
        icon = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 64, 64)

        self.set_transient_for(widgets.window)
        self.set_program_name("Editor")
        self.set_comments("Data editor for OpenSoccerManager")
        self.set_website("http://opensoccermanager.org/")
        self.set_website_label("Website")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo(icon)


class Preferences(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_title("Preferences")
        self.set_border_width(5)
        self.set_resizable(False)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        commonframe = widgets.CommonFrame("Interface")
        grid.attach(commonframe, 0, 0, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        commonframe.insert(grid1)

        self.checkbuttonQuit = Gtk.CheckButton("Display confirmation dialog when _quitting")
        self.checkbuttonQuit.set_use_underline(True)
        self.checkbuttonQuit.connect("toggled", self.quit_toggled)
        grid1.attach(self.checkbuttonQuit, 0, 0, 1, 1)
        self.checkbuttonRemove = Gtk.CheckButton("Display confirmation dialog when _removing items")
        self.checkbuttonRemove.set_use_underline(True)
        self.checkbuttonRemove.connect("toggled", self.remove_toggled)
        grid1.attach(self.checkbuttonRemove, 0, 1, 1, 1)
        self.checkbuttonToolbar = Gtk.CheckButton("_Show toolbar")
        self.checkbuttonToolbar.set_use_underline(True)
        self.checkbuttonToolbar.connect("toggled", self.toolbar_toggled)
        grid1.attach(self.checkbuttonToolbar, 0, 2, 1, 1)

    def response_handler(self, widget, event):
        self.hide()

    def remove_toggled(self, checkbutton):
        data.options.confirm_remove = checkbutton.get_active()
        data.options["INTERFACE"]["ConfirmRemove"] = str(data.options.confirm_remove)

        data.options.write_file()

    def quit_toggled(self, checkbutton):
        data.options.confirm_quit = checkbutton.get_active()
        data.options["INTERFACE"]["ConfirmQuit"] = str(data.options.confirm_quit)

        data.options.write_file()

    def toolbar_toggled(self, checkbutton):
        data.options.show_toolbar = checkbutton.get_active()
        data.options["INTERFACE"]["ShowToolbar"] = str(data.options.show_toolbar)
        widgets.window.toolbar.set_visible(data.options.show_toolbar)

        data.options.write_file()

    def display(self):
        self.checkbuttonQuit.set_active(data.options.confirm_quit)
        self.checkbuttonRemove.set_active(data.options.confirm_remove)
        self.checkbuttonToolbar.set_active(data.options.show_toolbar)

        self.show_all()
        self.run()


class NewDatabase(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_title("New Database")
        self.set_transient_for(widgets.window)
        self.add_button("C_ancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Create", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.set_current_name("New Database")
        self.set_do_overwrite_confirmation(True)

    def display(self):
        self.show_all()

        filename = None

        if self.run() == Gtk.ResponseType.OK:
            filename = self.get_filename()

        self.hide()

        return filename


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
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("changed", self.changed_search)
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

    def changed_search(self, entry):
        if entry.get_text() is "":
            self.populate(data.players)

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
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
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
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("changed", self.changed_search)
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def changed_search(self, entry):
        if entry.get_text() is "":
            self.populate(data.clubs)

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
        self.populate(data.clubs)

    def treeselection_changed(self, treeselection):
        state = not treeselection.count_selected_rows() == 0
        self.set_response_sensitive(Gtk.ResponseType.OK, state)

        model, treeiter = treeselection.get_selected()

        if treeiter:
            treepath = model.get_path(treeiter)
            treeview = treeselection.get_tree_view()
            treeview.scroll_to_cell(treepath)

    def display(self, clubid, year):
        self.populate(data.clubs, year)

        for item in self.treemodelsort:
            if item[0] == clubid:
                self.treeselection.select_iter(item.iter)

        self.entrySearch.set_text("")
        self.set_focus(self.entrySearch)
        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            clubid = model[treeiter][0]

        self.hide()

        return clubid

    def populate(self, data, year):
        self.liststore.clear()

        for clubid, club in data.items():
            for attributeid, attribute in club.attributes.items():
                if attribute.year == year:
                    self.liststore.append([clubid, club.name])


class NationSelectionDialog(Gtk.Dialog):
    def __init__(self, parent):
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
        self.treeselection.connect("changed", self.treeselection_changed)
        scrolledwindow.add(treeview)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.connect("activate", self.activate_search)
        self.entrySearch.connect("icon-press", self.clear_search)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

    def treeselection_changed(self, treeselection):
        state = not treeselection.count_selected_rows() == 0
        self.set_response_sensitive(Gtk.ResponseType.OK, state)

        model, treeiter = treeselection.get_selected()
        treeview = treeselection.get_tree_view()

        if treeiter:
            treepath = model.get_path(treeiter)
            treeview.scroll_to_cell(treepath)

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

        self.date_of_birth = None

    def display(self, date):
        state = False

        if date:
            year, month, day = list(map(int, date.split("-")))
        else:
            year, month, day = [data.season - 18, 1, 1]

        self.calendar.select_day(day)
        self.calendar.select_month(month - 1, year)

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            year, month, day = self.calendar.get_date()

            month += 1

            if month < 10:
                month = "0%i" % (month)
            else:
                month = str(month)

            if day < 10:
                day = "0%i" % (day)
            else:
                day = str(day)

            self.date_of_birth = "%i-%s-%s" % (year, month, day)

            state = True

        self.hide()

        return state


class DataImport(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("Import Data")
        self.set_border_width(5)
        self.set_transient_for(widgets.window)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Import", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("_Data To Import")
        grid.attach(label, 0, 0, 1, 1)
        self.combobox = Gtk.ComboBoxText()
        self.combobox.append("0", "Players")
        self.combobox.append("1", "Clubs")
        self.combobox.append("2", "Nations")
        self.combobox.append("3", "Stadiums")
        self.combobox.set_active(0)
        label.set_mnemonic_widget(self.combobox)
        grid.attach(self.combobox, 1, 0, 1, 1)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("CSV Files")
        filefilter.add_pattern("*.csv")

        label = widgets.Label("_File Location")
        grid.attach(label, 0, 1, 1, 1)
        self.filechooserbutton = Gtk.FileChooserButton()
        self.filechooserbutton.set_hexpand(True)
        self.filechooserbutton.add_filter(filefilter)
        label.set_mnemonic_widget(self.filechooserbutton)
        grid.attach(self.filechooserbutton, 1, 1, 1, 1)

    def display(self):
        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            selected = self.combobox.get_active_id()
            path = self.filechooserbutton.get_filename()

            with open("%s" % (path), "r") as fp:
                reader = csv.reader(fp, delimiter=",")

                for item in reader:
                    if selected == "0":
                        data.player(item)
                    elif selected == "1":
                        data.club(item)
                    elif selected == "2":
                        data.nation(item)
                    elif selected == "3":
                        data.stadium(item)

        self.destroy()


class DataExport(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("Export Data")
        self.set_border_width(5)
        self.set_transient_for(widgets.window)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Export", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("Data To Export")
        grid.attach(label, 0, 0, 1, 1)
        self.combobox = Gtk.ComboBoxText()
        self.combobox.append("0", "All")
        self.combobox.append("1", "Players")
        self.combobox.append("2", "Clubs")
        self.combobox.append("3", "Nations")
        self.combobox.append("4", "Stadiums")
        self.combobox.set_active(0)
        grid.attach(self.combobox, 1, 0, 1, 1)

    def display(self):
        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        def export(table):
            data.db.cursor.execute("SELECT * FROM %s" % (table))
            values = data.db.cursor.fetchall()

            with open("%s.csv" % (table), "w", newline="") as fp:
                writer = csv.writer(fp, delimiter=",")
                writer.writerows(values)

        if response == Gtk.ResponseType.OK:
            items = ("player", "club", "nation", "stadium")

            active = int(self.combobox.get_active_id())

            if active == 0:
                for table in items:
                    export(table)
            else:
                table = items[active - 1]
                export(table)


class Filter(Gtk.Dialog):
    def __init__(self):
        self.criteria = None

        Gtk.Dialog.__init__(self)
        self.set_transient_for(widgets.window)
        self.set_border_width(5)
        self.set_title("Data Filter")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Filter", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        notebook = Gtk.Notebook()
        grid.attach(notebook, 0, 0, 1, 1)

        self.players = filters.Players()
        self.clubs = filters.Clubs()
        self.nations = filters.Nations()
        self.stadiums = filters.Stadiums()

        label = widgets.Label("_Players")
        notebook.append_page(self.players, label)

        label = widgets.Label("_Clubs")
        notebook.append_page(self.clubs, label)

        label = widgets.Label("_Nations")
        notebook.append_page(self.nations, label)

        label = widgets.Label("_Stadiums")
        notebook.append_page(self.stadiums, label)

    def display(self):
        self.show_all()
        self.run()

        return self.criteria

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.criteria = self.players.get_criteria()

        self.hide()


def remove_dialog(index):
    item = ("Player", "Club", "Nation", "Stadium")[index]

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Remove %s" % (item))
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Remove %s from database?" % (item.lower()))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def remove_from_squad_dialog(mode=0):
    if mode == 0:
        title = "Remove From Squad"
        primary = "Remove selected player from squad?"
        secondary = "The player will not be assigned to any club."
        button = "Remove"
    elif mode == 1:
        title = "Clear Squad"
        primary = "Clear all players from the squad?"
        secondary = "All the players will be assigned to no club."
        button = "Clear"

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title(title)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_%s" % (button), Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("<span size='12000'><b>%s</b></span>" % (primary))
    messagedialog.format_secondary_text(secondary)

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def file_dialog(mode=0):
    if mode == 0:
        title = "Open File"
        button = "Open"
    elif mode == 1:
        title = "Save File"
        button = "Save"

    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(widgets.window)
    dialog.set_title(title)
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_%s" % (button), Gtk.ResponseType.OK)
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


def unsaved_dialog():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Unsaved Data")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Quit", Gtk.ResponseType.CLOSE)
    messagedialog.add_button("_Save and Quit", Gtk.ResponseType.OK)
    messagedialog.set_markup("<span size='12000'><b>The database is currently unsaved.</b></span>")
    messagedialog.format_secondary_text("Do you want to save it before closing?")

    response = messagedialog.run()

    state = 0

    if response == Gtk.ResponseType.CLOSE:
        state = 1
    elif response == Gtk.ResponseType.OK:
        state = 2

    messagedialog.destroy()

    return state


def quit_dialog():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Quit Editor")
    messagedialog.add_button("_Do Not Quit", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Quit", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("Quit the data editor?")

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def noerrors():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Validation Results")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("There were no errors found while validating the database.")

    messagedialog.run()
    messagedialog.destroy()


def error(errorid):
    errors = {0: "Unable to delete club as a player is still assigned to it.",
              1: "Unable to delete nation as a player is still assigned to it.",
              2: "Unable to delete stadium as a club is still assigned to it.",
              }

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Foreign Key Error")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("<span size='12000'><b>Foreign key error</b></span>")
    messagedialog.format_secondary_text(errors[errorid])

    messagedialog.run()
    messagedialog.destroy()


def squad_error(errorid):
    errors = {0: ("There are too many players in the squad.",
                  "Each team is allowed a maximum of 30 players."),
              1: ("There are too few players in the squad.",
                  "Each team is allowed a minimum of 16 players."),
             }

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(widgets.window)
    messagedialog.set_title("Squad Error")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("<span size='12000'><b>%s</b></span>" % (errors[errorid][0]))
    messagedialog.format_secondary_text(errors[errorid][1])

    messagedialog.run()
    messagedialog.destroy()
