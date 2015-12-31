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

        self.populate_data()

    def get_clubid(self):
        '''
        Return a new club ID.
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
        Return player for given club id.
        '''
        return self.clubs[clubid]

    def add_club(self):
        '''
        Add club to the data structure.
        '''
        clubid = self.get_clubid()
        club = structures.clubs.Club(clubid)
        self.clubs[clubid] = club

        data.unsaved = True

        return clubid

    def remove_club(self, clubid):
        '''
        Remove club from data structure.
        '''
        del self.clubs[clubid]

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
                attribute = structures.attributes.Attribute()
                attributeid = value[0]
                club.attributes[attributeid] = attribute

                attribute.year = value[2]
                attribute.league = value[3]
                attribute.manager = value[4]
                attribute.chairman = value[5]
                attribute.stadium = value[6]
                attribute.reputation = value[7]

            if clubid > self.clubid:
                self.clubid = clubid

class Club:
    def __init__(self, clubid):
        self.clubid = clubid
        self.name = ""
        self.nickname = ""

        self.attributes = {}

    def get_players_associated(self):
        '''
        Return whether club has any associated players.
        '''
        state = False

        for playerid, player in data.players.get_players():
            for attributeid, attribute in player.attributes.items():
                if attribute.club == self.clubid:
                    state = True
                    break

        return state
