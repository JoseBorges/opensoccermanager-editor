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


import data
import structures.attributes


class Stadiums:
    def __init__(self):
        self.stadiums = {}
        self.stadiumid = 0

        self.populate_data()

    def get_stadiumid(self):
        '''
        Return a new player ID.
        '''
        self.stadiumid += 1

        return self.stadiumid

    def get_stadium_by_id(self, stadiumid):
        return self.stadiums[stadiumid]

    def get_stadiums(self):
        return self.stadiums.items()

    def add_stadium(self):
        stadiumid = self.get_stadiumid()
        self.stadiums[stadiumid] = Stadium()

        return stadiumid

    def remove_stadium(self, stadiumid):
        del self.stadiums[stadiumid]

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM stadium")

        for item in data.database.cursor.fetchall():
            stadium = Stadium()
            stadiumid = item[0]
            stadium.name = item[1]
            self.stadiums[stadiumid] = stadium

            data.database.cursor.execute("SELECT * FROM stadiumattr WHERE stadium=?", (stadiumid,))
            stadiumattrs = data.database.cursor.fetchall()

            for value in stadiumattrs:
                attribute = Attribute()
                attributeid = value[0]
                stadium.attributes[attributeid] = attribute

                attribute.year = value[2]

                attribute.main = value[3:7]
                attribute.corner = value[7:11]
                attribute.box = value[11:15]

class Stadium:
    def __init__(self):
        self.name = ""

        self.attributes = {}


class Attribute:
    def __init__(self):
        self.year = 0

        self.main = []
        self.corner = []

    def get_capacity(self):
        capacity = 0

        for value in self.main:
            capacity += value

        for value in self.corner:
            capacity += value

        for value in self.box:
            capacity += value

        return capacity

    def get_building_count(self):
        '''
        Return number of buildings assigned.
        '''
        buildings = 0

        return buildings
