#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import interface
import menu
import widgets


class Stadiums(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.attach(self.search, 0, 0, 1, 1)

    def row_activated(self, treeview=None, treepath=None, treeviewcolumn=None):
        model = treeview.get_model()
        stadiumid = model[treepath][0]

    def row_delete(self, treeview=None, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=3)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                stadiumid = [model[treepath][0] for treepath in treepath]

                keys = [club.stadium for club in data.clubs.values()]

                if [item for item in stadiumid if item in keys]:
                    dialogs.error(2)
                else:
                    for item in stadium:
                        del(data.stadiums[item])

                    data.unsaved = True

                    self.populate()

    def run(self):
        self.search.data = data.stadiums
        self.search.populate_data()
        self.show_all()
