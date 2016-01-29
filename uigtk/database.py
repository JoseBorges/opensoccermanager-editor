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
import uigtk.widgets


class DatabaseCounts(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Database Information")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("Players", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.labelPlayerCount = uigtk.widgets.Label(leftalign=True)
        self.labelPlayerCount.set_label("%i" % (data.players.get_player_count()))
        grid.attach(self.labelPlayerCount, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Clubs", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.labelClubCount = uigtk.widgets.Label(leftalign=True)
        self.labelClubCount.set_label("%i" % (data.clubs.get_club_count()))
        grid.attach(self.labelClubCount, 1, 1, 1, 1)

        label = uigtk.widgets.Label("Stadiums", leftalign=True)
        grid.attach(label, 0, 2, 1, 1)
        self.labelStadiumCount = uigtk.widgets.Label(leftalign=True)
        self.labelStadiumCount.set_label("%i" % (data.stadiums.get_stadium_count()))
        grid.attach(self.labelStadiumCount, 1, 2, 1, 1)

        label = uigtk.widgets.Label("Leagues", leftalign=True)
        grid.attach(label, 0, 3, 1, 1)
        self.labelLeagueCount = uigtk.widgets.Label(leftalign=True)
        self.labelLeagueCount.set_label("%i" % (data.leagues.get_league_count()))
        grid.attach(self.labelLeagueCount, 1, 3, 1, 1)

        label = uigtk.widgets.Label("Referees", leftalign=True)
        grid.attach(label, 0, 4, 1, 1)
        self.labelRefereeCount = uigtk.widgets.Label(leftalign=True)
        self.labelRefereeCount.set_label("%i" % (data.referees.get_referee_count()))
        grid.attach(self.labelRefereeCount, 1, 4, 1, 1)

        label = uigtk.widgets.Label("Nations", leftalign=True)
        grid.attach(label, 0, 5, 1, 1)
        self.labelNationCount = uigtk.widgets.Label(leftalign=True)
        self.labelNationCount.set_label("%i" % (data.nations.get_nation_count()))
        grid.attach(self.labelNationCount, 1, 5, 1, 1)

        self.show_all()

    def on_response(self, *args):
        self.destroy()
