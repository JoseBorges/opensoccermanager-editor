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
        Add  to the data structure.
        '''
        leagueid = self.get_leagueid()
        league = League(leagueid)
        self.leagues[leagueid] = league

        data.unsaved = True

        return league

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
            league = League(item[0])
            self.leagues[league.leagueid] = league

            league.name = item[1]

            data.database.cursor.execute("SELECT * FROM leagueattr WHERE league=?", (league.leagueid,))
            leagueattrs = data.database.cursor.fetchall()

            for value in leagueattrs:
                attribute = Attribute(league.leagueid)
                attributeid = value[0]
                attribute.year = value[2]
                league.attributes[attributeid] = attribute

                if attributeid > league.attributeid:
                    league.attributeid = attributeid

            if league.leagueid > self.leagueid:
                self.leagueid = league.leagueid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM league")
        leagues = [league[0] for league in data.database.cursor.fetchall()]

        for leagueid, league in self.leagues.items():
            if leagueid in leagues:
                data.database.cursor.execute("UPDATE league SET name=? WHERE id=?", (league.name, leagueid,))
            else:
                data.database.cursor.execute("INSERT INTO league VALUES (null, ?)", (league.name,))

            data.database.cursor.execute("SELECT * FROM leagueattr WHERE league=?", (leagueid,))
            attributes = [attribute[0] for attribute in data.database.cursor.fetchall()]

            for attributeid, attribute in league.attributes.items():
                if attributeid in attributes:
                    data.database.cursor.execute("UPDATE leagueattr SET league=?, year=? WHERE id=?", (leagueid, attribute.year, attributeid))
                else:
                    data.database.cursor.execute("INSERT INTO leagueattr VALUES (null, ?, ?)", (leagueid, attribute.year))

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
        '''
        Return a new league attribute id.
        '''
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        '''
        Add league attribute to data structure.
        '''
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute(self.leagueid)

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        '''
        Remove league attribute from data structure.
        '''
        del self.attributes[attributeid]

        data.unsaved = True

    def can_remove(self):
        '''
        Return whether league can be removed from data set.
        '''
        return self.attributes == {}


class Attribute(structures.attributes.Attribute):
    def __init__(self, leagueid):
        structures.attributes.Attribute.__init__(self)

        self.leagueid = leagueid

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

    def get_referee_count(self):
        '''
        Return number of referees associated with attribute data.
        '''
        count = 0

        for refereeid, referee in data.referees.get_referees():
            for attributeid, attribute in referee.attributes.items():
                if attribute.year == self.year:
                    if attribute.league == self.leagueid:
                        count += 1

        return count
