#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import os
import re
import unicodedata

import clubs
import data
import database
import dialogs
import menu
import nations
import players
import preferences
import stadiums
import validation
import widgets


class Window(Gtk.Window):
    def __init__(self):
        data.options.read_file()

        iconpath = os.path.join("resources", "logo.svg")

        Gtk.Window.__init__(self)
        self.set_title("Editor")
        self.set_icon_from_file(iconpath)
        self.connect("delete-event", self.close_application)
        self.set_default_size(data.options.window_width,
                              data.options.window_height)

        if data.options.window_maximize:
            self.maximize()
        else:
            self.unmaximize()

        widgets.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(widgets.accelgroup)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        mainmenu = menu.Menu()
        self.grid.attach(mainmenu, 0, 0, 1, 1)

        self.menuView = mainmenu.menuView
        self.menuTools = mainmenu.menuTools

        mainmenu.menuitemNew.connect("activate", new_database)
        mainmenu.menuitemOpen.connect("activate", new_database, 1)
        self.menuitemSave = mainmenu.menuitemSave
        mainmenu.menuitemSave.connect("activate", self.save_database)
        self.menuitemSaveAs = mainmenu.menuitemSaveAs
        mainmenu.menuitemSaveAs.connect("activate", self.save_database)
        self.menuitemImport = mainmenu.menuitemImport
        mainmenu.menuitemImport.connect("activate", self.data_import)
        self.menuitemExport = mainmenu.menuitemExport
        mainmenu.menuitemExport.connect("activate", self.data_export)
        mainmenu.menuitemQuit.connect("activate", self.close_application)
        self.menuitemAdd = mainmenu.menuitemAdd
        mainmenu.menuitemAdd.connect("activate", self.add_data)
        self.menuitemEdit = mainmenu.menuitemEdit
        mainmenu.menuitemEdit.connect("activate", self.edit_data)
        self.menuitemRemove = mainmenu.menuitemRemove
        mainmenu.menuitemRemove.connect("activate", self.remove_data)
        mainmenu.menuitemPreferences.connect("activate", self.open_preferences)
        mainmenu.menuitemPrevious.connect("activate", self.move_notebook_page, -1)
        mainmenu.menuitemNext.connect("activate", self.move_notebook_page, 1)
        mainmenu.menuitemPlayers.connect("activate", self.switch_notebook_page, 0)
        mainmenu.menuitemClubs.connect("activate", self.switch_notebook_page, 1)
        mainmenu.menuitemNations.connect("activate", self.switch_notebook_page, 2)
        mainmenu.menuitemStadiums.connect("activate", self.switch_notebook_page, 3)
        self.menuitemValidate = mainmenu.menuitemValidate
        mainmenu.menuitemValidate.connect("activate", self.validate_database)
        self.menuitemFilter = mainmenu.menuitemFilter
        mainmenu.menuitemFilter.connect("activate", self.filter_data)
        mainmenu.menuitemClear.connect("activate", self.clear_data)
        mainmenu.menuitemAbout.connect("activate", self.about_dialog)

        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_sensitive(False)
        self.grid.attach(self.toolbar, 0, 1, 1, 1)
        toolbuttonAdd = Gtk.ToolButton(label="_Add")
        toolbuttonAdd.set_use_underline(True)
        toolbuttonAdd.set_icon_name("gtk-add")
        toolbuttonAdd.set_tooltip_text("Add item to database")
        toolbuttonAdd.connect("clicked", self.add_data)
        self.toolbar.add(toolbuttonAdd)
        toolbuttonEdit = Gtk.ToolButton(label="_Edit")
        widgets.toolbuttonEdit = toolbuttonEdit
        toolbuttonEdit.set_use_underline(True)
        toolbuttonEdit.set_icon_name("gtk-edit")
        toolbuttonEdit.set_tooltip_text("Edit selected item")
        toolbuttonEdit.connect("clicked", self.edit_data)
        self.toolbar.add(toolbuttonEdit)
        toolbuttonRemove = Gtk.ToolButton(label="_Remove")
        widgets.toolbuttonRemove = toolbuttonRemove
        toolbuttonRemove.set_use_underline(True)
        toolbuttonRemove.set_icon_name("gtk-remove")
        toolbuttonRemove.set_tooltip_text("Remove item from database")
        toolbuttonRemove.connect("clicked", self.remove_data)
        self.toolbar.add(toolbuttonRemove)
        separator = Gtk.SeparatorToolItem()
        self.toolbar.add(separator)
        self.toolbuttonSave = Gtk.ToolButton(label="_Save")
        self.toolbuttonSave.set_use_underline(True)
        self.toolbuttonSave.set_icon_name("gtk-save")
        self.toolbuttonSave.set_tooltip_text("Save changes to database")
        self.toolbuttonSave.connect("clicked", self.save_database)
        self.toolbar.add(self.toolbuttonSave)

    def about_dialog(self, menuitem):
        aboutdialog = dialogs.AboutDialog()
        aboutdialog.run()
        aboutdialog.destroy()

    def validate_database(self, menuitem):
        validator = validation.Validate()
        validator.run()
        validator.destroy()

    def filter_data(self, menuitem):
        filter_dialog = dialogs.Filter()
        criteria = filter_dialog.display()

        if criteria:
            filtered = {}

            for playerid, player in data.players.items():
                show = False

                if criteria[0](player.age, criteria[1]):
                    show = True

                if show:
                    filtered[playerid] = player

            players.populate(items=filtered)

        filter_dialog.destroy()

    def clear_data(self, menuitem):
        players.populate()

    def save_database(self, widget):
        if widget in (self.menuitemSave, self.toolbuttonSave):
            data.db.save()
            data.unsaved = False
        elif widget is self.menuitemSaveAs:
            filename = dialogs.file_dialog(mode=1)

            if filename:
                data.db.connect(filename)
                data.db.save()
                data.unsaved = False

                self.update_title(filename)

    def open_preferences(self, menuitem):
        preferences_dialog = dialogs.Preferences()
        preferences_dialog.display()
        preferences_dialog.hide()

    def data_import(self, menuitem):
        import_dialog = dialogs.DataImport()
        import_dialog.display()
        import_dialog.destroy()

    def data_export(self, menuitem):
        export_dialog = dialogs.DataExport()
        export_dialog.display()
        export_dialog.destroy()

    def update_title(self, filename):
        self.set_title("Editor - %s" % (filename))

    def add_data(self, toolbutton):
        page = maineditor.get_current_page()

        if page == 0:
            dialogs.players.display()

            if dialogs.players.state:
                players.populate()
                data.unsaved = True
        elif page == 1:
            dialogs.clubs.display()

            if dialogs.clubs.state:
                clubs.populate()
                data.unsaved = True
        elif page == 2:
            dialogs.nations.display()

            if dialogs.nations.state:
                nations.populate()
                data.unsaved = True
        elif page == 3:
            dialogs.stadiums.display()

            if dialogs.stadiums.state:
                stadiums.populate()
                data.unsaved = True

    def edit_data(self, toolbutton):
        page = maineditor.get_current_page()

        if page == 0:
            dialogs.players.display(playerid=players.selected)

            if dialogs.players.state:
                players.populate()
                data.unsaved = True
        elif page == 1:
            dialogs.clubs.display(clubid=clubs.selected)

            if dialogs.clubs.state:
                clubs.populate()
                data.unsaved = True
        elif page == 2:
            dialogs.nations.display(nationid=nations.selected)

            if dialogs.nations.state:
                nations.populate()
                data.unsaved = True
        elif page == 3:
            dialogs.stadiums.display(stadiumid=stadiums.selected)

            if dialogs.stadiums.state:
                stadiums.populate()
                data.unsaved = True

    def remove_data(self, toolbutton):
        page = maineditor.get_current_page()

        if data.options.confirm_remove:
            state = dialogs.remove_dialog(index=page)
        else:
            state = True

        if state:
            if page == 0:
                for item in players.selected:
                    del(data.players[item])

                players.populate()
                data.unsaved = True
            elif page == 1:
                keys = [player.club for player in data.players.values()]

                if [item for item in clubs.selected if item in keys]:
                    dialogs.error(0)
                else:
                    for item in clubs.selected:
                        del(data.clubs[item])

                    clubs.populate()
                    data.unsaved = True
            elif page == 2:
                keys = [player.nationality for player in data.players.values()]

                if [item for item in nations.selected if item in keys]:
                    dialogs.error(1)
                else:
                    for item in nations.selected:
                        del(data.nations[item])

                    nations.populate()
                    data.unsaved = True
            elif page == 3:
                keys = [club.stadium for club in data.clubs.values()]

                if [item for item in stadiums.selected if item in keys]:
                    dialogs.error(2)
                else:
                    for item in stadiums.selected:
                        del(data.stadiums[stadiums.selected])

                    stadiums.populate()
                    data.unsaved = True

    def move_notebook_page(self, menuitem, direction):
        if direction == -1:
            if maineditor.get_current_page() == 0:
                maineditor.set_current_page(maineditor.get_n_pages() - 1)
            else:
                maineditor.prev_page()
        elif direction == 1:
            if maineditor.get_n_pages() == maineditor.get_current_page() + 1:
                maineditor.set_current_page(0)
            else:
                maineditor.next_page()

    def switch_notebook_page(self, menuitem, page):
        maineditor.set_current_page(page)

    def close_application(self, widget, event=None):
        if data.unsaved:
            state = dialogs.unsaved_dialog()

            if state == 1:
                if data.db.cursor:
                    data.db.disconnect()

                self.quit_application()
            elif state == 2:
                data.db.save()

                if data.db.cursor:
                    data.db.disconnect()

                self.quit_application()
        else:
            if data.options.confirm_quit:
                state = dialogs.quit_dialog()

                if state:
                    if data.db.cursor:
                        data.db.disconnect()

                    self.quit_application()
            else:
                self.quit_application()

        return True

    def quit_application(self):
        width = str(self.get_size()[0])
        height = str(self.get_size()[1])

        if self.is_maximized():
            data.options["INTERFACE"]["Maximized"] = "True"
        else:
            data.options["INTERFACE"]["Width"] = width
            data.options["INTERFACE"]["Height"] = height
            data.options["INTERFACE"]["Maximized"] = "False"

        data.options.write_file()

        Gtk.main_quit()

    def run(self):
        self.grid.attach(mainmenu, 0, 2, 1, 1)

        self.show_all()

        self.toolbar.set_visible(data.options.show_toolbar)


class MainMenu(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_column_spacing(5)
        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)

        label = Gtk.Label()
        self.attach(label, 0, 0, 1, 1)
        label = Gtk.Label()
        self.attach(label, 3, 2, 1, 2)

        image = Gtk.Image.new_from_icon_name("gtk-new",
                                             Gtk.IconSize.DIALOG)

        buttonNew = widgets.Button("_New Database")
        buttonNew.set_always_show_image(True)
        buttonNew.set_image(image)
        buttonNew.set_image_position(Gtk.PositionType.TOP)
        buttonNew.set_tooltip_text("Create a new database file")
        buttonNew.connect("clicked", new_database)
        self.attach(buttonNew, 1, 1, 1, 1)

        image = Gtk.Image.new_from_icon_name("gtk-open",
                                             Gtk.IconSize.DIALOG)

        buttonOpen = widgets.Button("_Open Database")
        buttonOpen.set_always_show_image(True)
        buttonOpen.set_image(image)
        buttonOpen.set_image_position(Gtk.PositionType.TOP)
        buttonOpen.set_tooltip_text("Open existing database file")
        buttonOpen.connect("clicked", new_database, 1)
        self.attach(buttonOpen, 2, 1, 1, 1)

    def run(self):
        self.show_all()


class MainEditor(Gtk.Notebook):
    active = False

    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.connect("switch-page", self.switch_page)

    def run(self):
        widgets.window.menuView.set_sensitive(True)
        widgets.window.menuTools.set_sensitive(True)
        widgets.window.menuitemSave.set_sensitive(True)
        widgets.window.menuitemSaveAs.set_sensitive(True)
        widgets.window.menuitemImport.set_sensitive(True)
        widgets.window.menuitemExport.set_sensitive(True)
        widgets.window.menuitemAdd.set_sensitive(True)
        widgets.window.menuitemEdit.set_sensitive(True)
        widgets.window.menuitemRemove.set_sensitive(True)
        widgets.window.toolbar.set_sensitive(True)

        players.run()
        clubs.run()
        nations.run()
        stadiums.run()

        if not self.active:
            self.add_tabs()
            self.active = True

        self.show_all()

    def add_tabs(self):
        widgets.window.grid.attach(self, 0, 3, 1, 1)
        self.append_page(players, widgets.Label("_Players"))
        self.append_page(clubs, widgets.Label("_Clubs"))
        self.append_page(nations, widgets.Label("_Nations"))
        self.append_page(stadiums, widgets.Label("_Stadiums"))

    def switch_page(self, notebook, page, number):
        if page.selected is None:
            widgets.window.menuitemEdit.set_sensitive(False)
            widgets.window.menuitemRemove.set_sensitive(False)
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)
        else:
            widgets.window.menuitemEdit.set_sensitive(True)
            widgets.window.menuitemRemove.set_sensitive(True)
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)


def new_database(widget=None, mode=0):
    if mode == 0:
        new_database = dialogs.NewDatabase()
        filename = new_database.display()
    elif mode == 1:
        filename = dialogs.file_dialog(mode=0)

    if filename:
        if data.db.connect(filename):
            widgets.window.update_title(filename)
            widgets.window.grid.remove(mainmenu)

            data.db.load()

            players.populate()
            #clubs.populate()
            nations.populate()
            #stadiums.populate()

            maineditor.run()


data.options = preferences.Preferences()

widgets.window = Window()
mainmenu = MainMenu()
maineditor = MainEditor()
players = players.Players()
clubs = clubs.Clubs()
nations = nations.Nations()
stadiums = stadiums.Stadiums()
data.db = database.Database()
widgets.window.run()


if __name__ == "__main__":
    Gtk.main()
