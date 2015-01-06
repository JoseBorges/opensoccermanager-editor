#!/usr/bin/env python

from gi.repository import Gtk


class MenuItem(Gtk.MenuItem):
    def __init__(self, label=""):
        Gtk.MenuItem.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class Label(Gtk.Label):
    def __init__(self, label=""):
        Gtk.Label.__init__(self)
        self.set_label(label)
        self.set_alignment(0, 0.5)


class Button(Gtk.Button):
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)
