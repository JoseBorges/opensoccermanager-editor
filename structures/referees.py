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


class Referees:
    def __init__(self):
        self.referees = {}
        self.refereeid = 0

        self.deletions = []

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
        referee = Referee(refereeid)
        self.referees[refereeid] = referee

        data.unsaved = True

        return referee

    def remove_referee(self, refereeid):
        '''
        Remove referee from data structure.
        '''
        del self.referees[refereeid]
        self.deletions.append(refereeid)

        data.unsaved = True

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM referee")

        for item in data.database.cursor.fetchall():
            referee = Referee(item[0])
            self.referees[referee.refereeid] = referee

            referee.name = item[1]

            data.database.cursor.execute("SELECT * FROM refereeattr WHERE referee=?", (referee.refereeid,))
            refereeattrs = data.database.cursor.fetchall()

            for value in refereeattrs:
                attribute = structures.attributes.Attribute()
                attributeid = value[0]
                attribute.year = value[2]
                attribute.league = value[3]
                referee.attributes[attributeid] = attribute

                if attributeid > referee.attributeid:
                    referee.attributeid = attributeid

            if referee.refereeid > self.refereeid:
                self.refereeid = referee.refereeid

    def save_data(self):
        data.database.cursor.execute("SELECT * FROM referee")
        referees = [referee[0] for referee in data.database.cursor.fetchall()]

        for refereeid, referee in self.referees.items():
            if refereeid in referees:
                data.database.cursor.execute("UPDATE referee SET name=? WHERE id=?", (referee.name, refereeid))
            else:
                data.database.cursor.execute("INSERT INTO referee VALUES (null, ?)", (referee.name,))

            data.database.cursor.execute("SELECT * FROM refereeattr WHERE referee=?", (refereeid,))
            attributes = [attribute[0] for attribute in data.database.cursor.fetchall()]

            for attributeid, attribute in referee.attributes.items():
                if attributeid in attributes:
                    data.database.cursor.execute("UPDATE refereeattr SET referee=?, year=?, league=? WHERE id=?", (refereeid, attribute.year, attribute.league, attributeid))
                else:
                    data.database.cursor.execute("INSERT INTO refereeattr VALUES (null, ?, ?, ?)", (refereeid, attribute.year, attribute.league))

        for refereeid in referees:
            if refereeid in self.deletions:
                data.database.cursor.execute("DELETE FROM referee WHERE id=?", (refereeid,))

        self.deletions.clear()


class Referee:
    def __init__(self, refereeid):
        self.refereeid = refereeid
        self.name = ""

        self.attributes = {}
        self.attributeid = 0

    def get_attributeid(self):
        '''
        Return a new referee attribute id.
        '''
        self.attributeid += 1

        return self.attributeid

    def add_attribute(self):
        '''
        Add referee attribute to data structure.
        '''
        attributeid = self.get_attributeid()
        self.attributes[attributeid] = Attribute(self.refereeid)

        data.unsaved = True

        return attributeid

    def remove_attribute(self, attributeid):
        '''
        Remove referee attribute from data structure.
        '''
        del self.attributes[attributeid]

        data.unsaved = True


class Attribute(structures.attributes.Attribute):
    def __init__(self, refereeid):
        structures.attributes.Attribute.__init__(self)

        self.refereeid = refereeid
        self.league = None
