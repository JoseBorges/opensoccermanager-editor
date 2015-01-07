#!/usr/bin/env python

from gi.repository import Gtk

import data
import widgets
import players
import clubs
import nations
import stadiums
import dialogs
import database


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Editor")
        self.set_default_size(640, 480)
        self.maximize()
        self.connect("destroy", self.close_application)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        menubar = Gtk.MenuBar()
        self.grid.attach(menubar, 0, 0, 1, 1)

        menuitem = widgets.MenuItem("_File")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = widgets.MenuItem("_Open Database")
        key, mod = Gtk.accelerator_parse("<CONTROL>O")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.open_database)
        menu.append(menuitem)
        menuitem = widgets.MenuItem("_Save Database")
        key, mod = Gtk.accelerator_parse("<CONTROL>S")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.save_database)
        menu.append(menuitem)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitem = widgets.MenuItem("_Quit")
        key, mod = Gtk.accelerator_parse("<CONTROL>Q")
        menuitem.add_accelerator("activate", accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menuitem.connect("activate", self.close_application)
        menu.append(menuitem)

        menuitem = widgets.MenuItem("_View")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

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

        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 1, 1, 1)
        toolbuttonAdd = Gtk.ToolButton(label="_Add")
        toolbuttonAdd.set_use_underline(True)
        toolbuttonAdd.set_icon_name("gtk-add")
        toolbuttonAdd.connect("clicked", self.add_data)
        toolbar.add(toolbuttonAdd)
        toolbuttonEdit = Gtk.ToolButton(label="_Edit")
        widgets.toolbuttonEdit = toolbuttonEdit
        toolbuttonEdit.set_use_underline(True)
        toolbuttonEdit.set_icon_name("gtk-edit")
        toolbuttonEdit.connect("clicked", self.edit_data)
        toolbar.add(toolbuttonEdit)
        toolbuttonRemove = Gtk.ToolButton(label="_Remove")
        widgets.toolbuttonRemove = toolbuttonRemove
        toolbuttonRemove.set_use_underline(True)
        toolbuttonRemove.set_icon_name("gtk-remove")
        toolbuttonRemove.connect("clicked", self.remove_data)
        toolbar.add(toolbuttonRemove)
        separator = Gtk.SeparatorToolItem()
        toolbar.add(separator)
        toolbuttonSave = Gtk.ToolButton(label="_Save")
        toolbuttonSave.set_use_underline(True)
        toolbuttonSave.set_icon_name("gtk-save")
        toolbuttonSave.set_tooltip_text("Save Changes to Database")
        toolbuttonSave.connect("clicked", self.save_database)
        toolbar.add(toolbuttonSave)

        self.notebook = Gtk.Notebook()
        self.notebook.set_hexpand(True)
        self.notebook.set_vexpand(True)
        self.notebook.set_border_width(5)
        self.grid.attach(self.notebook, 0, 2, 1, 1)

    def open_database(self, widget=None):
        filename = dialogs.open_dialog()

        if filename:
            if db.cursor:
                db.disconnect()

            if db.connect(filename) is not False:
                db.load()
                self.update_title(filename)
                players.populate()
                clubs.populate()
                nations.populate()
                stadiums.populate()

    def save_database(self, widget):
        db.save()

    def update_title(self, filename):
        self.set_title("Editor - %s" % (filename))

    def add_data(self, toolbutton):
        page = self.notebook.get_current_page()

        if page == 0:
            state = dialogs.add_player_dialog()

            if state:
                players.populate()
        elif page == 1:
            state = dialogs.add_club_dialog()

            if state:
                clubs.populate()
        elif page == 2:
            state = dialogs.add_nation_dialog()

            if state:
                nations.populate()
        elif page == 3:
            state = dialogs.add_stadium_dialog()

            if state:
                stadiums.populate()

    def edit_data(self, toolbutton):
        page = self.notebook.get_current_page()

        if page == 0:
            state = dialogs.add_player_dialog(players.selected)

            if state:
                players.populate()
        elif page == 1:
            state = dialogs.add_club_dialog(clubs.selected)

            if state:
                clubs.populate()
        elif page == 2:
            state = dialogs.add_nation_dialog(nations.selected)

            if state:
                nations.populate()
        elif page == 3:
            state = dialogs.add_stadium_dialog(stadiums.selected)

            if state:
                stadiums.populate()

    def remove_data(self, toolbutton):
        page = self.notebook.get_current_page()

        state = dialogs.remove_dialog(page)

        if state:
            if page == 0:
                del(data.players[players.selected])
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
                    dialogs.error(0)
                else:
                    del(data.nations[nations.selected])
                    nations.populate()
            elif page == 3:
                del(data.stadiums[stadiums.selected])
                stadiums.populate()

    def move_notebook_page(self, menuitem, direction):
        if direction == -1:
            self.notebook.prev_page()
        elif direction == 1:
            self.notebook.next_page()

    def switch_notebook_page(self, menuitem, page):
        self.notebook.set_current_page(page)

    def run(self):
        self.open_database()

        self.notebook.append_page(players, Gtk.Label("Players"))
        self.notebook.append_page(clubs, Gtk.Label("Clubs"))
        self.notebook.append_page(nations, Gtk.Label("Nations"))
        self.notebook.append_page(stadiums, Gtk.Label("Stadiums"))

        self.show_all()

    def close_application(self, widget):
        if db.cursor is not None:
            db.disconnect()

        Gtk.main_quit()


widgets.window = Window()
players = players.Players()
clubs = clubs.Clubs()
nations = nations.Nations()
stadiums = stadiums.Stadiums()
db = database.Database()


if __name__ == "__main__":
    widgets.window.run()

    Gtk.main()
