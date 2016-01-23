#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk

import data
import uigtk.about
import uigtk.database
import uigtk.filedialog
import uigtk.preferences
import uigtk.version
import uigtk.widgets
import uigtk.year


class Menu(Gtk.MenuBar):
    def __init__(self):
        Gtk.MenuBar.__init__(self)
        self.set_hexpand(True)

        menuitem = uigtk.widgets.MenuItem("_File")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemNew = uigtk.widgets.MenuItem("_New...")
        key, mod = Gtk.accelerator_parse("<Control>N")
        self.menuitemNew.add_accelerator("activate",
                                         data.window.accelgroup,
                                         key,
                                         mod,
                                         Gtk.AccelFlags.VISIBLE)
        self.menuitemNew.connect("activate", data.window.welcome.on_new_clicked)
        menu.append(self.menuitemNew)
        self.menuitemOpen = uigtk.widgets.MenuItem("_Open...")
        key, mod = Gtk.accelerator_parse("<Control>O")
        self.menuitemOpen.add_accelerator("activate",
                                         data.window.accelgroup,
                                         key,
                                         mod,
                                         Gtk.AccelFlags.VISIBLE)
        self.menuitemOpen.connect("activate", data.window.welcome.on_open_clicked)
        menu.append(self.menuitemOpen)
        self.menuitemSave = uigtk.widgets.MenuItem("_Save")
        self.menuitemSave.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<Control>S")
        self.menuitemSave.add_accelerator("activate",
                                          data.window.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        self.menuitemSave.connect("activate", self.on_save_clicked)
        menu.append(self.menuitemSave)
        self.menuitemSaveAs = uigtk.widgets.MenuItem("_Save As...")
        self.menuitemSaveAs.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<Control><Shift>S")
        self.menuitemSaveAs.add_accelerator("activate",
                                            data.window.accelgroup,
                                            key,
                                            mod,
                                            Gtk.AccelFlags.VISIBLE)
        self.menuitemSaveAs.connect("activate", self.on_save_as_clicked)
        menu.append(self.menuitemSaveAs)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemQuit = uigtk.widgets.MenuItem("_Quit")
        key, mod = Gtk.accelerator_parse("<Control>Q")
        menuitemQuit.add_accelerator("activate",
                                      data.window.accelgroup,
                                      key,
                                      mod,
                                      Gtk.AccelFlags.VISIBLE)
        menuitemQuit.connect("activate", self.on_quit_clicked)
        menu.append(menuitemQuit)

        menuitem = uigtk.widgets.MenuItem("_Edit")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemAdd = uigtk.widgets.MenuItem("_Add Item")
        self.menuitemAdd.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<Control><Shift>A")
        self.menuitemAdd.add_accelerator("activate",
                                         data.window.accelgroup,
                                         key,
                                         mod,
                                         Gtk.AccelFlags.VISIBLE)
        self.menuitemAdd.connect("activate", self.on_add_clicked)
        menu.append(self.menuitemAdd)
        self.menuitemRemove = uigtk.widgets.MenuItem("_Remove Item")
        self.menuitemRemove.set_sensitive(False)
        key, mod = Gtk.accelerator_parse("<Control><Shift>R")
        self.menuitemRemove.add_accelerator("activate",
                                            data.window.accelgroup,
                                            key,
                                            mod,
                                            Gtk.AccelFlags.VISIBLE)
        self.menuitemRemove.connect("activate", self.on_remove_clicked)
        menu.append(self.menuitemRemove)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemYearManager = uigtk.widgets.MenuItem("_Year Manager")
        self.menuitemYearManager.set_sensitive(False)
        self.menuitemYearManager.connect("activate", uigtk.year.YearManager)
        menu.append(self.menuitemYearManager)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemPreferences = uigtk.widgets.MenuItem("_Preferences")
        self.menuitemPreferences.connect("activate", uigtk.preferences.Preferences)
        menu.append(self.menuitemPreferences)

        self.menuitemView = uigtk.widgets.MenuItem("_View")
        self.menuitemView.set_sensitive(False)
        self.add(self.menuitemView)

        self.menuView = Gtk.Menu()
        self.menuitemView.set_submenu(self.menuView)

        self.menuitemPrevious = uigtk.widgets.MenuItem("_Previous Tab")
        key, mod = Gtk.accelerator_parse("<Alt>Left")
        self.menuitemPrevious.add_accelerator("activate",
                                              data.window.accelgroup,
                                              key,
                                              mod,
                                              Gtk.AccelFlags.VISIBLE)
        self.menuitemPrevious.connect("activate", self.on_previous_clicked)
        self.menuView.append(self.menuitemPrevious)
        self.menuitemNext = uigtk.widgets.MenuItem("_Next Tab")
        key, mod = Gtk.accelerator_parse("<Alt>Right")
        self.menuitemNext.add_accelerator("activate",
                                          data.window.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        self.menuitemNext.connect("activate", self.on_next_clicked)
        self.menuView.append(self.menuitemNext)

        separator = Gtk.SeparatorMenuItem()
        self.menuView.append(separator)

        menuitem = uigtk.widgets.MenuItem("_Help")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemDatabase = uigtk.widgets.MenuItem("_Database")
        self.menuitemDatabase.set_sensitive(False)
        self.menuitemDatabase.connect("activate", uigtk.database.DatabaseCounts)
        menu.append(self.menuitemDatabase)
        menuitem = uigtk.widgets.MenuItem("_Versions")
        menuitem.connect("activate", uigtk.version.Dialog)
        menu.append(menuitem)
        self.menuitemAbout = uigtk.widgets.MenuItem("_About")
        self.menuitemAbout.connect("activate", uigtk.about.AboutDialog)
        menu.append(self.menuitemAbout)

    def on_save_clicked(self, *args):
        '''
        Call save functions for each data set.
        '''
        data.database.save_database()

    def on_save_as_clicked(self, *args):
        print("Save As")

    def on_add_clicked(self, *args):
        '''
        Call add item function of current page type.
        '''
        page = data.window.notebook.get_page_type()
        page.add_item()

    def on_remove_clicked(self, *args):
        '''
        Call remove item function of current page type.
        '''
        page = data.window.notebook.get_page_type()
        page.remove_item()

    def on_previous_clicked(self, *args):
        '''
        Move to previous tab page.
        '''
        data.window.notebook.prev_page()

    def on_next_clicked(self, *args):
        '''
        Move to next tab page.
        '''
        data.window.notebook.next_page()

    def add_view_items(self):
        '''
        Add pages in notebook interface to view menu.
        '''
        for count, page in enumerate(data.pages):
            menuitem = uigtk.widgets.MenuItem("_%s" % (page.name))
            key, mod = Gtk.accelerator_parse("<Alt>%i" % (count + 1))
            menuitem.add_accelerator("activate",
                                     data.window.accelgroup,
                                     key,
                                     mod,
                                     Gtk.AccelFlags.VISIBLE)
            menuitem.connect("activate", data.window.notebook.set_visible_page, count)
            self.menuView.append(menuitem)

        self.menuView.show_all()

        self.set_menu_enabled()

    def set_menu_enabled(self):
        '''
        Enable relevant items when selected database is loaded.
        '''
        self.menuitemSave.set_sensitive(True)
        self.menuitemSaveAs.set_sensitive(True)
        self.menuitemAdd.set_sensitive(True)
        self.menuitemYearManager.set_sensitive(True)
        self.menuitemView.set_sensitive(True)
        self.menuitemDatabase.set_sensitive(True)

    def on_quit_clicked(self, *args):
        data.window.on_quit()
