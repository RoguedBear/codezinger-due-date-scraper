"""
    Copyright (c) 2021 Ya-s-h, RoguedBear

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from scrap_data import *


def main():
    print("Hello World")


if __name__ == '__main__':
    print("""DB-Hax  Copyright (C) 2021  RoguedBear, Ya-s-h
    This program comes with ABSOLUTELY NO WARRANTY; see COPYING
    This is free software, and you are welcome to redistribute it
    under certain conditions; see COPYING""")
    try:
        main()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
