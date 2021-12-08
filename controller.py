from os import environ
from pyrogram import Client, filters, types
import logging
import time

import calendar_table
import login
from session import Session, Course_link, User_detail, CALENDAR_LINKS
import reply_markups

from pyrogram.types.bots_and_keyboards import callback_query

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


API_ID = int(environ["API_ID"])
API_HASH = environ["API_HASH"]
BOT_TOKEN = environ["BOT_TOKEN"]

bot = Client("Lambton Moodle Scrappy Bot", api_id=API_ID, api_hash=API_HASH,
             bot_token=BOT_TOKEN)

print('Hi! Welcome to my "Lambton Moodle Scrappy Bot"')

# Getter and setter - session
my_session = Session()

# Getter and setter - course link
links = Course_link()

# Student detail to fetch name
detail = User_detail()


@bot.on_message(filters.command(['start', 'help', 'login']))
def command_handler(client, message):
    if message.text == '/start':
        message.reply_text('Hello Hi ! I am online\n\n\n'
                           'For moodle login use the below format\n\n'
                           '/login\n'
                           'id\n'
                           'password')

    elif message.text == '/help':
        pass

    # to do - sess_key to be found | stop the session | set the setters to none
    if '/login' in message.text:

        value = message.text.split()

        if len(value) == 3:

            result = login.login(value[1], value[2])

            if result:

                # result has name and session
                name = result[0]
                my_session.set_session(result[1])
                course_list = login.course_getter(my_session.get_session())
                # setter are set for session and link
                links.set_links(course_list)
                detail.set_name(name)

                # if course_list having name and links
                if course_list:
                    client.send_message(
                        message.chat.id,
                        f"Welcome {name}\n\n"
                        f"Please select the course\n"
                        "from the below buttons",
                        reply_markup=reply_markups.home_menu_reply_markup(course_list)
                    )
                else:
                    print('error')
            else:
                message.reply_text(f'Enter the valid id and password with login')
        else:
            message.reply_text(f'Enter the valid id and password with login')


@bot.on_callback_query()
async def markup(client, query):
    session = my_session.get_session()
    course_list_dict = login.course_getter(session)

    if query.data == 'calendar':
        print(CALENDAR_LINKS)
        cal_curr_month = calendar_table.global_calendar(session)
        await client.send_message(query.message.chat.id,
                                  text=f"Hi! {detail.get_name()}\n\nYour Calendar of Month - {cal_curr_month}",
                                  reply_markup=reply_markups.CALENDAR_REPLY_MARKUP)

    elif query.data == 'previous_month':
        print(CALENDAR_LINKS)
        cal_prev_month = calendar_table.get_calendar_details(session, link=CALENDAR_LINKS[0])
        await client.send_message(query.message.chat.id,
                                  text=f"Hi! {detail.get_name()}\n\nYour Calendar of Month - {cal_prev_month}",
                                  reply_markup=reply_markups.CALENDAR_REPLY_MARKUP)

    elif query.data == 'next_month':
        print(CALENDAR_LINKS)
        cal_next_month = calendar_table.get_calendar_details(session, link=CALENDAR_LINKS[1])
        await client.send_message(query.message.chat.id,
                                  text=f"Hi! {detail.get_name()}\n\nYour Calendar of Month - {cal_next_month}",
                                  reply_markup=reply_markups.CALENDAR_REPLY_MARKUP)

    elif query.data in course_list_dict.keys():

        recorded_links = login.course_detail(session, course_list_dict[query.data])

        value = '\n'.join(recorded_links)
        await client.send_message(query.message.chat.id,
                                  text=f"Hey {detail.get_name()}!\n\n\nCourse: {query.data}\n\nRecorded Lectures:\n{value}",
                                  reply_markup=reply_markups.COURSE_REPLY_MARKUP
                                  )

    elif query.data == 'home':
        await client.send_message(query.message.chat.id,
                                  text=f"Hey {detail.get_name()}!\n\n\nPlease select a course \nfrom the below buttons",
                                  reply_markup=reply_markups.home_menu_reply_markup(course_list_dict)
                                  )


bot.run()
