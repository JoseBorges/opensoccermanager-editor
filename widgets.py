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
