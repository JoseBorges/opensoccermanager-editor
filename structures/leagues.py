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


import data
import structures.attributes

class Leagues:
    def __init__(self):
        self.leagues = {}
        self.leagueid = 0

        self.populate_data()

    def get_leagueid(self):
        '''
        Return a new league ID.
        '''
        self.leagueid += 1

        return self.leagueid

    def get_leagues(self):
        '''
        Return complete dictionary of leagues.
        '''
        return self.leagues.items()

    def get_league_by_id(self, leagueid):
        '''
        Return league for given league id.
        '''
        return self.leagues[leagueid]

    def get_league_count(self):
        '''
        Get number of leagues in data structure.
        '''
        return len(self.leagues)

    def add_league(self):
        '''
        Add referee to the data structure.
        '''
        leagueid = self.get_leagueid()
        self.leagues[leagueid] = League()

        return leagueid

    def remove_league(self, leagueid):
        '''
        Remove league from data structure.
        '''
        del self.leagues[leagueid]

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM league")

        for item in data.database.cursor.fetchall():
            league = League()
            leagueid = item[0]
            league.name = item[1]
            self.leagues[leagueid] = league

            data.database.cursor.execute("SELECT * FROM leagueattr WHERE league=?", (leagueid,))
            leagueattrs = data.database.cursor.fetchall()

            for value in leagueattrs:
                attribute = Attribute()
                attributeid = value[0]
                attribute.year = value[2]
                league.attributes[attributeid] = attribute

            if leagueid > self.leagueid:
                self.leagueid = leagueid


class League:
    def __init__(self):
        self.name = ""

        self.attributes = {}

    def get_clubs(self):
        '''
        Return tuple of clubs associated with league.
        '''


class Attribute:
    def __init__(self):
        self.year = 2000

    def get_club_count(self):
        print(self.attributes.items())

        return 0
