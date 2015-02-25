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


def club(player):
    if player.club != 0:
        club = data.clubs[player.club].name
    else:
        club = ""

    return club


def nation(player):
    nation = data.nations[player.nationality].name

    return nation
