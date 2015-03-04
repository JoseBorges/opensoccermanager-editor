#!/usr/bin/env python3

import data


def name(player, mode=0):
    if player.common_name != "":
        name = player.common_name
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


def club(player):
    if player.club != 0:
        club = data.clubs[player.club].name
    else:
        club = ""

    return club


def nation(player):
    nation = data.nations[player.nationality].name

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
