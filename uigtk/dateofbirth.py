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


class DateOfBirth(Gtk.Dialog):
    def __init__(self):
        self.date_of_birth = None

        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_resizable(False)
        self.set_title("Select Date Of Birth")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)

        self.calendar = Gtk.Calendar()
        self.calendar.set_property("year", True)
        self.calendar.connect("day-selected-double-click", self.on_calendar_clicked)
        self.vbox.add(self.calendar)

    def on_calendar_clicked(self, calendar):
        '''
        Emit response for double-click on calendar date.
        '''
        self.response(Gtk.ResponseType.OK)

    def get_date_of_birth(self):
        '''
        Return tuple for set date of birth.
        '''
        return self.date_of_birth

    def show(self, date_of_birth=None):
        self.date_of_birth = date_of_birth

        if self.date_of_birth:
            self.calendar.select_month(self.date_of_birth[1] - 1, self.date_of_birth[0])
            self.calendar.select_day(self.date_of_birth[2])

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            year, month, day = self.calendar.get_date()
            month += 1

            self.date_of_birth = (year, month, day)

        self.hide()

        return self.date_of_birth
