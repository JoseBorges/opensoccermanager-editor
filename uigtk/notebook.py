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
import uigtk.clubs
import uigtk.leagues
import uigtk.nations
import uigtk.players
import uigtk.referees
import uigtk.search
import uigtk.stadiums
import uigtk.widgets


class Notebook(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)

        data.pages = []

        players = uigtk.players.Players()
        label = uigtk.widgets.Label("_%s" % (players.name))
        self.append_page(players, label)

        clubs = uigtk.clubs.Clubs()
        label = uigtk.widgets.Label("_%s" % (clubs.name))
        self.append_page(clubs, label)

        stadiums = uigtk.stadiums.Stadiums()
        label = uigtk.widgets.Label("_%s" % (stadiums.name))
        self.append_page(stadiums, label)

        leagues = uigtk.leagues.Leagues()
        label = uigtk.widgets.Label("_%s" % (leagues.name))
        self.append_page(leagues, label)

        referees = uigtk.referees.Referees()
        label = uigtk.widgets.Label("_%s" % (referees.name))
        self.append_page(referees, label)

        nations = uigtk.nations.Nations()
        label = uigtk.widgets.Label("_%s" % (nations.name))
        self.append_page(nations, label)

        data.pages = (players, clubs, stadiums, leagues, referees, nations)

        self.connect("switch-page", self.on_page_switched)

        self.show_all()

    def set_visible_page(self, notebook, page):
        '''
        Set currently visible page in notebook.
        '''
        self.set_current_page(page)

    def get_page_type(self):
        '''
        Return object for current page number.
        '''
        number = self.get_current_page()

        return data.pages[number]

    def on_page_switched(self, notebook, page, number):
        '''
        Handle toolbar button sensitivity on page switching.
        '''
        model, treeiter = page.search.treeselection.get_selected()

        if treeiter:
            data.window.toolbar.toolbuttonRemove.set_sensitive(True)
        else:
            data.window.toolbar.toolbuttonRemove.set_sensitive(False)
