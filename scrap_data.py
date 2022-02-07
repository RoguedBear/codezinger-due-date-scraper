# Copyright (c) 2021 RoguedBear
"""
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
import json
import traceback
from datetime import datetime
from pprint import pprint
from time import sleep
from typing import List

import selenium.webdriver.remote.webelement
from pyppeteer import launch
from pyppeteer.element_handle import ElementHandle
from pyppeteer.page import Page
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# CONSTANTS

FOLDER_BUTTON_XPATH = "/html/body/app/div[1]/main/ng-component/div[1]/div/problemset-tree/div[1]/div[2]/div/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node/div/tree-node-wrapper/div/div/div/div/button"
QUESTIONS_XPATH = "/html/body/app/div[1]/main/ng-component/div[1]/div/problemset-tree/div[1]/div[2]/div/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node/div/tree-node-children/div/tree-node-collection/div/tree-node/div/tree-node-wrapper/div/div/div"
QUESTION_TITLE_XPATH = "div[1]/button/span[4]"
PROBLEM_NUMBER_XPATH = "div[1]/button/span[2]"
DUE_DATE_XPATH = "div[2]/div[1]/div/span/span[2]"
STATUS_XPATH = "div[2]/div[4]/div/span[2]"
DEBUG = False

with open("xpaths.json") as file:
    XPATHS = json.load(file)


# ========


def main(driver: webdriver.Chrome):
    print("A new CHROME browser window will open with the codezinger link in it")
    print("You have to enter your login and password.")
    # input("Press enter to continue... ")
    login_codezinger(driver)
    expand_all_labs(driver)
    data = get_data(driver)
    pprint(data)


async def login_codezinger(page: Page, username, password):
    await set_cookies(page)
    link = "https://labs.codezinger.com/student/dashboard"
    await page.goto(link)

    if "login" not in (await page.title()).lower():
        print("Logged in. allegedly")
        return

    if DEBUG or (username and password):
        print("Cookie login didn't work, trying manual login")
        while "login" not in (await page.title()).lower():
            sleep(1)

        email = (await page.xpath(XPATHS["LOGIN_EMAIL_INPUT"]))[0]
        # await email.click()
        await email.type(username)
        pwd = (await page.xpath(XPATHS["LOGIN_PASSWD_INPUT"]))[0]
        # await pwd.click()
        await pwd.type(password)
        submit = (await page.xpath(XPATHS["LOGIN_SUBMIT_BTN"]))[0]
        await submit.click()
        sleep(1)
        try:
            yes = await page.xpath(XPATHS["LOGIN_FORCE_YES_BTN"])
            print(yes)
            await yes[0].click()
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            await page.close()

    while "login" in (await page.title()).lower():
        sleep(1)

    print("logged in")

    await save_cookies(page)


async def expand_all_labs(page: Page):
    async def get_buttons():
        return await page.querySelectorAll(".chapter-node > div > div > button")

    buttons = []
    while not buttons:
        # buttons = await page.evaluate()
        buttons = await get_buttons()
    prev_len = len(buttons)
    # input("PAUSED.")
    for button in buttons:
        while (await page.evaluate('node => node.getAttribute("aria-expanded")', button)) != 'true':
            await button.click()
            sleep(0.3)

            # get new buttons if they exist
    print("Expanded", len(buttons), "folders.")


async def sort_pending_by_due_date(page: Page):
    pending_text_button = []
    while pending_text_button == []:
        pending_text_button = await page.xpath(XPATHS["PENDING_DUE_DATE_FILTER"])
        sleep(0.1)
    pending_text = await page.evaluate('(node) => node.textContent', pending_text_button[0])

    if pending_text != "Pending By Due Date":
        await pending_text_button[0].click()
        due_by_pending_btn = (await page.xpath(XPATHS["PENDING_DUE_DATE_BTN"]))[0]
        await due_by_pending_btn.click()


async def keep_clicking_load_more(page: Page):
    async def get_load_more() -> list[ElementHandle]:
        return await page.xpath(XPATHS["LOAD_MORE_BTN"])

    # wait for the button to load first
    button = []
    while not button:
        button = await get_load_more()
        sleep(0.05)

    while button := await get_load_more():
        await button[0].click()
        sleep(0.5)


async def get_data(page: Page) -> List[dict]:
    # TODO: convert this to async
    data_list: List[dict, ...] = []
    questions = await page.xpath(XPATHS["QUESTION_ROW"])
    print(questions)
    print(len(questions))

    question: ElementHandle
    for index, question in enumerate(questions):
        print("Processing data... ({:3.0%})".format(index / len(questions)), end="\r")

        question_title = await question.xpath(XPATHS["RELATIVE_QUESTION"])
        codezinger_class = await question.xpath(XPATHS["RELATIVE_CLASS"])
        question_type = await question.xpath(XPATHS["RELATIVE_Q_TYPE"])
        due_date = (await question.xpath(XPATHS["RELATIVE_DUE_DATE"]))
        try:
            due_date = await page.evaluate('node => node.getAttribute("data-bs-original-title")', due_date[0])
            due_date = due_date.strip("Due: <br/>Late -")
            # print(due_date)
            parsed_date = datetime.strptime(due_date, "%d %b, %I:%M %p")
            parsed_date = parsed_date.replace(year=datetime.now().year)
            # parsed_date = parsed_date.isoformat()
            # print(index, parsed_date)
        except ValueError:
            parsed_date = datetime.min

        data_list.append({
            "question": await get_text(page, question_title[0]),
            "class": await get_text(page, codezinger_class[0]),
            "question_type": "assignment" if (await get_text(page, question_type[0])) else "practise",
            "due_date": parsed_date
        })
    print("Scraped", len(questions), "questions")

    return data_list


async def set_cookies(page: Page):
    # try to load cookies and refresh
    with open("cookies.json") as f:
        cookies = json.load(f)
    await page.setCookie(*cookies)


async def save_cookies(page: Page):
    # save cookies
    cookies = await page.cookies()
    with open("cookies.json", "w") as file:
        json.dump(cookies, file)


async def get_text(page: Page, element: ElementHandle):
    return await page.evaluate('(node) => node.textContent', element)


def safe_find_element_by_xpath(element: selenium.webdriver.remote.webelement.WebElement, xpath: str) -> str:
    result: str
    try:
        result = element.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        result = "NULL"
    return result


if __name__ == '__main__':
    driver = webdriver.Chrome()
    try:
        main(driver)
        x = input("enter to close....")
        if x:
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        driver.close()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        driver.close()
