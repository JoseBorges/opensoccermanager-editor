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

        menubar = menu.Menu()
        self.grid.attach(menubar, 0, 0, 1, 1)

        self.menuView = menubar.menuView
        self.menuTools = menubar.menuTools

        menubar.menuitemNew.connect("activate", mainmenu.new_database)
        menubar.menuitemOpen.connect("activate", mainmenu.new_database, 1)
        self.menuitemSave = menubar.menuitemSave
        menubar.menuitemSave.connect("activate", self.save_database)
        self.menuitemSaveAs = menubar.menuitemSaveAs
        menubar.menuitemSaveAs.connect("activate", self.save_database)
        self.menuitemImport = menubar.menuitemImport
        menubar.menuitemImport.connect("activate", self.data_import)
        self.menuitemExport = menubar.menuitemExport
        menubar.menuitemExport.connect("activate", self.data_export)
        menubar.menuitemQuit.connect("activate", self.close_application)
        self.menuitemAdd = menubar.menuitemAdd
        menubar.menuitemAdd.connect("activate", self.add_data)
        self.menuitemRemove = menubar.menuitemRemove
        menubar.menuitemRemove.connect("activate", self.remove_data)
        self.menuitemYear = menubar.menuitemYear
        menubar.menuitemYear.connect("activate", self.year_manager)
        menubar.menuitemPreferences.connect("activate", self.open_preferences)
        menubar.menuitemPrevious.connect("activate", self.move_notebook_page, -1)
        menubar.menuitemNext.connect("activate", self.move_notebook_page, 1)
        menubar.menuitemPlayers.connect("activate", self.switch_notebook_page, 0)
        menubar.menuitemClubs.connect("activate", self.switch_notebook_page, 1)
        menubar.menuitemNations.connect("activate", self.switch_notebook_page, 2)
        menubar.menuitemStadiums.connect("activate", self.switch_notebook_page, 3)
        self.menuitemValidate = menubar.menuitemValidate
        menubar.menuitemValidate.connect("activate", self.validate_database)
        self.menuitemFilter = menubar.menuitemFilter
        menubar.menuitemFilter.connect("activate", self.filter_data)
        menubar.menuitemClear.connect("activate", self.clear_data)
        menubar.menuitemAbout.connect("activate", self.about_dialog)

        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_sensitive(False)
        self.grid.attach(self.toolbar, 0, 1, 1, 1)
        toolbuttonAdd = Gtk.ToolButton(label="_Add")
        toolbuttonAdd.set_use_underline(True)
        toolbuttonAdd.set_icon_name("gtk-add")
        toolbuttonAdd.set_tooltip_text("Add item to database")
        toolbuttonAdd.connect("clicked", self.add_data)
        self.toolbar.add(toolbuttonAdd)
        toolbuttonRemove = Gtk.ToolButton(label="_Remove")
        widgets.toolbuttonRemove = toolbuttonRemove
        toolbuttonRemove.set_sensitive(False)
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

    def year_manager(self, menuitem):
        year_dialog = dialogs.YearManager()
        year_dialog.display()
        year_dialog.destroy()

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
            players.add_player()

    def remove_data(self, toolbutton):
        page = maineditor.get_current_page()

        if data.options.confirm_remove:
            state = dialogs.remove_dialog(index=page)
        else:
            state = True

        if state:
            if page == 0:
                del data.players[players.selected]
                players.populate_data(values=data.players)
            elif page == 1:
                keys = []

                for player in data.players.values():
                    for attribute in player.attributes.values():
                        keys.append(attribute.club)

                if clubs.selected in keys:
                    dialogs.error(0)
                else:
                    del data.clubs[clubs.selected]
                    clubs.populate_data(values=data.clubs)
            elif page == 2:
                keys = [player.nationality for player in data.players.values()]

                if nations.selected in keys:
                    dialogs.error(1)
                else:
                    del data.nations[nations.selected]
                    nations.populate_data(values=data.nations)
            elif page == 3:
                keys = [club.stadium for club in data.clubs.values()]

                if [item for item in stadiums.selected if item in keys]:
                    dialogs.error(2)
                else:
                    for item in stadiums.selected:
                        del data.stadiums[stadiums.selected]

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
        self.active = False

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
        buttonNew.connect("clicked", self.new_database)
        self.attach(buttonNew, 1, 1, 1, 1)

        image = Gtk.Image.new_from_icon_name("gtk-open",
                                             Gtk.IconSize.DIALOG)

        buttonOpen = widgets.Button("_Open Database")
        buttonOpen.set_always_show_image(True)
        buttonOpen.set_image(image)
        buttonOpen.set_image_position(Gtk.PositionType.TOP)
        buttonOpen.set_tooltip_text("Open existing database file")
        buttonOpen.connect("clicked", self.new_database, 1)
        self.attach(buttonOpen, 2, 1, 1, 1)

    def new_database(self, widget=None, mode=0):
        if mode == 0:
            new_database = dialogs.NewDatabase()
            filename = new_database.display()
        elif mode == 1:
            filename = dialogs.file_dialog(mode=0)

        if filename:
            if data.db.connect(filename):
                widgets.window.update_title(filename)

                if not self.active:
                    widgets.window.grid.remove(mainmenu)
                    self.active = True

                data.db.load()

                maineditor.run()

    def run(self):
        self.show_all()


class MainEditor(Gtk.Notebook):
    def __init__(self):
        self.active = False

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
        widgets.window.menuitemYear.set_sensitive(True)
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
        if not page.selected:
            widgets.window.menuitemRemove.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)
        else:
            widgets.window.menuitemRemove.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)


data.options = preferences.Preferences()

mainmenu = MainMenu()
widgets.window = Window()
maineditor = MainEditor()
players = players.Players()
clubs = clubs.Clubs()
nations = nations.Nations()
stadiums = stadiums.Stadiums()
data.db = database.Database()
widgets.window.run()


if __name__ == "__main__":
    Gtk.main()
