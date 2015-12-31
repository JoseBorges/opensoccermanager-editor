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


import sqlite3
import os

class Database:
    def __init__(self, filepath):
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = on")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS year (year INTEGER PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS referee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS nation (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, denonym TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS league (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stadium (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, nickname TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, commonname TEXT, dateofbirth TEXT, nation INTEGER, FOREIGN KEY(nation) REFERENCES nation(id))")

        self.connection.commit()

    def close(self):
        self.connection.close()

        self.connection = None
        self.cursor = None
