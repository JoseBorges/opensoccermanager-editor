#!/usr/bin/env python3

import database


unsaved = False

players = {}
clubs = {}
nations = {}
stadiums = {}


class IDNumbers:
    pass


idnumbers = IDNumbers()
database = database.Database()

skill_short = ("KP", "TK", "PS", "SH", "HD", "PC", "ST", "BC", "SP")
skill = ("Keeping",
         "Tackling",
         "Passing",
         "Shooting",
         "Heading",
         "Pace",
         "Stamina",
         "Ball Control",
         "Set Pieces")

positions = ("GK", "DL", "DR", "DC", "D", "ML", "MR", "MC", "M", "AS", "AF")
