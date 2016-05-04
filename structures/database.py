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


import os

import data


class Database:
    def __init__(self):
        try:
            import sqlite3

            self.initialise(sqlite3, "python-sqlite2")
        except ImportError:
            try:
                import apsw

                self.initialise(apsw, "apsw")
            except ImportError:
                print("Requires python-sqlite3 or apsw for the database.")
                exit()

    def initialise(self, binding, name):
        self.binding = binding
        self.binding.name = name

        self.connection = None
        self.cursor = None

    def connect(self, filepath):
        self.connection = self.binding.Connection(filepath)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = on")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS year (year INTEGER PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS nation (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, denonym TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS referee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS refereeattr (id INTEGER PRIMARY KEY AUTOINCREMENT, referee INTEGER, year INTEGER, league INTEGER, FOREIGN KEY(referee) REFERENCES referee(id), FOREIGN KEY(year) REFERENCES year(year), FOREIGN KEY(league) REFERENCES league(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS league (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS leagueattr (id INTEGER PRIMARY KEY AUTOINCREMENT, league INTEGER, year INTEGER, FOREIGN KEY(league) REFERENCES league(id), FOREIGN KEY(year) REFERENCES year(year))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stadium (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stadiumattr (id, stadium INTEGER, year INTEGER, north INTEGER, east INTEGER, south INTEGER, west INTEGER, northeast INTEGER, northwest INTEGER, southeast INTEGER, southwest INTEGER, northbox INTEGER, eastbox INTEGER, southbox INTEGER, westbox INTEGER, northroof BOOLEAN, eastroof BOOLEAN, southroof BOOLEAN, westroof BOOLEAN, northeastroof BOOLEAN, northwestroof BOOLEAN, southeastroof BOOLEAN, southwestroof BOOLEAN, northseating BOOLEAN, eastseating BOOLEAN, southseating BOOLEAN, westseating BOOLEAN, northeastseating BOOLEAN, northwestseating BOOLEAN, southeastseating BOOLEAN, southwestseating BOOLEAN, stall INTEGER, programme INTEGER, smallshop INTEGER, largeshop INTEGER, bar INTEGER, burgerbar INTEGER, cafe INTEGER, restaurant INTEGER, FOREIGN KEY(stadium) REFERENCES stadium(id), FOREIGN KEY(year) REFERENCES year(year))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, nickname TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS clubattr (id INTEGER PRIMARY KEY AUTOINCREMENT, club INTEGER, year INTEGER, league INTEGER, manager TEXT, chairman TEXT, stadium INTEGER, reputation INTEGER, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(league) REFERENCES league(id), FOREIGN KEY(stadium) REFERENCES stadium(id), FOREIGN KEY(year) REFERENCES year(year))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, commonname TEXT, dateofbirth TEXT, nation INTEGER, FOREIGN KEY(nation) REFERENCES nation(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS playerattr (id INTEGER PRIMARY KEY AUTOINCREMENT, player INTEGER, year INTEGER, club INTEGER, position TEXT, keeping INTEGER, tackling INTEGER, passing INTEGER, shooting INTEGER, heading INTEGER, pace INTEGER, stamina INTEGER, ballcontrol INTEGER, setpieces INTEGER, training INTEGER, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(year) REFERENCES year(year))")

        if self.binding.name == "sqlite3":
            self.connection.commit()

    def save_database(self, *args):
        '''
        Call save data method for each type of data.
        '''
        data.years.save_data()
        data.nations.save_data()
        data.leagues.save_data()
        data.referees.save_data()
        data.stadiums.save_data()
        data.clubs.save_data()
        data.players.save_data()

        if self.binding.name == "sqlite3":
            self.connection.commit()

        data.unsaved = False

    def close(self):
        '''
        Close database connection and clear reference values.
        '''
        self.connection.close()

        self.connection = None
        self.cursor = None
