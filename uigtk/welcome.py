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
import structures.clubs
import structures.database
import structures.leagues
import structures.nations
import structures.stadiums
import structures.players
import structures.referees
import structures.stadiums
import structures.years
import uigtk.filedialog
import uigtk.notebook
import uigtk.widgets


class Welcome(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(5)
        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)
        self.set_hexpand(True)
        self.set_vexpand(True)

        label = Gtk.Label()
        self.attach(label, 0, 0, 1, 1)
        label = Gtk.Label()
        self.attach(label, 3, 2, 1, 1)

        image = Gtk.Image.new_from_icon_name("gtk-new", Gtk.IconSize.DIALOG)

        buttonNew = uigtk.widgets.Button("_New Database")
        buttonNew.set_always_show_image(True)
        buttonNew.set_image(image)
        buttonNew.set_image_position(Gtk.PositionType.TOP)
        buttonNew.set_tooltip_text("Create a new database file.")
        buttonNew.connect("clicked", self.on_new_clicked)
        self.attach(buttonNew, 1, 1, 1, 1)

        image = Gtk.Image.new_from_icon_name("gtk-open", Gtk.IconSize.DIALOG)

        buttonOpen = uigtk.widgets.Button("_Open Database")
        buttonOpen.set_always_show_image(True)
        buttonOpen.set_image(image)
        buttonOpen.set_image_position(Gtk.PositionType.TOP)
        buttonOpen.set_tooltip_text("Open existing database file.")
        buttonOpen.connect("clicked", self.on_open_clicked)
        self.attach(buttonOpen, 2, 1, 1, 1)

    def on_new_clicked(self, *args):
        '''
        Display new database dialog and initialise editor window.
        '''
        dialog = uigtk.filedialog.NewDialog()
        filename = dialog.show()

        self.initialise_editor(filename)

    def on_open_clicked(self, *args):
        '''
        Display open database dialog and initialise editor window.
        '''
        dialog = uigtk.filedialog.OpenDialog()
        filename = dialog.show()

        self.initialise_editor(filename)

    def initialise_editor(self, filename):
        '''
        Instantiate data objects and add interface elements.
        '''
        if filename:
            data.window.set_title("Editor - %s" % (filename))

            data.database = structures.database.Database(filename)
            data.years = structures.years.Years()
            data.nations = structures.nations.Nations()
            data.referees = structures.referees.Referees()
            data.leagues = structures.leagues.Leagues()
            data.stadiums = structures.stadiums.Stadiums()
            data.clubs = structures.clubs.Clubs()
            data.players = structures.players.Players()

            if data.welcome:
                self.destroy()

                notebook = uigtk.notebook.Notebook()
                data.window.add_interface_widget(notebook)
                data.window.menu.add_view_items()
                data.window.toolbar.set_sensitive(True)

                data.welcome = False
            else:
                for page in data.pages:
                    page.populate_data()
