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

        self.deletions = []

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
        self.leagues[leagueid] = League(leagueid)

        data.unsaved = True

        return leagueid

    def remove_league(self, leagueid):
        '''
        Remove league from data structure.
        '''
        del self.leagues[leagueid]
        self.deletions.append(leagueid)

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM league")

        for item in data.database.cursor.fetchall():
            leagueid = item[0]
            league = League(leagueid)
            league.name = item[1]
            self.leagues[leagueid] = league

            data.database.cursor.execute("SELECT * FROM leagueattr WHERE league=?", (leagueid,))
            leagueattrs = data.database.cursor.fetchall()

            for value in leagueattrs:
                attribute = Attribute(leagueid)
                attributeid = value[0]
                attribute.year = value[2]
                league.attributes[attributeid] = attribute

                if attributeid > league.attributeid:
                    league.attributeid = attributeid

            if leagueid > self.leagueid:
                self.leagueid = leagueid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM league")
        leagues = [league[0] for league in data.database.cursor.fetchall()]

        for leagueid, league in self.get_leagues():
            if leagueid in leagues:
                data.database.cursor.execute("UPDATE league SET name=? WHERE id=?", (league.name, leagueid,))
            else:
                data.database.cursor.execute("INSERT INTO league VALUES (null, ?)", (league.name,))

        for leagueid in leagues:
            if leagueid in self.deletions:
                data.database.cursor.execute("DELETE FROM league WHERE id=?", (leagueid,))

        self.deletions.clear()


class League:
    def __init__(self, leagueid):
        self.leagueid = leagueid
        self.name = ""

        self.attributes = {}
        self.attributeid = 0

    def get_attributeid(self):
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute(self.leagueid)

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        del self.attributes[attributeid]

        data.unsaved = True

    def can_remove(self):
        '''
        Return whether league can be removed from data set.
        '''
        return self.attributes == {}


class Attribute(structures.attributes.Attribute):
    def __init__(self, leagueid):
        self.leagueid = leagueid

        structures.attributes.Attribute.__init__(self)

    def get_club_count(self):
        '''
        Return number of clubs associated with attribute data.
        '''
        count = 0

        for clubid, club in data.clubs.get_clubs():
            for attributeid, attribute in club.attributes.items():
                if attribute.year == self.year:
                    if attribute.league == self.leagueid:
                        count += 1

        return count
