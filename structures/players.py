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

        self.deletions = []

        self.populate_data()

    def get_playerid(self):
        '''
        Return a new player id.
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
        self.deletions.append(playerid)

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

                if attributeid > player.attributeid:
                    player.attributeid = attributeid

            if playerid > self.playerid:
                self.playerid = playerid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM player")
        players = [player[0] for player in data.database.cursor.fetchall()]

        for playerid, player in self.players.items():
            date_of_birth = "%i-%i-%i" % (player.date_of_birth)

            if playerid in players:
                data.database.cursor.execute("UPDATE player SET firstname=?, secondname=?, commonname=?, dateofbirth=?, nation=? WHERE id=?", (player.first_name, player.second_name, player.common_name, date_of_birth, player.nationality, playerid))
            else:
                data.database.cursor.execute("INSERT INTO player VALUES (null, ?, ?, ?, ?, ?)", (player.first_name, player.second_name, player.common_name, date_of_birth, player.nationality))

            data.database.cursor.execute("SELECT * FROM playerattr WHERE player=?", (playerid,))
            attributes = [attribute[0] for attribute in data.database.cursor.fetchall()]

            for attributeid, attribute in player.attributes.items():
                if attributeid in attributes:
                    data.database.cursor.execute("UPDATE playerattr SET player=?, year=?, club=?, position=?, keeping=?, tackling=?, passing=?, shooting=?, heading=?, pace=?, stamina=?, ballcontrol=?, setpieces=?, training=? WHERE id=?", (playerid, attribute.year, attribute.club, attribute.position, attribute.keeping, attribute.tackling, attribute.passing, attribute.shooting, attribute.heading, attribute.pace, attribute.stamina, attribute.ball_control, attribute.set_pieces, attribute.training, attributeid))
                else:
                    data.database.cursor.execute("INSERT INTO playerattr VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, attribute.year, attribute.club, attribute.position, attribute.keeping, attribute.tackling, attribute.passing, attribute.shooting, attribute.heading, attribute.pace, attribute.stamina, attribute.ball_control, attribute.set_pieces, attribute.training))

        for playerid in players:
            if playerid in self.deletions:
                data.database.cursor.execute("DELETE FROM player WHERE id=?", (playerid,))

        self.deletions.clear()


class Player:
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.common_name = ""
        self.date_of_birth = None
        self.nationality = None

        self.attributes = {}
        self.attributeid = 0

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

        if self.first_name == "" and self.second_name == "":
            name = ""

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

    def get_age(self, year):
        '''
        Return age of player calculated from passed year attribute value.
        '''
        age = year - self.date_of_birth[0]

        if (self.date_of_birth[1], self.date_of_birth[2]) > (8, 1):
            age -= 1

        return age

    def get_attributeid(self):
        '''
        Return a new player attribute id.
        '''
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        '''
        Add player attribute to data structure.
        '''
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute()

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        '''
        Remove player attribute from data structure.
        '''
        del self.attributes[attributeid]

        data.unsaved = True


class Attribute(structures.attributes.Attribute):
    def __init__(self):
        structures.attributes.Attribute.__init__(self)

    def get_club_name(self):
        '''
        Return name of club associated with attribute.
        '''
        if self.club:
            club = data.clubs.get_club_by_id(self.club)

            return club.name
        else:
            return ""

    def get_skills(self):
        '''
        Return tuple of player skill values.
        '''
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
