import requests

from bs4 import BeautifulSoup as bs

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}


def login(id, password):
    login_data = {

        'anchor': '',
        'logintoken': 'value',
        'username': id,
        'password': password,
        'rememberusername': '1'

    }

    with requests.session() as session:
        url = 'https://moodle.cestarcollege.com/moodle/login/index.php'
        response = session.get(url, headers=headers, verify=False)
        soup = bs(response.content, 'html5lib')
        login_data['logintoken'] = soup.find('input', attrs={'name': 'logintoken'})['value']
        login_data['rememberusername'] = soup.find('input', attrs={'name': 'rememberusername'})['value']

        response = session.post(url, data=login_data, headers=headers, verify=False)
        soup = bs(response.content, 'html5lib')

        if response.status_code == 200:
            setters = []
            name = soup.find('span', attrs={'class': 'usertext mr-1'}).text
            setters.append(name)
            setters.append(session)
            return setters

        return False


def course_getter(session):
    url = 'https://moodle.cestarcollege.com/moodle/my/'
    response = session.get(url, headers=headers, verify=False)

    if response.status_code == 200:

        soup = bs(response.content, 'html5lib')
        #print(soup.prettify())
        courses_side_menu = soup.find_all('div', attrs={'class': 'column c1'})
        courses_link_dict = {}

        for course in courses_side_menu:
            course_data = course.find('a')
            courses_link_dict["_".join(course_data.text.split()[6:])] = course_data['href']

        return courses_link_dict

    return False


def course_detail(session, link):
    url = str(link)

    print(url)
    response = session.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        soup = bs(response.content, 'html5lib')
        recorded_link = soup.find_all('li', attrs={'class': 'activity url modtype_url'})
        links = []
        for link in recorded_link:
            data = link.find('a')
            links.append(data['href'])

        return links

    return False


