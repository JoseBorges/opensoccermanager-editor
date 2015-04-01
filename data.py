#!/usr/bin/env python3

import data
import display


unsaved = False

years = []
players = {}
clubs = {}
nations = {}
stadiums = {}


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
        self.attributes = {}


class Nation:
    pass


class Stadium:
    pass


class Attributes:
    pass


class IDNumbers:
    playerid = 0
    playerattrid = 0

    def request_playerid(self):
        self.playerid += 1

        return self.playerid

    def request_playerattrid(self):
        self.playerattrid += 1

        return self.playerattrid


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
        attributes.attributeid = values[0]
        attributes.year = values[2]
        attributes.manager = values[3]
        attributes.chairman = values[4]
        attributes.stadium = values[5]
        attributes.reputation = values[6]

        club.attributes[attributes.attributeid] = attributes

    clubs[clubid] = club


def nation(item):
    nation = Nation()
    nationid = item[0]
    nation.name = item[1]
    nation.denonym = item[2]
    nations[nationid] = nation


def stadium(item):
    stadium = Stadium()
    stadiumid = item[0]
    stadium.name = item[1]
    capacity = list(map(int, item[2:14]))
    stadium.capacity = sum(capacity)
    stadium.stands = list(map(int, item[2:10]))
    stadium.seating = list(map(bool, item[14:22]))
    stadium.roof = list(map(bool, item[22:30]))
    stadium.box = list(map(int, item[10:14]))
    stadium.buildings = list(map(int, item[30:38]))
    stadiums[stadiumid] = stadium


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
