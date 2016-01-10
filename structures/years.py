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


class Years:
    def __init__(self):
        self.years = set()

        self.populate_data()

    def add_year(self, year):
        '''
        Add passed year to list.
        '''
        self.years.add(year)

    def remove_year(self, year):
        '''
        Remove specified year from list.
        '''
        self.years.remove(year)

    def get_years(self):
        '''
        Return list of years in game.
        '''
        return self.years

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM year")

        for item in data.database.cursor.fetchall():
            self.years.add(item[0])

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM year")
        years = [year[0] for year in data.database.cursor.fetchall()]

        for year in data.years.get_years():
            if year not in years:
                data.database.cursor.execute("INSERT INTO year VALUES (?)", (year,))
