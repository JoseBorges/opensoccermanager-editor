#!/usr/bin/env python3

from gi.repository import Gtk

import data
import widgets


class Players(Gtk.Grid):
    class Specification(Gtk.Grid):
        def __init__(self):
            self.comparison = {"0": ("First Name", Gtk.Entry()),
                               "1": ("Second Name", Gtk.Entry()),
                               "2": ("Common Name", Gtk.Entry()),
                               "3": ("Date Of Birth", Gtk.Button()),
                               "4": ("Age", Gtk.SpinButton()),
                               "5": ("Club", Gtk.ComboBox()),
                               "6": ("Nationality", Gtk.ComboBox()),
                              }

            self.criteria = None

            Gtk.Grid.__init__(self)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            liststore = Gtk.ListStore(str, str)
            treemodelsort = Gtk.TreeModelSort(liststore)
            treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)
            cellrenderertext = Gtk.CellRendererText()

            self.comboboxCriteria = Gtk.ComboBox()
            self.comboboxCriteria.set_model(treemodelsort)
            self.comboboxCriteria.set_id_column(0)
            self.comboboxCriteria.pack_start(cellrenderertext, True)
            self.comboboxCriteria.add_attribute(cellrenderertext, "text", 1)

            for key, item in self.comparison.items():
                liststore.append([key, item[0]])

            self.comboboxCriteria.connect("changed", self.criteria_changed)
            self.comboboxCriteria.set_active(0)
            self.attach(self.comboboxCriteria, 0, 0, 1, 1)

            self.comboboxCompare = Gtk.ComboBoxText()
            self.attach(self.comboboxCompare, 1, 0, 1, 1)

        def criteria_changed(self, combobox):
            active = combobox.get_active_id()

            if self.criteria:
                self.criteria.destroy()

            self.criteria = self.comparison[active][1]
            self.attach(self.criteria, 2, 0, 1, 1)

            self.show_all()

    def __init__(self):
        self.spec_id = 0
        self.specifications = {}

        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.buttonAdd = widgets.Button("_Add")
        self.buttonAdd.connect("clicked", self.add_button_clicked)
        self.attach(self.buttonAdd, 0, 0, 1, 1)

    def add_button_clicked(self, button):
        specification = self.Specification()

        position = len(self.specifications) + 1
        self.attach(specification, 0, position, 3, 1)

        buttonRemove = widgets.Button("_Remove")
        buttonRemove.connect("clicked", self.remove_button_clicked, self.spec_id)
        self.attach(buttonRemove, 4, position, 1, 1)

        self.specifications[self.spec_id] = specification
        self.spec_id += 1

        self.show_all()

    def remove_button_clicked(self, button, spec_id):
        self.specifications[spec_id].destroy()
        button.destroy()

        del(self.specifications[spec_id])

        self.buttonAdd.set_sensitive(True)

    def get_criteria(self):
        '''
        first_name = self.entryFirstName.get_text()
        second_name = self.entrySecondName.get_text()
        common_name = self.entryCommonName.get_text()

        if self.comboboxClub.get_active_id():
            club = int(self.comboboxClub.get_active_id())
        else:
            club = None

        if self.comboboxNation.get_active_id():
            nation = int(self.comboboxNation.get_active_id())
        else:
            nation = None

        criteria = {"FirstName": first_name,
                    "SecondName": second_name,
                    "CommonName": common_name,
                    "Club": club,
                    "Nation": nation,
                   }
        '''
        return criteria


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
