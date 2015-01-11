#!/usr/bin/env python

import database


players = {}
clubs = {}
nations = {}
stadiums = {}


class IDNumbers:
    pass


idnumbers = IDNumbers()
database = database.Database()

skill_short = ("KP", "TK", "PS", "SH", "HD", "PC", "ST", "BC", "SP")
skill = ("Keeping", "Tackling", "Passing", "Shooting", "Heading", "Pace", "Stamina", "Ball Control", "Set Pieces")
