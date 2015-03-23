#!/usr/bin/env python3

from gi.repository import Gtk
import operator

import data
import widgets


class Players(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.liststore = Gtk.ListStore(str, object)
        self.liststore.append(["is greater than", operator.gt])
        self.liststore.append(["is greater than or equal to", operator.ge])
        self.liststore.append(["is less than", operator.lt])
        self.liststore.append(["is less than or equal to", operator.le])

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.Label("Age")
        self.attach(label, 0, 0, 1, 1)
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(self.liststore)
        self.combobox.pack_start(cellrenderertext, True)
        self.combobox.add_attribute(cellrenderertext, "text", 0)
        self.attach(self.combobox, 1, 0, 1, 1)
        self.spinbutton = Gtk.SpinButton.new_with_range(16, 50, 1)
        self.attach(self.spinbutton, 2, 0, 1, 1)

    def get_criteria(self):
        active = self.combobox.get_active()

        comparison = self.liststore[active][1]

        value = self.spinbutton.get_value_as_int()

        return comparison, value

class Clubs(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)


class Nations(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)


class Stadiums(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
