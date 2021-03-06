"""
Dwarf - Copyright (C) 2018 iGio90

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget

from ui.widget_item_not_editable import NotEditableTableWidgetItem


class RangesPanel(QTableWidget):
    def __init__(self, app, *__args):
        super().__init__(*__args)
        self.app = app

        self.verticalHeader().hide()
        self.horizontalScrollBar().hide()
        self.setShowGrid(False)
        self.setHorizontalHeaderLabels(['base', 'size', 'protection', 'file'])
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cellDoubleClicked.connect(self.ranges_cell_double_clicked)

    def set_ranges(self, ranges):
        self.setRowCount(0)
        i = 0
        for range in sorted(ranges, key=lambda x: x['base'], reverse=True):
            self.insertRow(i)
            q = NotEditableTableWidgetItem(range['base'])
            q.setForeground(Qt.red)
            self.setItem(i, 0, q)
            self.setItem(i, 1, NotEditableTableWidgetItem(str(range['size'])))
            self.setItem(i, 2, NotEditableTableWidgetItem(range['protection']))
            if 'file' in range:
                q = NotEditableTableWidgetItem(range['file']['path'])
                q.setForeground(Qt.gray)
                self.setItem(i, 3, q)
            else:
                self.setItem(i, 3, NotEditableTableWidgetItem(''))
            i += 1
        self.resizeRowToContents(1)

    def ranges_cell_double_clicked(self, row, c):
        if c == 0:
            self.app.get_memory_panel().read_memory(self.item(row, c).text())
