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


class Nations:
    def __init__(self):
        self.nations = {}
        self.nationid = 0

        self.populate_data()

    def get_nationid(self):
        '''
        Return a new nation ID.
        '''
        self.nationid += 1

        return self.nationid

    def get_nations(self):
        '''
        Return complete dictionary of nations.
        '''
        return self.nations.items()

    def get_nation_by_id(self, nationid):
        '''
        Return nation object for given nation id.
        '''
        return self.nations[nationid]

    def get_nation_count(self):
        '''
        Get number of nations in data structure.
        '''
        return len(self.nations)

    def add_nation(self):
        '''
        Add nation to the data structure.
        '''
        nationid = self.get_nationid()
        self.nations[nationid] = Nation()

        data.unsaved = True

        return nationid

    def remove_nation(self, nationid):
        '''
        Remove nation from data structure.
        '''
        del self.nations[nationid]

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM nation")

        for item in data.database.cursor.fetchall():
            nation = Nation()
            nationid = item[0]
            self.nations[nationid] = nation

            nation.name = item[1]
            nation.denonym = item[2]

            if nationid > self.nationid:
                self.nationid = nationid


class Nation:
    def __init__(self):
        self.name = ""
        self.denonym = ""
