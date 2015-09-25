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


import sqlite3
import os

import data


class Database:
    def initialise(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = on")

    def connect(self, filename=""):
        if os.path.isfile(filename):
            self.initialise(filename)

            return True
        elif not os.path.isfile(filename):
            self.initialise(filename)

            self.cursor.execute("CREATE TABLE year (year INTEGER PRIMARY KEY)")

            self.cursor.execute("CREATE TABLE nation (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, denonym TEXT)")

            self.cursor.execute("CREATE TABLE league (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

            self.cursor.execute("CREATE TABLE leagueattr (id INTEGER PRIMARY KEY AUTOINCREMENT, league INTEGER NOT NULL, year INTEGER NOT NULL, FOREIGN KEY(league) REFERENCES league(id), FOREIGN KEY(year) REFERENCES year(year))")

            self.cursor.execute("CREATE TABLE stadium (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

            self.cursor.execute("CREATE TABLE stadiumattr (id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER NOT NULL)")

            self.cursor.execute("CREATE TABLE club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, nickname TEXT)")

            self.cursor.execute("CREATE TABLE clubattr (id INTEGER PRIMARY KEY AUTOINCREMENT, club INTEGER NOT NULL, manager TEXT, chairman TEXT, stadium INTEGER, reputation INTEGER, FOREIGN KEY(stadium) REFERENCES stadium(id), FOREIGN KEY(club) REFERENCES club(id))")

            self.cursor.execute("CREATE TABLE player (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, commonname TEXT, dateofbirth TEXT, nation INTEGER, FOREIGN KEY(nation) REFERENCES nation(id))")

            self.cursor.execute("CREATE TABLE playerattr (id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER NOT NULL, player INTEGER NOT NULL, club INTEGER, position TEXT, keeping INTEGER, tackling INTEGER, passing INTEGER, shooting INTEGER, heading INTEGER, pace INTEGER, stamina INTEGER, ballcontrol INTEGER, setpieces INTEGER, training INTEGER, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id))")

            self.connection.commit()

            return True
        else:
            return False

    def disconnect(self):
        self.connection.close()

    def load(self):
        data.years = []
        data.players = {}
        data.clubs = {}
        data.nations = {}
        data.leagues = {}
        data.stadiums = {}

        self.cursor.execute("SELECT * FROM year")

        for item in self.cursor.fetchall():
            data.years.append(item[0])

        self.cursor.execute("SELECT * FROM player")

        for item in self.cursor.fetchall():
            data.player(item)

        self.cursor.execute("SELECT * FROM club")

        for item in self.cursor.fetchall():
            data.club(item)

        self.cursor.execute("SELECT * FROM league")

        for item in self.cursor.fetchall():
            data.league(item)

        self.cursor.execute("SELECT * FROM nation")

        for item in self.cursor.fetchall():
            data.nation(item)

        self.cursor.execute("SELECT * FROM stadium")

        for item in self.cursor.fetchall():
            data.stadium(item)

    def save(self):
        # Year
        for year in data.years:
            try:
                self.cursor.execute("INSERT INTO year VALUES (?)", (year,))
            except sqlite3.IntegrityError:
                pass

        # Nation
        results = self.cursor.execute("SELECT * FROM nation")
        content = results.fetchall()

        keys = (item[0] for item in content)

        for nationid, nation in data.nations.items():
            if nationid in keys:
                self.cursor.execute("UPDATE nation SET name=?, denonym=? WHERE id=?", (nation.name, nation.denonym, nationid))
            elif nationid not in keys:
                self.cursor.execute("INSERT INTO nation VALUES (?, ?, ?)", (nationid, nation.name, nation.denonym))

        for nationid in keys:
            if nationid not in data.nations.keys():
                self.cursor.execute("DELETE FROM nation WHERE id=?", (nationid,))

        # Stadium
        results = self.cursor.execute("SELECT * FROM stadium")
        content = results.fetchall()

        keys = (item[0] for item in content)

        for stadiumid, stadium in data.stadiums.items():
            if stadiumid in keys:
                self.cursor.execute("UPDATE stadium SET name=? WHERE id=?", (stadium.name, stadiumid))
            elif stadiumid not in keys:
                self.cursor.execute("INSERT INTO stadium VALUES (?, ?)", (stadiumid, stadium.name))

        for stadiumid in keys:
            if stadiumid not in data.stadiums.keys():
                self.cursor.execute("DELETE FROM stadium WHERE id=?", (stadiumid,))

        # Club
        results = self.cursor.execute("SELECT * FROM club")
        content = results.fetchall()

        keys = (item[0] for item in content)

        for clubid, club in data.clubs.items():
            if clubid in keys:
                self.cursor.execute("UPDATE club SET name=?, nickname=? WHERE id=?", (club.name, club.nickname, clubid))
            elif clubid not in keys:
                self.cursor.execute("INSERT INTO club VALUES (?, ?, ?)", (clubid, club.name, club.nickname))

        for clubid in keys:
            if clubid not in data.clubs.keys():
                self.cursor.execute("DELETE FROM club WHERE id=?", (clubid,))

        # Player
        results = self.cursor.execute("SELECT * FROM player")
        content = results.fetchall()

        player_keys = (item[0] for item in content)

        for playerid, player in data.players.items():
            if playerid in player_keys:
                self.cursor.execute("UPDATE player SET firstname=?, secondname=?, commonname=?, dateofbirth=?, nation=? WHERE id=?", (player.first_name, player.second_name, player.common_name, player.date_of_birth, player.nationality, playerid))

                for attributeid, attribute in player.attributes.items():
                    self.cursor.execute("UPDATE playerattr SET player=?, year=?, club=?, position=?, keeping=?, tackling=?, passing=?, shooting=?, heading=?, pace=?, stamina=?, ballcontrol=?, setpieces=?, training=? WHERE id=?", (playerid, attribute.year, attribute.club, attribute.position, attribute.keeping, attribute.tackling, attribute.passing, attribute.shooting, attribute.heading, attribute.pace, attribute.stamina, attribute.ball_control, attribute.set_pieces, attribute.training_value, attributeid))
            elif playerid not in player_keys:
                self.cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?)", (playerid, player.first_name, player.second_name, player.common_name, player.date_of_birth, player.nationality))

        for playerid in player_keys:
            if playerid not in data.players.keys():
                self.cursor.execute("DELETE FROM player WHERE id=?", (playerid,))

        self.connection.commit()
