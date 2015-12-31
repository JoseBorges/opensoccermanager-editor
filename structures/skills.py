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


class Skills:
    def __init__(self):
        self.skills = (("Keeping", "KP"),
                       ("Tackling", "TK"),
                       ("Passing", "PS"),
                       ("Shooting", "SH"),
                       ("Heading", "HD"),
                       ("Pace", "PC"),
                       ("Stamina", "ST"),
                       ("Ball Control", "BC"),
                       ("Set Pieces", "SP"))

    def get_short_skills(self):
        '''
        Return list of shortened skill names.
        '''
        skills = [skill[1] for skill in self.skills]

        return skills

    def get_skills(self):
        '''
        Return list of full skill names.
        '''
        skills = [skill[0] for skill in self.skills]

        return skills
