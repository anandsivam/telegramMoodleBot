class Session:

    def __init__(self, session=None):
        self._session = session

    def get_session(self):
        return self._session

    def set_session(self, session):
        self._session = session


class Course_link:

    def __init__(self, links=None):
        self._links = links

    def get_links(self):
        return self._links

    def set_links(self, links):
        self._links = links


class User_detail:

    def __init__(self, name=None):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name


CURRENT_CALENDAR_MONTH_LINK = "https://moodle.cestarcollege.com/moodle/calendar/view.php?view=month"
CALENDAR_LINKS = ["previous month link", "next month link"]
