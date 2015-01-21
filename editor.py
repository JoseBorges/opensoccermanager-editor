#!/usr/bin/env python3

from gi.repository import Gtk
import os

import clubs
import data
import database
import dialogs
import nations
import players
import stadiums
import widgets


class Window(Gtk.Window):
    menuEdit = None
    menuView = None
    menuitemSave = None
    menuitemSaveAs = None
    menuitemImport = None
    menuitemExport = None
    toolbar = None

    def __init__(self):
        iconpath = os.path.join("resources", "logo.svg")

        Gtk.Window.__init__(self)
        self.set_title("Editor")
        self.set_icon_from_file(iconpath)
        self.set_default_size(640, 480)
        self.maximize()
        self.connect("destroy", self.close_application)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        self.grid.attach(menubar, 0, 0, 1, 1)

        menuitem = widgets.MenuItem("_File")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = widgets.MenuItem("_New")
        key, mod = Gtk.accelerator_parse("<CONTROL>N")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", new_database)
        menu.append(menuitem)
        menuitem = widgets.MenuItem("_Open")
        key, mod = Gtk.accelerator_parse("<CONTROL>O")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", open_database)
        menu.append(menuitem)
        self.menuitemSave = widgets.MenuItem("_Save")
        key, mod = Gtk.accelerator_parse("<CONTROL>S")
        self.menuitemSave.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        self.menuitemSave.set_sensitive(False)
        self.menuitemSave.connect("activate", self.save_database)
        menu.append(self.menuitemSave)
        self.menuitemSaveAs = widgets.MenuItem("_Save As...")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>S")
        self.menuitemSaveAs.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        self.menuitemSaveAs.set_sensitive(False)
        self.menuitemSaveAs.connect("activate", self.save_database)
        menu.append(self.menuitemSaveAs)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemImport = widgets.MenuItem("Import from CSV...")
        self.menuitemImport.set_sensitive(False)
        menu.append(self.menuitemImport)
        self.menuitemExport = widgets.MenuItem("Export to CSV...")
        self.menuitemExport.set_sensitive(False)
        menu.append(self.menuitemExport)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitem = widgets.MenuItem("_Quit")
        key, mod = Gtk.accelerator_parse("<CONTROL>Q")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.close_application)
        menu.append(menuitem)

        self.menuEdit = widgets.MenuItem("_Edit")
        self.menuEdit.set_sensitive(False)
        menubar.append(self.menuEdit)

        menu = Gtk.Menu()
        self.menuEdit.set_submenu(menu)

        menuitem = widgets.MenuItem("_Add Item")
        key, mod = Gtk.accelerator_parse("<CONTROL>A")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.add_data)
        menu.append(menuitem)
        menuitem = widgets.MenuItem("_Edit Item")
        key, mod = Gtk.accelerator_parse("<CONTROL>E")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.edit_data)
        menu.append(menuitem)
        menuitem = widgets.MenuItem("_Remove Item")
        key, mod = Gtk.accelerator_parse("<CONTROL>R")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.remove_data)
        menu.append(menuitem)

        self.menuView = widgets.MenuItem("_View")
        self.menuView.set_sensitive(False)
        menubar.append(self.menuView)

        menu = Gtk.Menu()
        self.menuView.set_submenu(menu)

        menuitem = widgets.MenuItem("_Previous Tab")
        key, mod = Gtk.accelerator_parse("<ALT>Left")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.move_notebook_page, -1)
        menu.append(menuitem)
        menuitem = widgets.MenuItem("_Next Tab")
        key, mod = Gtk.accelerator_parse("<ALT>Right")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.move_notebook_page, 1)
        menu.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)

        for count, label in enumerate(("Players", "Clubs", "Nations", "Stadiums")):
            menuitem = widgets.MenuItem("_%s" % (label))
            key, mod = Gtk.accelerator_parse("<ALT>%i" % (count + 1))
            menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
            menuitem.connect("activate", self.switch_notebook_page, count)
            menu.append(menuitem)

        menuitem = widgets.MenuItem("_Help")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = widgets.MenuItem("_About")
        menuitem.connect("activate", lambda i: dialogs.about())
        menu.append(menuitem)

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
        toolbuttonSave = Gtk.ToolButton(label="_Save")
        toolbuttonSave.set_use_underline(True)
        toolbuttonSave.set_icon_name("gtk-save")
        toolbuttonSave.set_tooltip_text("Save changes to database")
        toolbuttonSave.connect("clicked", self.save_database)
        self.toolbar.add(toolbuttonSave)

    def save_database(self, widget):
        data.db.save()

    def update_title(self, filename):
        self.set_title("Editor - %s" % (filename))

    def add_data(self, toolbutton):
        page = maineditor.get_current_page()

        if page == 0:
            widgets.players_dialog.display()

            if widgets.players_dialog.state:
                players.populate()
        elif page == 1:
            widgets.clubs_dialog.display()

            if widgets.clubs_dialog.state:
                clubs.populate()
        elif page == 2:
            widgets.nations_dialog.display()

            if widgets.nations_dialog.state:
                nations.populate()
        elif page == 3:
            state = dialogs.add_stadium_dialog()

            if state:
                stadiums.populate()

    def edit_data(self, toolbutton):
        page = maineditor.get_current_page()

        if page == 0:
            widgets.players_dialog.display(playerid=players.selected)

            if widgets.players_dialog.state:
                players.populate()
        elif page == 1:
            widgets.clubs_dialog.display(clubid=clubs.selected)

            if widgets.clubs_dialog.state:
                clubs.populate()
        elif page == 2:
            widgets.nations_dialog.display(nationid=nations.selected)

            if widgets.nations_dialog.state:
                nations.populate()
        elif page == 3:
            state = dialogs.add_stadium_dialog(stadiums.selected)

            if state:
                stadiums.populate()

    def remove_data(self, toolbutton):
        page = maineditor.get_current_page()

        state = dialogs.remove_dialog(index=page, parent=widgets.window)

        if state:
            if page == 0:
                for item in players.selected:
                    del(data.players[item])

                players.populate()
            elif page == 1:
                keys = [player.club for playerid, player in data.players.items()]

                if clubs.selected in keys:
                    dialogs.error(0)
                else:
                    del(data.clubs[clubs.selected])
                    clubs.populate()
            elif page == 2:
                keys = [player.nationality for playerid, player in data.players.items()]

                if nations.selected in keys:
                    dialogs.error(1)
                else:
                    del(data.nations[nations.selected])
                    nations.populate()
            elif page == 3:
                keys = [club.stadium for clubid, club in data.clubs.items()]

                if stadiums.selected in keys:
                    dialogs.error(2)
                else:
                    del(data.stadiums[stadiums.selected])
                    stadiums.populate()

    def move_notebook_page(self, menuitem, direction):
        if direction == -1:
            maineditor.prev_page()
        elif direction == 1:
            maineditor.next_page()

    def switch_notebook_page(self, menuitem, page):
        maineditor.set_current_page(page)

    def run(self):
        self.grid.attach(mainmenu, 0, 2, 1, 1)

        self.show_all()

    def close_application(self, widget):
        if data.db.cursor is not None:
            data.db.disconnect()

        Gtk.main_quit()


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
        buttonNew.connect("clicked", new_database)
        self.attach(buttonNew, 1, 1, 1, 1)

        image = Gtk.Image.new_from_icon_name("gtk-open",
                                             Gtk.IconSize.DIALOG)

        buttonOpen = widgets.Button("_Open Database")
        buttonOpen.set_always_show_image(True)
        buttonOpen.set_image(image)
        buttonOpen.set_image_position(Gtk.PositionType.TOP)
        buttonOpen.connect("clicked", open_database)
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
        widgets.window.menuEdit.set_sensitive(True)
        widgets.window.menuView.set_sensitive(True)
        widgets.window.menuitemSave.set_sensitive(True)
        widgets.window.menuitemSaveAs.set_sensitive(True)
        widgets.window.menuitemImport.set_sensitive(True)
        widgets.window.menuitemExport.set_sensitive(True)
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
        widgets.window.grid.attach(self, 0, 2, 1, 1)
        self.append_page(players, widgets.Label("_Players"))
        self.append_page(clubs, widgets.Label("_Clubs"))
        self.append_page(nations, widgets.Label("_Nations"))
        self.append_page(stadiums, widgets.Label("_Stadiums"))

    def switch_page(self, notebook, page, number):
        if page.selected is None:
            widgets.toolbuttonEdit.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)
        else:
            widgets.toolbuttonEdit.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)


def new_database(widget=None):
    filename = new_database.display()

    if filename:
        data.db.connect(filename=filename)

        widgets.window.update_title(filename)

        if widgets.window.grid.get_child_at(0, 2) is mainmenu:
            widgets.window.grid.remove(mainmenu)

        data.db.load()

        players.populate()
        clubs.populate()
        nations.populate()
        stadiums.populate()

        maineditor.run()


def open_database(widget=None):
    filename = dialogs.open_dialog()

    if filename:
        if data.db.connect(filename) is not False:
            data.db.load()

            players.populate()
            clubs.populate()
            nations.populate()
            stadiums.populate()

            widgets.window.update_title(filename)

            if widgets.window.grid.get_child_at(0, 2) is mainmenu:
                widgets.window.grid.remove(mainmenu)

            maineditor.run()


widgets.window = Window()
mainmenu = MainMenu()
maineditor = MainEditor()
widgets.players_dialog = dialogs.AddPlayerDialog()
widgets.clubs_dialog = dialogs.AddClubDialog()
widgets.nations_dialog = dialogs.AddNationDialog()
players = players.Players()
clubs = clubs.Clubs()
nations = nations.Nations()
stadiums = stadiums.Stadiums()
data.db = database.Database()
new_database = dialogs.NewDatabase()
widgets.window.run()


if __name__ == "__main__":
    Gtk.main()
