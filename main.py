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
import asyncio
import os

from dotenv import load_dotenv
from get_docker_secret import get_docker_secret

import scrap_data

load_dotenv()

config = dict()


def load_config():
    config["WEBHOOK_URL"] = get_docker_secret("WEBHOOK_URL", autocast_name=False)
    config["email"] = get_docker_secret("EMAIL", autocast_name=False)
    config["password"] = get_docker_secret("PASSWORD", autocast_name=False)
    config["link"] = get_docker_secret("CODEZINGER_DASHBOARD", autocast_name=False)
    config["chrome_path"] = os.getenv("CHROME_PATH", "")

    print(config)


def main():
    print("Hello World")
    load_config()

    data = asyncio.run(scrap_data.main(**config))
    print(data)


if __name__ == '__main__':
    print("""DB-Hax  Copyright (C) 2021  RoguedBear, Ya-s-h
    This program comes with ABSOLUTELY NO WARRANTY; see COPYING
    This is free software, and you are welcome to redistribute it
    under certain conditions; see COPYING""")
    try:
        main()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
