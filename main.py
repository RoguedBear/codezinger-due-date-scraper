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
import traceback

import yaml
from dotenv import load_dotenv
from get_docker_secret import get_docker_secret

import scrap_data
from classes.Database import Database
from classes.QuestionData import QuestionData
from classes.Webhook import Webhook
from data_processing import process_data, purge_old_questions

load_dotenv()

config = dict()


def load_config():
    config["WEBHOOK_URL"] = get_docker_secret("WEBHOOK_URL", autocast_name=False)
    config["email"] = get_docker_secret("EMAIL", autocast_name=False)
    config["password"] = get_docker_secret("PASSWORD", autocast_name=False)
    config["link"] = get_docker_secret("CODEZINGER_DASHBOARD", autocast_name=False)
    config["chrome_path"] = os.getenv("CHROME_PATH", "")
    config["AVATAR_URL"] = os.getenv("AVATAR_URL")
    config["WEBHOOK_USERNAME"] = os.getenv("WEBHOOK_USERNAME")

    try:
        with open("config.yml", "r", encoding="utf8") as config_file:
            config["mapping"] = yaml.safe_load(config_file)
            QuestionData.update_mapping_from_config(config["mapping"])
            print("loaded short names")
    except FileNotFoundError:
        print("config file does not exist! Skipping mapping")


def main():
    load_config()
    # init webhook & Database
    db = Database(folder="db/")
    webhook = Webhook(config["WEBHOOK_URL"], config["AVATAR_URL"], config["WEBHOOK_USERNAME"])

    data = asyncio.run(scrap_data.main(**config))
    process_data(data, db, webhook)
    purge_old_questions(db, webhook)


if __name__ == '__main__':
    print("""codezinger-due-date-scraper  Copyright (C) 2022  RoguedBear, Ya-s-h
    This program comes with ABSOLUTELY NO WARRANTY; see COPYING
    This is free software, and you are welcome to redistribute it
    under certain conditions; see COPYING""")
    try:
        main()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        # incase stderr isn't shown in portainer or the traceback thing isn't working
        print(ex)

    print("Finished, exiting...")
