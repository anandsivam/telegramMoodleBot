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
        # print(soup.prettify())
        courses_side_menu = soup.find_all('div', attrs={'class': 'column c1'})
        courses_link_dict = {}

        for course in courses_side_menu:
            course_data = course.find('a')
            courses_link_dict["_".join(course_data.text.split()[6:])] = course_data['href']

        return courses_link_dict

    return False


def course_detail(session, link):
    url = str(link)

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


def grades(session, url):
    main_url = 'https://moodle.cestarcollege.com/moodle/grade/report/user/index.php?id=' + url

    response = session.get(main_url, headers=headers, verify=False)
    print(main_url)

    if response.status_code == 200:
        soup = bs(response.content, 'html5lib')

        grades = []

        gname_start = soup.find_all('th', attrs={'class': 'level2 leveleven item b1b column-itemname'})

        for item in gname_start:
            parent = item.parent

            name = parent.find('th', attrs={'class': 'level2 leveleven item b1b column-itemname'}).text
            grade = parent.find('td', attrs={'class': 'level2 leveleven item b1b itemcenter column-grade'}).text
            ranges = parent.find('td', attrs={'class': 'level2 leveleven item b1b itemcenter column-range'}).text
            precentage = parent.find('td',
                                     attrs={'class': 'level2 leveleven item b1b itemcenter column-percentage'}).text

            value = f'{name}\n Grade ={grade} Range ={ranges} Percentage ={precentage}'

            grades.append(value)
            print(grades)
        return grades

    return False


def resource_get(session, link):
    url = str(link)

    response = session.get(url, headers=headers, verify=False)
    if response.status_code == 200:

        soup = bs(response.content, 'html5lib')
        header = soup.find_all('h3', attrs={'class': 'sectionname'})

        resources = []

        for item in header:

            # print(item.text)  # header - general / recored lecture

            parent = item.parent

            files = parent.find_all('li', attrs={'class': 'activity resource modtype_resource'})

            folders = parent.find_all('li', attrs={'class': 'activity folder modtype_folder'})

            if files or folders:
                resources.append(item.text)
                resources.append('--------------------------')

            for i in files:
                link = i.find('a', attrs={'class': 'aalink'})

                name_link = f'<a href="{link["href"]}">{link.text}</a>'

                # print('File', link.text, link['href'])

                resources.append(name_link)

            for j in folders:

                link = j.find('a', attrs={'class': 'aalink'})

                fold_link = link['href']

                sub_response = session.get(fold_link, headers=headers, verify=False)

                if sub_response.status_code == 200:
                    soup_sub = bs(sub_response.content, 'html5lib')

                    finder = soup_sub.find_all('span', attrs={'class': 'fp-filename'})

                    for sub_find in finder:

                        if sub_find.text != '':
                            sub_parent = sub_find.parent

                            name_link = f'<a href="{sub_parent["href"]}">{sub_find.text}</a>'

                            # print('Folder',sub_find.text,sub_parent['href'])

                            resources.append(name_link)

            if files or folders:
                resources.append(" ")

        return resources

    return False
