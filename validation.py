#!/usr/bin/env python3

from gi.repository import Gtk

import data
import dialogs
import display
import widgets


class Validate:
    def __init__(self):
        self.cursor = data.db.cursor

        self.results = Results()

    def check(self, player):
        errors = []

        if len(player[1]) < 1:
            errors.append("First Name not long enough")

        if len(player[2]) < 1:
            errors.append("Second Name not long enough")

        if player[5] not in data.clubs.keys():
            errors.append("Member of a non-existent club")

        if player[6] not in data.nations.keys():
            errors.append("Member of a non-existent nation")

        for count, value in enumerate(player[8:17]):
            if value < 1:
                errors.append("%s value lower than 1" % (data.skill[count]))
            elif value > 99:
                errors.append("%s value higher than 99" % (data.skill[count]))

        if player[17] < 1 or player[17] > 10:
            errors.append("Training value out of bounds")

        return errors

    def run(self):
        self.cursor.execute("SELECT * FROM player")

        problems = {}

        for player in self.cursor.fetchall():
            errors = self.check(player)

            if errors != []:
                problems[player[0]] = errors

        if problems != {}:
            self.results.display(problems)
            self.results.hide()
        else:
            dialogs.noerrors()


class Results(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_border_width(5)
        self.set_transient_for(widgets.window)
        self.set_default_size(-1, 180)
        self.set_title("Validation Results")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        textview.set_vexpand(True)
        textview.set_hexpand(True)
        textview.set_editable(False)
        self.textbuffer = textview.get_buffer()
        scrolledwindow.add(textview)

    def display(self, problems):
        text = ""

        for key, item in problems.items():
            player = data.players[key]

            name = display.name(player, mode=1)

            text += "%s (ID %i) has the following validation errors:\n" % (name, key)

            for error in item:
                text += "\t%s\n" % (error)

        self.textbuffer.set_text(text)

        self.show_all()
        self.run()
