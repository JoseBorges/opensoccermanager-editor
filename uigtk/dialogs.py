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

import data


class RemoveItem(Gtk.MessageDialog):
    '''
    Message dialog displayed to confirm removal of item.
    '''
    def __init__(self, item, value):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Remove %s" % (item))
        self.set_markup("Remove %s from database?" % (value))
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Do Not Remove", Gtk.ResponseType.CANCEL)
        self.add_button("_Remove", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class RemoveAttribute(Gtk.MessageDialog):
    '''
    Message dialog displayed to confirm removal of attribute.
    '''
    def __init__(self, index=0):
        item = ["player", "club", "stadium"][index]

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Remove Attribute")
        self.set_markup("Remove selected attribute from %s?" % (item))
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Do Not Remove", Gtk.ResponseType.CANCEL)
        self.add_button("_Remove", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class ClubKeyError(Gtk.MessageDialog):
    def __init__(self, item):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Key Error")
        self.set_markup("<span size='12000'><b>Unable to remove %s from the database.</b></span>" % (item))
        self.format_secondary_markup("Remove all associated players from the club to delete.")
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()
