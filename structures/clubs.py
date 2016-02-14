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


class Clubs:
    def __init__(self):
        self.clubs = {}
        self.clubid = 0

        self.deletions = []

        self.populate_data()

    def get_clubid(self):
        '''
        Return a new club id.
        '''
        self.clubid += 1

        return self.clubid

    def get_clubs(self):
        '''
        Return complete dictionary of clubs.
        '''
        return self.clubs.items()

    def get_club_by_id(self, clubid):
        '''
        Return club for given club id.
        '''
        if clubid:
            return self.clubs[clubid]
        else:
            return None

    def get_club_count(self):
        '''
        Get number of clubs in data structure.
        '''
        return len(self.clubs)

    def add_club(self):
        '''
        Add club to the data structure.
        '''
        clubid = self.get_clubid()
        self.clubs[clubid] = Club(clubid)

        data.unsaved = True

        return clubid

    def remove_club(self, clubid):
        '''
        Remove club from data structure.
        '''
        del self.clubs[clubid]
        self.deletions.append(clubid)

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM club")

        for item in data.database.cursor.fetchall():
            clubid = item[0]
            club = Club(clubid)
            self.clubs[clubid] = club

            club.name = item[1]
            club.nickname = item[2]

            data.database.cursor.execute("SELECT * FROM clubattr WHERE club=?", (clubid,))
            clubattrs = data.database.cursor.fetchall()

            for value in clubattrs:
                attribute = Attribute(clubid)
                attributeid = value[0]
                club.attributes[attributeid] = attribute

                attribute.year = value[2]
                attribute.league = value[3]
                attribute.manager = value[4]
                attribute.chairman = value[5]
                attribute.stadium = value[6]
                attribute.reputation = value[7]

                if attributeid > club.attributeid:
                    club.attributeid = attributeid

            if clubid > self.clubid:
                self.clubid = clubid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM club")
        clubs = [club[0] for club in data.database.cursor.fetchall()]

        for clubid, club in self.clubs.items():
            if clubid in clubs:
                data.database.cursor.execute("UPDATE club SET name=?, nickname=? WHERE id=?", (club.name, club.nickname, clubid))
            else:
                data.database.cursor.execute("INSERT INTO club VALUES (null, ?, ?)", (club.name, club.nickname))

            data.database.cursor.execute("SELECT * FROM clubattr WHERE club=?", (clubid,))
            attributes = [attribute[0] for attribute in data.database.cursor.fetchall()]

            for attributeid, attribute in club.attributes.items():
                if attributeid in attributes:
                    data.database.cursor.execute("UPDATE clubattr SET club=?, year=?, league=?, manager=?, chairman=?, stadium=?, reputation=? WHERE id=?", (clubid, attribute.year, attribute.league, attribute.manager, attribute.chairman, attribute.stadium, attribute.reputation, attributeid))
                else:
                    data.database.cursor.execute("INSERT INTO clubattr VALUES (null, ?, ?, ?, ?, ?, ?, ?)", (clubid, attribute.year, attribute.league, attribute.manager, attribute.chairman, attribute.stadium, attribute.reputation))

        for clubid in clubs:
            if clubid in self.deletions:
                data.database.cursor.execute("DELETE FROM club WHERE id=?", (nationid,))

        self.deletions.clear()


class Club:
    def __init__(self, clubid):
        self.clubid = clubid
        self.name = ""
        self.nickname = ""

        self.attributes = {}
        self.attributeid = 0

    def get_attributeid(self):
        '''
        Return a new club attribute id.
        '''
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        '''
        Add club attribute to data structure.
        '''
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute(self.clubid)

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        '''
        Remove club attribute from data structure.
        '''
        del self.attributes[attributeid]

        data.unsaved = True

    def can_remove(self):
        '''
        Return whether club has any associated players.
        '''
        return self.attributes == {}


class Attribute(structures.attributes.Attribute):
    def __init__(self, clubid):
        self.clubid = clubid
        self.league = None
        self.manager = ""
        self.chairman = ""
        self.stadium = None
        self.reputation = 1

        structures.attributes.Attribute.__init__(self)

    def get_player_count(self):
        '''
        Return number of players associated with attribute data.
        '''
        count = 0

        for playerid, player in data.players.get_players():
            for attributeid, attribute in player.attributes.items():
                if attribute.year == self.year:
                    if attribute.club == self.clubid:
                        count += 1

        return count
