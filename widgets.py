#!/usr/bin/env python3

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
        self.set_use_underline(True)


class Button(Gtk.Button):
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CommonFrame(Gtk.Frame):
    '''
    Tidy frame widget for use in dialogs to group widgets.
    '''
    def __init__(self, title=None):
        Gtk.Frame.__init__(self)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        label = Gtk.Label("<b>%s</b>" % (title))
        label.set_use_markup(True)
        self.set_label_widget(label)

        self.grid = Gtk.Grid()
        self.grid.set_property("margin-left", 12)
        self.grid.set_property("margin-top", 5)
        self.add(self.grid)

    def insert(self, child):
        self.grid.attach(child, 0, 0, 1, 1)


class TreeViewColumn(Gtk.TreeViewColumn):
    '''
    Column setting model column and title.
    '''
    def __init__(self, title="", column=0):
        Gtk.TreeViewColumn.__init__(self)

        cellrenderertext = Gtk.CellRendererText()

        if title:
            self.set_title(title)

        self.pack_start(cellrenderertext, False)
        self.add_attribute(cellrenderertext, "text", column)
