#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager-Editor is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager-Editor is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager-Editor.  If not, see <http://www.gnu.org/licenses/>.


import data


def name(player, mode=0):
    if player.common_name != "":
        name = player.common_name
    elif player.first_name == "" and player.second_name == "":
        name = ""
    else:
        if mode == 0:
            name = "%s, %s" % (player.second_name, player.first_name)
        elif mode == 1:
            name = "%s %s" % (player.first_name, player.second_name)

    return name


def age(date_of_birth):
    year, month, day = list(map(int, date_of_birth.split("-")))
    age = data.season - year

    if (month, day) > (8, 1):
        age -= 1

    return age


def club(clubid):
    if clubid:
        club = data.clubs[clubid].name
    else:
        club = "Free Agent"

    return club


def nation(nationid):
    if nationid:
        nation = data.nations[nationid].name
    else:
        nation = ""

    return nation


def value(value):
    currency = "£"

    if value >= 1000000:
        amount = (value / 1000000)
        value = "%s%.1fM" % (currency, amount)
    elif value >= 1000:
        amount = (value / 1000)
        value = "%s%iK" % (currency, amount)

    return value


def wage(wage):
    currency = "£"

    if wage >= 1000:
        amount = (wage / 1000)
        wage = "%s%.1fK" % (currency, amount)
    elif wage >= 100:
        amount = wage
        wage = "%s%i" % (currency, amount)

    return wage
