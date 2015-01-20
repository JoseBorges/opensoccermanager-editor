#!/usr/bin/env python3

import data


def name(player):
    if player.common_name != "":
        name = player.common_name
    else:
        name = "%s, %s" % (player.second_name, player.first_name)

    return name


def club(player):
    if player.club != 0:
        club = data.clubs[player.club].name
    else:
        club = ""

    return club
