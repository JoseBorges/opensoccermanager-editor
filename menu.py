#!/usr/bin/env python3

from gi.repository import Gtk

import widgets


class Menu(Gtk.MenuBar):
    def __init__(self):
        Gtk.MenuBar.__init__(self)
        self.set_hexpand(True)

        menuitem = widgets.MenuItem("_File")
        self.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        self.menuitemNew = widgets.MenuItem("_New...")
        key, mod = Gtk.accelerator_parse("<CONTROL>N")
        self.menuitemNew.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNew)
        self.menuitemOpen = widgets.MenuItem("_Open...")
        key, mod = Gtk.accelerator_parse("<CONTROL>O")
        self.menuitemOpen.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemOpen)
        self.menuitemSave = widgets.MenuItem("_Save")
        key, mod = Gtk.accelerator_parse("<CONTROL>S")
        self.menuitemSave.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        self.menuitemSave.set_sensitive(False)
        menu.append(self.menuitemSave)
        self.menuitemSaveAs = widgets.MenuItem("_Save As...")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>S")
        self.menuitemSaveAs.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        self.menuitemSaveAs.set_sensitive(False)
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
        self.menuitemQuit = widgets.MenuItem("_Quit")
        key, mod = Gtk.accelerator_parse("<CONTROL>Q")
        self.menuitemQuit.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemQuit)

        menuitem = widgets.MenuItem("_Edit")
        self.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        self.menuitemAdd = widgets.MenuItem("_Add Item")
        self.menuitemAdd.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<CONTROL>A")
        self.menuitemAdd.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemAdd)
        self.menuitemRemove = widgets.MenuItem("_Remove Item")
        self.menuitemRemove.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<CONTROL>R")
        self.menuitemRemove.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemRemove)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemPreferences = widgets.MenuItem("_Preferences")
        menu.append(self.menuitemPreferences)

        self.menuView = widgets.MenuItem("_View")
        self.menuView.set_sensitive(False)
        self.append(self.menuView)

        menu = Gtk.Menu()
        self.menuView.set_submenu(menu)

        self.menuitemPrevious = widgets.MenuItem("_Previous Tab")
        key, mod = Gtk.accelerator_parse("<ALT>Left")
        self.menuitemPrevious.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemPrevious)
        self.menuitemNext = widgets.MenuItem("_Next Tab")
        key, mod = Gtk.accelerator_parse("<ALT>Right")
        self.menuitemNext.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNext)

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)

        self.menuitemPlayers = widgets.MenuItem("_Players")
        key, mod = Gtk.accelerator_parse("<ALT>1")
        self.menuitemPlayers.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemPlayers)
        self.menuitemClubs = widgets.MenuItem("_Clubs")
        key, mod = Gtk.accelerator_parse("<ALT>2")
        self.menuitemClubs.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemClubs)
        self.menuitemNations = widgets.MenuItem("_Nations")
        key, mod = Gtk.accelerator_parse("<ALT>3")
        self.menuitemNations.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNations)
        self.menuitemStadiums = widgets.MenuItem("_Stadiums")
        key, mod = Gtk.accelerator_parse("<ALT>4")
        self.menuitemStadiums.add_accelerator("activate", widgets.accelgroup, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemStadiums)

        self.menuTools = widgets.MenuItem("_Tools")
        self.menuTools.set_sensitive(False)
        self.append(self.menuTools)

        menu = Gtk.Menu()
        self.menuTools.set_submenu(menu)

        self.menuitemValidate = widgets.MenuItem("_Validate Database")
        menu.append(self.menuitemValidate)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemFilter = widgets.MenuItem("_Data Filter")
        menu.append(self.menuitemFilter)
        self.menuitemClear = widgets.MenuItem("_Clear Filter")
        menu.append(self.menuitemClear)

        menuitem = widgets.MenuItem("_Help")
        self.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)

        self.menuitemAbout = widgets.MenuItem("_About")
        menu.append(self.menuitemAbout)


class ContextMenu(Gtk.Menu):
    def __init__(self, item=""):
        Gtk.Menu.__init__(self)

        self.menuitemEdit = widgets.MenuItem("_Edit Item")
        self.append(self.menuitemEdit)
        self.menuitemRemove = widgets.MenuItem("_Remove Item")
        self.append(self.menuitemRemove)
