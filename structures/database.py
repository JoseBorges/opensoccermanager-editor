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
import sqlite3

import data


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

    def save_database(self, *args):
        '''
        Call save data method for each type of data.
        '''
        data.years.save_data()
        data.nations.save_data()
        data.referees.save_data()
        data.clubs.save_data()

        self.connection.commit()

        data.unsaved = False

    def close(self):
        '''
        Close database connection and clear reference values.
        '''
        self.connection.close()

        self.connection = None
        self.cursor = None
