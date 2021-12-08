import regex
from bs4 import BeautifulSoup as bs
from session import CALENDAR_LINKS, CURRENT_CALENDAR_MONTH_LINK

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}


def global_calendar(session):
    return get_calendar_details(session, CURRENT_CALENDAR_MONTH_LINK)


def get_calendar_details(session, link):
    url = str(link)
    print(url)
    response = session.get(url, headers=headers, verify=False)

    if response.status_code == 200:

        calendar_soup = bs(response.content, "html5lib")
        events_day_list = []
        month_name = calendar_soup.find('h2').string
        events_day_list.append(f"{month_name} \n\n\n")

        prev_mon_link = calendar_soup.find('a', attrs={'title' : 'Previous month'})['href']
        CALENDAR_LINKS[0] = prev_mon_link

        next_mon_link = calendar_soup.find('a', attrs={'title' : 'Next month'})['href']
        CALENDAR_LINKS[1] = next_mon_link

        table = calendar_soup.find('table', attrs={'class': 'calendarmonth calendartable mb-0'})

        day_rows = table.tbody.find_all('td', attrs={'data-region': 'day'})

        for day in day_rows:
            day_event_count = day.find('span', attrs={'class': "sr-only"}).string
            if regex.match("no events*", day_event_count, regex.IGNORECASE):
                pass
            else:
                event_links = day.find_all('a', attrs={'data-action': 'view-event'})
                for event_link in event_links:
                    title = event_link.get("title")
                    link = event_link.get("href")
                    convtd_date_str = " ".join(day_event_count.split()[2:])
                    append_str = f"{convtd_date_str} \n{title}: {link}\n\n"

                    events_day_list.append(append_str)

        return " ".join(events_day_list)

    return False
