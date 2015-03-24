#!/usr/bin/env python3

import database
import display


db = database.Database()

unsaved = False

years = []
players = {}
clubs = {}
nations = {}
stadiums = {}


class Player:
    pass


class Club:
    pass


class Nation:
    pass


class Stadium:
    pass


class Attributes:
    pass


def player(item):
    player = Player()
    player.playerid = item[0]
    player.first_name = item[1]
    player.second_name = item[2]
    player.common_name = item[3]
    player.date_of_birth = item[4]
    player.nationality = item[5]

    player.attributes = {}

    db.cursor.execute("SELECT * FROM playerattr WHERE player=?", (player.playerid,))

    for data in db.cursor.fetchall():
        attributes = Attributes()
        attributes.attributeid = data[0]
        attributes.year = data[2]

        if not data[3]:
            attributes.club = 0
        else:
            attributes.club = data[3]

        attributes.position = data[4]
        attributes.keeping = data[5]
        attributes.tackling = data[6]
        attributes.passing = data[7]
        attributes.shooting = data[8]
        attributes.heading = data[9]
        attributes.pace = data[10]
        attributes.stamina = data[11]
        attributes.ball_control = data[12]
        attributes.set_pieces = data[13]
        attributes.training_value = data[14]

        player.attributes[attributes.attributeid] = attributes

    players[player.playerid] = player


def club(item):
    club = Club()
    club.clubid = item[0]
    club.name = item[1]
    club.nickname = item[2]

    club.attributes = {}

    db.cursor.execute("SELECT * FROM clubattr WHERE club=?", (club.clubid,))

    for data in db.cursor.fetchall():
        attributes = Attributes()
        attributes.attributeid = data[0]
        attributes.year = data[2]
        attributes.manager = data[3]
        attributes.chairman = data[4]
        attributes.stadium = data[5]
        attributes.reputation = data[6]

        club.attributes[attributes.attributeid] = attributes

    clubs[club.clubid] = club


def nation(item):
    nation = Nation()
    nation.nationid = item[0]
    nation.name = item[1]
    nation.denonym = item[2]
    nations[nation.nationid] = nation


def stadium(item):
    stadium = Stadium()
    stadium.stadiumid = item[0]
    stadium.name = item[1]
    capacity = list(map(int, item[2:14]))
    stadium.capacity = sum(capacity)
    stadium.stands = list(map(int, item[2:10]))
    stadium.seating = list(map(bool, item[14:22]))
    stadium.roof = list(map(bool, item[22:30]))
    stadium.box = list(map(int, item[10:14]))
    stadium.buildings = list(map(int, item[30:38]))
    stadiums[stadium.stadiumid] = stadium


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
