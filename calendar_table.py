from session import Session,User_detail

from bs4 import BeautifulSoup as bs
from pyrogram import Client, filters, types

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

def global_calendar(session):
    current_month_link = "https://moodle.cestarcollege.com/moodle/calendar/view.php?view=month"

    return get_calendar_details(session, current_month_link)


def prev_month(session):
    pass


def next_calendar(session):
    pass


def get_calendar_details(session, link):
    url = str(link)
    print(url)
    response = session.get(url, headers=headers, verify=False)
    if response.status_code == 200:

        calendar_soup = bs(response.content, "html5lib")
        print(calendar_soup.prettify())
        table = calendar_soup.find("table", id="month-detailed-6")

        print(table)

        return table

    return False