#!/usr/bin/env python

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

    def connect(self, filename="osm1415.db"):
        if os.path.isfile(filename):
            self.connection = sqlite3.connect(filename)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = on")
        else:
            return False

    def disconnect(self):
        self.connection.close()

    def load(self):
        data.idnumbers.playerid = 0
        data.idnumbers.clubid = 0
        data.idnumbers.nationid = 0
        data.idnumbers.stadiumid = 0

        self.cursor.execute("SELECT * FROM player")

        for item in self.cursor.fetchall():
            player = Player()
            player.playerid = item[0]
            player.first_name = item[1]
            player.second_name = item[2]
            player.common_name = item[3]
            player.date_of_birth = item[4]
            player.club = item[5]
            player.nationality = item[6]
            player.position = item[7]
            player.keeping = item[8]
            player.tackling = item[9]
            player.passing = item[10]
            player.shooting = item[11]
            player.heading = item[12]
            player.pace = item[13]
            player.stamina = item[14]
            player.ball_control = item[15]
            player.set_pieces = item[16]
            player.training_value = item[17]
            data.players[player.playerid] = player

            if player.playerid > data.idnumbers.playerid:
                data.idnumbers.playerid = player.playerid

        self.cursor.execute("SELECT * FROM club")

        for item in self.cursor.fetchall():
            club = Club()
            club.clubid = item[0]
            club.name = item[1]
            club.nickname = item[2]
            club.manager = item[3]
            club.chairman = item[4]
            club.stadium = item[5]
            club.reputation = item[6]
            data.clubs[club.clubid] = club

            if club.clubid > data.idnumbers.clubid:
                data.idnumbers.clubid = club.clubid

        self.cursor.execute("SELECT * FROM nation")

        for item in self.cursor.fetchall():
            nation = Nation()
            nation.nationid = item[0]
            nation.name = item[1]
            nation.denonym = item[2]
            data.nations[nation.nationid] = nation

            if nation.nationid > data.idnumbers.nationid:
                data.idnumbers.nationid = nation.nationid

        self.cursor.execute("SELECT * FROM stadium")

        for item in self.cursor.fetchall():
            stadium = Stadium()
            stadium.stadiumid = item[0]
            stadium.name = item[1]
            stadium.capacity = sum(item[2:14])
            stadium.stands = list(item[2:14])
            stadium.buildings = list(item[30:38])
            data.stadiums[stadium.stadiumid] = stadium

            if stadium.stadiumid > data.idnumbers.stadiumid:
                data.idnumbers.stadiumid = stadium.stadiumid

    def save(self):
        # Player
        results = self.cursor.execute("SELECT * FROM player")
        content = results.fetchall()

        keys = [item[0] for item in content]

        for playerid, player in data.players.items():
            if playerid in keys:
                self.cursor.execute("UPDATE player SET firstname=?, secondname=?, commonname=?, dateofbirth=?, club=?, nation=?, position=?, keeping=?, tackling=?, passing=?, shooting=?, heading=?, pace=?, stamina=?, ballcontrol=?, setpieces=?, training=? WHERE id=?", (player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.training_value, playerid))
            elif playerid not in keys:
                self.cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.training_value))

        for playerid in keys:
            if playerid not in data.players.keys():
                self.cursor.execute("DELETE FROM player WHERE id=?", (playerid,))

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

        self.connection.commit()
