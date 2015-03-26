#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import interface
import menu
import widgets


class Nations(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.attach(self.search, 0, 0, 1, 1)

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        nationid = model[path][0]

    def row_delete(self, treeview, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if data.options.confirm_remove:
                state = dialogs.remove_dialog(index=2)
            else:
                state = True

            if state:
                model, treepath = self.treeselection.get_selected_rows()
                nationid = [model[treepath][0] for treepath in treepath]

                keys = [player.nationality for player in data.players.values()]

                if [item for item in nationid if item in keys]:
                    dialogs.error(1)
                else:
                    for item in nationid:
                        del(data.nations[item])

                    data.unsaved = True

                    self.populate()

    def populate_data(self):
        self.search.clear_data()

        for nationid, nation in data.nations.items():
            self.search.liststore.append([nationid, nation.name])

    def run(self):
        self.populate_data()
        self.show_all()
