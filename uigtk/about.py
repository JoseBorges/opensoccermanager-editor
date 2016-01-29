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
from gi.repository import GdkPixbuf

import data


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, *args):
        logo = data.window.logo.scale_simple(64, 64, GdkPixbuf.InterpType.BILINEAR)

        Gtk.AboutDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_program_name("Editor")
        self.set_comments("Data Editor for OpenSoccerManager")
        self.set_website("http://opensoccermanager.org/")
        self.set_website_label("Website")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo(logo)
        self.set_authors(["Andrew Steele"])
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
