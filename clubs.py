#!/usrsel/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import dialogs
import display
import interface
import menu
import widgets


class Clubs(Gtk.Grid):
    def __init__(self):
        self.selected = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.search = interface.Search()
        self.attach(self.search, 0, 0, 1, 1)

        # Attribute Editor
        gridAttr = Gtk.Grid()
        gridAttr.set_row_spacing(5)
        self.attach(gridAttr, 1, 0, 1, 1)

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        gridAttr.attach(grid2, 0, 0, 1, 1)

        label = widgets.Label("Name")
        grid2.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        grid2.attach(self.entryName, 1, 0, 1, 1)
        label = widgets.Label("Nickname")
        grid2.attach(label, 0, 1, 1, 1)
        self.entryNickname = Gtk.Entry()
        grid2.attach(self.entryNickname, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Attributes")
        gridAttr.attach(commonframe, 0, 1, 1, 1)

        self.liststoreAttributes = Gtk.ListStore(int, int, str, str, str, int)
        cellrenderertext = Gtk.CellRendererText()

        grid3 = Gtk.Grid()
        grid3.set_row_spacing(5)
        grid3.set_column_spacing(5)
        commonframe.insert(grid3)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 120)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        grid3.attach(scrolledwindow, 0, 0, 1, 1)

        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.liststoreAttributes)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        #self.treeview.connect("row-activated", self.attribute_activated)
        self.treeselectionAttribute = self.treeview.get_selection()
        #self.treeselectionAttribute.connect("changed", self.attribute_treeview_changed)
        scrolledwindow.add(self.treeview)
        treeviewcolumn = widgets.TreeViewColumn("Year", column=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Manager", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Chairman", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Stadium", column=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn("Reputation", column=5)
        self.treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonAdd = Gtk.Button.new_from_icon_name("gtk-add", Gtk.IconSize.BUTTON)
        #buttonAdd.connect("clicked", self.add_attribute)
        buttonbox.add(buttonAdd)
        self.buttonEdit = Gtk.Button.new_from_icon_name("gtk-edit", Gtk.IconSize.BUTTON)
        self.buttonEdit.set_sensitive(False)
        #self.buttonEdit.connect("clicked", self.edit_attribute)
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = Gtk.Button.new_from_icon_name("gtk-remove", Gtk.IconSize.BUTTON)
        self.buttonRemove.set_sensitive(False)
        #self.buttonRemove.connect("clicked", self.remove_attribute)
        buttonbox.add(self.buttonRemove)
        grid3.attach(buttonbox, 1, 0, 1, 1)

    def club_activated(self, treeview, path, column):
        model = treeview.get_model()
        self.clubid = model[path][0]

        club = data.clubs[self.clubid]
        self.club = club

        self.entryName.set_text(club.name)
        self.entryNickname.set_text(club.nickname)

        self.populate_attributes()

    def populate_attributes(self):
        self.liststoreAttributes.clear()

        club = data.clubs[self.clubid]

        for attributeid, attribute in club.attributes.items():
            stadium = data.stadiums[attribute.stadium].name

            self.liststoreAttributes.append([attributeid,
                                             attribute.year,
                                             attribute.manager,
                                             attribute.chairman,
                                             stadium,
                                             attribute.reputation
                                             ])

    def row_delete(self, treeview, event=None):
        if event:
            key = Gdk.keyval_name(event.keyval)
        else:
            key = "Delete"

        if key == "Delete":
            if dialogs.remove_dialog(index=1):
                model, treepath = self.treeselection.get_selected_rows()
                clubid = [model[treepath][0] for treepath in treepath]

                keys = [player.club for player in data.players.values()]

                if [item for item in clubid if item in keys]:
                    dialogs.error(0)
                else:
                    for item in clubid:
                        del(data.clubs[item])

                    data.unsaved = True

                    self.populate()

    def selection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.selected = model[treeiter][0]

            widgets.window.menuitemRemove.set_sensitive(True)
            widgets.toolbuttonRemove.set_sensitive(True)
        else:
            self.selected = None

            widgets.window.menuitemRemove.set_sensitive(False)
            widgets.toolbuttonRemove.set_sensitive(False)

    def run(self):
        self.search.data = data.clubs
        self.search.populate_data()
        self.show_all()
