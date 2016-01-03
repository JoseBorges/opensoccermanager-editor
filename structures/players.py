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


class Players:
    def __init__(self):
        self.players = {}
        self.playerid = 0

        self.populate_data()

    def get_playerid(self):
        '''
        Return a new player ID.
        '''
        self.playerid += 1

        return self.playerid

    def get_players(self):
        '''
        Return complete dictionary of players.
        '''
        return self.players.items()

    def get_player_by_id(self, playerid):
        '''
        Return player for given player id.
        '''
        return self.players[playerid]

    def get_player_count(self):
        '''
        Get number of players in data structure.
        '''
        return len(self.players)

    def add_player(self):
        '''
        Add player to the data structure.
        '''
        playerid = self.get_playerid()
        self.players[playerid] = Player()

        data.unsaved = True

        return playerid

    def remove_player(self, playerid):
        '''
        Remove player from data structure.
        '''
        del self.players[playerid]

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM player")
        players = data.database.cursor.fetchall()

        for item in players:
            player = Player()
            playerid = item[0]
            self.players[playerid] = player

            player.first_name = item[1]
            player.second_name = item[2]
            player.common_name = item[3]
            player.date_of_birth = tuple(map(int, item[4].split("-")))
            player.nationality = item[5]

            data.database.cursor.execute("SELECT * FROM playerattr WHERE player=?", (playerid,))
            playerattrs = data.database.cursor.fetchall()

            for value in playerattrs:
                attribute = Attribute()
                attributeid = value[0]
                player.attributes[attributeid] = attribute

                attribute.year = value[2]
                attribute.club = value[3]
                attribute.position = value[4]
                attribute.keeping = value[5]
                attribute.tackling = value[6]
                attribute.passing = value[7]
                attribute.shooting = value[8]
                attribute.heading = value[9]
                attribute.pace = value[10]
                attribute.stamina = value[11]
                attribute.ball_control = value[12]
                attribute.set_pieces = value[13]
                attribute.training = value[14]

                if attributeid > attribute.attributeid:
                    attribute.attributeid = attributeid

            if playerid > self.playerid:
                self.playerid = playerid


class Player:
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.common_name = ""
        self.date_of_birth = None
        self.nationality = None

        self.attributes = {}

    def get_name(self, mode=0):
        '''
        Return common name or first and second name combination.
        '''
        if self.common_name:
            name = self.common_name
        else:
            if mode == 0:
                name = "%s, %s" % (self.second_name, self.first_name)
            elif mode == 1:
                name = "%s %s" % (self.first_name, self.second_name)

        return name

    def get_date_of_birth(self):
        '''
        Return tuple for date of birth.
        '''
        if self.date_of_birth:
            year, month, date = self.date_of_birth

            year = str(year)

            if month < 10:
                month = "0%i" % (month)
            else:
                month = str(month)

            if date < 10:
                date = "0%i" % (date)
            else:
                date = str(date)

            return year, month, date
        else:
            return None


class Attribute:
    def __init__(self):
        self.attributeid = 0

    def get_skills(self):
        skills = (self.keeping,
                  self.tackling,
                  self.passing,
                  self.shooting,
                  self.heading,
                  self.pace,
                  self.stamina,
                  self.ball_control,
                  self.set_pieces)

        return skills
