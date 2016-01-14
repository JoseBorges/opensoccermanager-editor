#!/usr/bin/env python3

#  This file is part of OpenSoccerManager-Editor.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk


class Grid(Gtk.Grid):
    '''
    Grid with assigned row and column spacing.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)


class Label(Gtk.Label):
    def __init__(self, label="", leftalign=False):
        Gtk.Label.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)
        self.set_use_markup(True)

        if leftalign:
            self.set_alignment(0, 0.5)


class Button(Gtk.Button):
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CheckButton(Gtk.CheckButton):
    def __init__(self, label=""):
        Gtk.CheckButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class RadioButton(Gtk.RadioButton):
    def __init__(self, label=""):
        Gtk.RadioButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class ToolButton(Gtk.ToolButton):
    def __init__(self, label=""):
        Gtk.ToolButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class MenuItem(Gtk.MenuItem):
    def __init__(self, label=""):
        Gtk.MenuItem.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CommonFrame(Gtk.Frame):
    '''
    Tidy frame widget for use in dialogs to group widgets.
    '''
    def __init__(self, title=""):
        Gtk.Frame.__init__(self)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        self.label = Gtk.Label("<b>%s</b>" % (title))
        self.label.set_use_markup(True)
        self.set_label_widget(self.label)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_property("margin-left", 12)
        self.grid.set_property("margin-top", 5)
        self.add(self.grid)

    def set_title(self, title):
        self.label.set_label("<b>%s</b>" % (title))


class TreeView(Gtk.TreeView):
    '''
    Treeview with search function pre-disabled.
    '''
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_enable_search(False)
        self.set_search_column(-1)

        self.treeselection = self.get_selection()


class TreeViewColumn(Gtk.TreeViewColumn):
    '''
    Column setting model column and title.
    '''
    def __init__(self, title="", column=0):
        Gtk.TreeViewColumn.__init__(self)

        cellrenderertext = Gtk.CellRendererText()
        self.pack_start(cellrenderertext, False)
        self.add_attribute(cellrenderertext, "text", column)

        if title:
            self.set_title(title)


class ScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


class ButtonBox(Gtk.ButtonBox):
    def __init__(self):
        Gtk.ButtonBox.__init__(self)
        self.set_spacing(5)
