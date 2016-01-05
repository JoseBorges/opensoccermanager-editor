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


class Referees:
    class Referee:
        def __init__(self, refereeid):
            self.refereeid = refereeid
            self.name = ""

    def __init__(self):
        self.referees = {}
        self.refereeid = 0

        self.populate_data()

    def get_refereeid(self):
        '''
        Return a new referee id.
        '''
        self.refereeid += 1

        return self.refereeid

    def get_referees(self):
        '''
        Return complete dictionary of referees.
        '''
        return self.referees.items()

    def get_referee_by_id(self, refereeid):
        '''
        Return referee for given referee id.
        '''
        return self.referees[refereeid]

    def get_referee_count(self):
        '''
        Get number of referees in data structure.
        '''
        return len(self.referees)

    def add_referee(self):
        '''
        Add referee to the data structure.
        '''
        refereeid = self.get_refereeid()
        self.referees[refereeid] = self.Referee(refereeid)

        return refereeid

    def remove_referee(self, refereeid):
        '''
        Remove referee from data structure.
        '''
        del self.referees[refereeid]

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM referee")

        for item in data.database.cursor.fetchall():
            refereeid = item[0]
            referee = self.Referee(refereeid)
            referee.name = item[1]
            self.referees[refereeid] = referee

            if refereeid > self.refereeid:
                self.refereeid = refereeid
