#!/usrsel/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import re
import unicodedata

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
        self.search.searchentry.connect("activate", self.search_activated)
        self.search.searchentry.connect("changed", self.search_changed)
        self.search.searchentry.connect("icon-press", self.search_cleared)
        self.search.treeview.connect("row-activated", self.club_activated)
        self.search.treeselection.connect("changed", self.club_changed)
        self.attach(self.search, 0, 0, 1, 1)

        self.attributes = Attributes()
        self.attach(self.attributes, 1, 0, 1, 1)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if criteria is not "":
            values = {}

            for clubid, club in data.clubs.items():
                for search in (club.name,):
                    search = ''.join((c for c in unicodedata.normalize('NFD', search) if unicodedata.category(c) != 'Mn'))

                    if re.findall(criteria, search, re.IGNORECASE):
                        values[clubid] = club

                        break

            self.populate_data(values)

    def search_changed(self, searchentry):
        if searchentry.get_text() is "":
            self.populate_data(data.clubs)

    def search_cleared(self, searchentry, icon, event):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(data.clubs)

    def club_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()
        self.clubid = model[treepath][0]

        club = data.clubs[self.clubid]
        self.attributes.clubid = self.clubid

        self.attributes.entryName.set_text(club.name)
        self.attributes.entryNickname.set_text(club.nickname)

        self.attributes.populate_attributes()

    def club_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.attributes.set_sensitive(True)
        else:
            self.attributes.set_sensitive(False)

    def populate_data(self, values):
        self.search.clear_data()

        for clubid, club in values.items():
            self.search.liststore.append([clubid, club.name])

    def run(self):
        self.populate_data(values=data.clubs)
        self.show_all()

        treepath = Gtk.TreePath.new_first()
        self.search.treeselection.select_path(treepath)
        column = self.search.treeviewcolumn
        self.search.treeview.row_activated(treepath, column)


class Attributes(Gtk.Grid):
    def __init__(self):
        self.clubid = None

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_sensitive(False)

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(5)
        grid2.set_column_spacing(5)
        self.attach(grid2, 0, 0, 1, 1)

        label = widgets.Label("Name")
        grid2.attach(label, 0, 0, 1, 1)
        self.entryName = Gtk.Entry()
        grid2.attach(self.entryName, 1, 0, 1, 1)

        label = widgets.Label("Nickname")
        grid2.attach(label, 0, 1, 1, 1)
        self.entryNickname = Gtk.Entry()
        grid2.attach(self.entryNickname, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Attributes")
        self.attach(commonframe, 0, 1, 1, 1)

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
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.liststoreAttributes)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeview.connect("row-activated", self.attribute_activated)
        self.treeselectionAttribute = self.treeview.get_selection()
        self.treeselectionAttribute.connect("changed", self.attribute_changed)
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

    def attribute_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonEdit.set_sensitive(True)
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonEdit.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def attribute_activated(self, treeview=None, treepath=None, treeviewcolumn=None):
        model, treeiter = self.treeselectionAttribute.get_selected()

        if treeiter:
            attributeid = model[treeiter][0]

            dialog = AttributeDialog(parent=widgets.window)
            dialog.display(clubid=self.clubid, attributeid=attributeid)

            self.populate_attributes()

    def populate_attributes(self):
        '''
        Populate attribute treeview with values for player id.
        '''
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
