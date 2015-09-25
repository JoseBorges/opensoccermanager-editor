#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager-Editor is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager-Editor is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager-Editor.  If not, see <http://www.gnu.org/licenses/>.


import data
import display


unsaved = False

years = []
players = {}
clubs = {}
leagues = {}
stadiums = {}
nations = {}


class Player:
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.common_name = ""
        self.date_of_birth = None
        self.nationality = None
        self.attributes = {}


class Club:
    def __init__(self):
        self.name = ""
        self.nickname = ""
        self.attributes = {}


class League:
    def __init__(self):
        self.name = ""
        self.attributes = {}


class Stadium:
    def __init__(self):
        self.name = ""
        self.attributes = {}


class Nation:
    def __init__(self):
        self.name = ""
        self.denonym = ""


class Attributes:
    pass


class IDNumbers:
    playerid = 0
    playerattrid = 0
    clubid = 0
    clubattrid = 0
    leagueid = 0
    nationid = 0
    stadiumid = 0
    stadiumattrid = 0

    def request_playerid(self):
        self.playerid += 1

        return self.playerid

    def request_playerattrid(self):
        self.playerattrid += 1

        return self.playerattrid

    def request_clubid(self):
        self.clubid += 1

        return self.clubid

    def request_clubattrid(self):
        self.clubattrid += 1

        return self.clubattrid

    def request_nationid(self):
        self.nationid += 1

        return self.nationid

    def request_stadiumid(self):
        self.stadiumid += 1

        return self.stadiumid

    def request_stadiumattrid(self):
        self.stadiumattrid += 1

        return self.stadiumattrid


idnumbers = IDNumbers()


def player(item):
    player = Player()
    playerid = item[0]
    player.first_name = item[1]
    player.second_name = item[2]
    player.common_name = item[3]
    player.date_of_birth = item[4]
    player.nationality = item[5]

    data.db.cursor.execute("SELECT * FROM playerattr WHERE player=?", (playerid,))

    for values in data.db.cursor.fetchall():
        attributes = Attributes()
        attributeid = values[0]
        attributes.year = values[2]

        if not values[3]:
            attributes.club = None
        else:
            attributes.club = values[3]

        attributes.position = values[4]
        attributes.keeping = values[5]
        attributes.tackling = values[6]
        attributes.passing = values[7]
        attributes.shooting = values[8]
        attributes.heading = values[9]
        attributes.pace = values[10]
        attributes.stamina = values[11]
        attributes.ball_control = values[12]
        attributes.set_pieces = values[13]
        attributes.training_value = values[14]

        player.attributes[attributeid] = attributes

        if attributeid > idnumbers.playerattrid:
            idnumbers.playerattrid = attributeid

    players[playerid] = player

    if playerid > idnumbers.playerid:
        idnumbers.playerid = playerid


def club(item):
    club = Club()
    clubid = item[0]
    club.name = item[1]
    club.nickname = item[2]

    data.db.cursor.execute("SELECT * FROM clubattr WHERE club=?", (clubid,))

    for values in data.db.cursor.fetchall():
        attributes = Attributes()
        attributeid = values[0]
        attributes.year = values[2]
        attributes.league = values[3]
        attributes.manager = values[4]
        attributes.chairman = values[5]
        attributes.stadium = values[6]
        attributes.reputation = values[7]

        club.attributes[attributeid] = attributes

        if attributeid > idnumbers.clubattrid:
            idnumbers.clubattrid = attributeid

    clubs[clubid] = club

    if clubid > idnumbers.clubid:
        idnumbers.clubid = clubid


def league(item):
    league = League()
    leagueid = item[0]
    league.name = item[1]

    leagues[leagueid] = league

    if leagueid > idnumbers.leagueid:
        idnumbers.leagueid = leagueid


def nation(item):
    nation = Nation()
    nationid = item[0]
    nation.name = item[1]
    nation.denonym = item[2]
    nations[nationid] = nation

    if nationid > idnumbers.nationid:
        idnumbers.nationid = nationid


def stadium(item):
    stadium = Stadium()
    stadiumid = item[0]
    stadium.name = item[1]

    data.db.cursor.execute("SELECT * FROM stadiumattr WHERE stadium=?", (stadiumid,))

    for values in data.db.cursor.fetchall():
        attributes = Attributes()
        attributeid = values[0]
        attributes.year = values[2]
        capacity = list(map(int, values[3:15]))
        attributes.capacity = sum(capacity)
        attributes.stands = list(map(int, values[3:11]))
        attributes.seating = list(map(bool, values[15:23]))
        attributes.roof = list(map(bool, values[23:31]))
        attributes.box = list(map(int, values[11:15]))
        attributes.buildings = list(map(int, values[31:39]))

        stadium.attributes[attributeid] = attributes

        if attributeid > idnumbers.stadiumattrid:
            idnumbers.stadiumattrid = attributeid

    stadiums[stadiumid] = stadium

    if stadiumid > idnumbers.stadiumid:
        idnumbers.stadiumid = stadiumid


positions = ("GK", "DL", "DR", "DC", "D", "ML", "MR", "MC", "M", "AS", "AF")
skill_short = ("KP", "TK", "PS", "SH", "HD", "PC", "ST", "BC", "SP")
skill = ("Keeping",
         "Tackling",
         "Passing",
         "Shooting",
         "Heading",
         "Pace",
         "Stamina",
         "Ball Control",
         "Set Pieces")
