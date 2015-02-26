#!/usr/bin/env python3

import sqlite3
import os

import data


class Player:
    pass


class Club:
    pass


class Nation:
    pass


class Stadium:
    pass


class Database:
    connection = None
    cursor = None

    def initialise(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = on")

    def connect(self, filename="osm1415.db"):
        if os.path.isfile(filename):
            self.initialise(filename)
        elif not os.path.isfile(filename):
            self.initialise(filename)

            self.cursor.execute("CREATE TABLE about (year INTEGER, version INTEGER)")
            self.cursor.execute("INSERT INTO about VALUES (?, ?)", (data.season, 1))

            self.cursor.execute("CREATE TABLE stadium (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, north INTEGER, east INTEGER, south INTEGER, west INTEGER, northeast INTEGER, northwest INTEGER, southeast INTEGER, southwest INTEGER, northbox INTEGER, eastbox INTEGER, southbox INTEGER, westbox INTEGER, northroof BOOLEAN, eastroof BOOLEAN, southroof BOOLEAN, westroof BOOLEAN, northeastroof BOOLEAN, northwestroof BOOLEAN, southeastroof BOOLEAN, southwestroof BOOLEAN, northseating BOOLEAN, eastseating BOOLEAN, southseating BOOLEAN, westseating BOOLEAN, northeastseating BOOLEAN, northwestseating BOOLEAN, southeastseating BOOLEAN, southwestseating BOOLEAN, stall INTEGER, programme INTEGER, smallshop INTEGER, largeshop INTEGER, bar INTEGER, burgerbar INTEGER, cafe INTEGER, restaurant INTEGER)")
            self.cursor.execute("CREATE TABLE nation (id INTEGER PRIMARY KEY AUTOINCREMENT, nation TEXT, denonym TEXT)")
            self.cursor.execute("CREATE TABLE club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, nickname TEXT, manager TEXT, chairman TEXT, stadium INTEGER, reputation INTEGER, FOREIGN KEY(stadium) REFERENCES stadium(id))")
            self.cursor.execute("CREATE TABLE player (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, commonname TEXT, dateofbirth TEXT, club INTEGER, nation INTEGER, position TEXT, keeping INTEGER, tackling INTEGER, passing INTEGER, shooting INTEGER, heading INTEGER, pace INTEGER, stamina INTEGER, ballcontrol INTEGER, setpieces INTEGER, training INTEGER, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(nation) REFERENCES nation(id))")

            self.connection.commit()
        else:
            return False

    def disconnect(self):
        self.connection.close()

    def initialise_ids(self):
        data.idnumbers.playerid = 0
        data.idnumbers.clubid = 0
        data.idnumbers.nationid = 0
        data.idnumbers.stadiumid = 0

    def load(self):
        self.initialise_ids()

        data.players = {}
        data.clubs = {}
        data.nations = {}
        data.stadiums = {}

        self.cursor.execute("SELECT * FROM about")

        data.season, data.version = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM player")

        for item in self.cursor.fetchall():
            data.player(item)

        self.cursor.execute("SELECT * FROM club")

        for item in self.cursor.fetchall():
            data.club(item)

        self.cursor.execute("SELECT * FROM nation")

        for item in self.cursor.fetchall():
            data.nation(item)

        self.cursor.execute("SELECT * FROM stadium")

        for item in self.cursor.fetchall():
            data.stadium(item)

    def save(self):
        # Nation
        results = self.cursor.execute("SELECT * FROM nation")
        content = results.fetchall()

        keys = [item[0] for item in content]

        for nationid, nation in data.nations.items():
            if nationid in keys:
                self.cursor.execute("UPDATE nation SET nation=?, denonym=? WHERE id=?", (nation.name, nation.denonym, nationid))
            elif nationid not in keys:
                self.cursor.execute("INSERT INTO nation VALUES (?, ?, ?)", (nationid, nation.name, nation.denonym))

        for nationid in keys:
            if nationid not in data.nations.keys():
                self.cursor.execute("DELETE FROM nation WHERE id=?", (nationid,))

        # Stadium
        results = self.cursor.execute("SELECT * FROM stadium")
        content = results.fetchall()

        keys = [item[0] for item in content]

        for stadiumid, stadium in data.stadiums.items():
            north, east, south, west, northeast, northwest, southeast, southwest = stadium.stands
            northseating, eastseating, southseating, westseating, northeastseating, northwestseating, southeastseating, southwestseating = stadium.seating
            northroof, eastroof, southroof, westroof, northeastroof, northwestroof, southeastroof, southwestroof = stadium.roof
            northbox, eastbox, southbox, westbox = stadium.box
            stall, programme, smallshop, largeshop, bar, burgerbar, cafe, restaurant = stadium.buildings

            if stadiumid in keys:
                self.cursor.execute("UPDATE stadium SET name=?, north=?, east=?, south=?, west=?, northeast=?, northwest=?, southeast=?, southwest=?, northbox=?, eastbox=?, southbox=?, westbox=?, northroof=?, eastroof=?, southroof=?, westroof=?, northeastroof=?, northwestroof=?, southeastroof=?, southwestroof=?, northseating=?, eastseating=?, southseating=?, westseating=?, northeastseating=?, northwestseating=?, southeastseating=?, southwestseating=?, stall=?, programme=?, smallshop=?, largeshop=?, bar=?, burgerbar=?, cafe=?, restaurant=? WHERE id=?", (stadium.name, north, east, south, west, northeast, northwest, southeast, southwest, northbox, eastbox, southbox, westbox, northseating, eastseating, southseating, westseating, northeastseating, northwestseating, southeastseating, southwestseating, northroof, eastroof, southroof, westroof, northeastroof, northwestroof, southeastroof, southwestroof, stall, programme, smallshop, largeshop, bar, burgerbar, cafe, restaurant, stadiumid))
            elif stadiumid not in keys:
                self.cursor.execute("INSERT INTO stadium VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (stadiumid, stadium.name, north, east, south, west, northeast, northwest, southeast, southwest, northbox, eastbox, southbox, westbox, northseating, eastseating, southseating, westseating, northeastseating, northwestseating, southeastseating, southwestseating, northroof, eastroof, southroof, westroof, northeastroof, northwestroof, southeastroof, southwestroof, stall, programme, smallshop, largeshop, bar, burgerbar, cafe, restaurant))

        for stadiumid in keys:
            if stadiumid not in data.stadiums.keys():
                self.cursor.execute("DELETE FROM stadium WHERE id=?", (stadiumid,))

        # Club
        results = self.cursor.execute("SELECT * FROM club")
        content = results.fetchall()

        keys = [item[0] for item in content]

        for clubid, club in data.clubs.items():
            if clubid in keys:
                self.cursor.execute("UPDATE club SET name=?, nickname=?, manager=?, chairman=?, stadium=?, reputation=? WHERE id=?", (club.name, club.nickname, club.manager, club.chairman, club.stadium, club.reputation, clubid))
            elif clubid not in keys:
                self.cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?, ?, ?, ?)", (clubid, club.name, club.nickname, club.manager, club.chairman, club.stadium, club.reputation))

        for clubid in keys:
            if clubid not in data.clubs.keys():
                self.cursor.execute("DELETE FROM club WHERE id=?", (clubid,))

        # Player
        results = self.cursor.execute("SELECT * FROM player")
        content = results.fetchall()

        keys = [item[0] for item in content]

        for playerid, player in data.players.items():
            if player.club == 0:
                player.club = None

            if playerid in keys:
                self.cursor.execute("UPDATE player SET firstname=?, secondname=?, commonname=?, dateofbirth=?, club=?, nation=?, position=?, keeping=?, tackling=?, passing=?, shooting=?, heading=?, pace=?, stamina=?, ballcontrol=?, setpieces=?, training=? WHERE id=?", (player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.training_value, playerid))
            elif playerid not in keys:
                self.cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.training_value))

        for playerid in keys:
            if playerid not in data.players.keys():
                self.cursor.execute("DELETE FROM player WHERE id=?", (playerid,))

        self.connection.commit()
