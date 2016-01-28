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


class Names:
    def __init__(self):
        self.names = ("North",
                      "East",
                      "South",
                      "West",
                      "North East",
                      "South East",
                      "South West",
                      "North West")

    def get_names(self):
        '''
        Return tuple of stadium stand names.
        '''
        return self.names


class Stadiums:
    def __init__(self):
        self.stadiums = {}
        self.stadiumid = 0

        self.deletions = []

        self.populate_data()

    def get_stadiumid(self):
        '''
        Return a new player ID.
        '''
        self.stadiumid += 1

        return self.stadiumid

    def get_stadiums(self):
        '''
        Return complete dictionary of stadiums.
        '''
        return self.stadiums.items()

    def get_stadium_by_id(self, stadiumid):
        '''
        Return stadium object for given stadium id.
        '''
        return self.stadiums[stadiumid]

    def get_stadium_count(self):
        '''
        Get number of stadiums in data structure.
        '''
        return len(self.stadiums)

    def add_stadium(self):
        '''
        Add stadium to data structure.
        '''
        stadiumid = self.get_stadiumid()
        self.stadiums[stadiumid] = Stadium()

        data.unsaved = True

        return stadiumid

    def remove_stadium(self, stadiumid):
        '''
        Remove stadium from data structure.
        '''
        del self.stadiums[stadiumid]
        self.deletions.append(stadiumid)

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

            if stadiumid > self.stadiumid:
                self.stadiumid = stadiumid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM stadium")
        stadiums = [stadium[0] for stadium in data.database.cursor.fetchall()]

        for stadiumid, stadium in self.stadiums.items():
            if stadiumid in stadiums:
                data.database.cursor.execute("UPDATE stadium SET name=? WHERE id=?", (stadium.name, stadiumid))
            else:
                data.database.cursor.execute("INSERT INTO stadium VALUES (null, ?)", (stadium.name))

        for stadiumid in stadiums:
            if stadiumid in self.deletions:
                data.database.cursor.execute("DELETE FROM stadium WHERE id=?", (stadiumid,))

        self.deletions.clear()


class Stadium:
    def __init__(self):
        self.name = ""

        self.attributes = {}
        self.attributeid = 0

    def get_attributeid(self):
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute()

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        del self.attributes[attributeid]

        data.unsaved = True

    def can_remove(self):
        '''
        Return whether stadium can be removed from data set.
        '''
        return self.attributes == {}


class Attribute(structures.attributes.Attribute):
    def __init__(self):
        structures.attributes.Attribute.__init__(self)

        self.main = []
        self.corner = []

    def get_capacity(self):
        '''
        Return total stadium capacity.
        '''
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
