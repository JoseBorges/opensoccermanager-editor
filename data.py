#!/usr/bin/env python3

import database


unsaved = False

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


class IDNumbers:
    playerid = 0
    clubid = 0
    nationid = 0
    stadiumid = 0


idnumbers = IDNumbers()
database = database.Database()


def player(item):
    player = Player()
    player.playerid = int(item[0])
    player.first_name = item[1]
    player.second_name = item[2]
    player.common_name = item[3]
    player.date_of_birth = item[4]

    if item[5] is None:
        player.club = 0
    else:
        player.club = int(item[5])

    player.nationality = int(item[6])
    player.position = (item[7])
    player.keeping = (item[8])
    player.tackling = (item[9])
    player.passing = (item[10])
    player.shooting = (item[11])
    player.heading = (item[12])
    player.pace = (item[13])
    player.stamina = (item[14])
    player.ball_control = (item[15])
    player.set_pieces = (item[16])
    player.training_value = (item[17])
    players[player.playerid] = player

    if player.playerid > idnumbers.playerid:
        idnumbers.playerid = player.playerid


def club(item):
    club = Club()
    club.clubid = int(item[0])
    club.name = item[1]
    club.nickname = item[2]
    club.manager = item[3]
    club.chairman = item[4]
    club.stadium = int(item[5])
    club.reputation = int(item[6])
    clubs[club.clubid] = club

    if club.clubid > idnumbers.clubid:
        idnumbers.clubid = club.clubid


def nation(item):
    nation = Nation()
    nation.nationid = int(item[0])
    nation.name = item[1]
    nation.denonym = item[2]
    nations[nation.nationid] = nation

    if nation.nationid > idnumbers.nationid:
        idnumbers.nationid = nation.nationid


def stadium(item):
    stadium = Stadium()
    stadium.stadiumid = int(item[0])
    stadium.name = item[1]
    capacity = list(map(int, item[2:14]))
    stadium.capacity = sum(capacity)
    stadium.stands = capacity
    stadium.seating = list(map(bool, item[14:22]))
    stadium.roof = list(map(bool, item[22:30]))
    stadium.buildings = list(map(int, item[30:38]))
    stadiums[stadium.stadiumid] = stadium

    if stadium.stadiumid > idnumbers.stadiumid:
        idnumbers.stadiumid = stadium.stadiumid


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
