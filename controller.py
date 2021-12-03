from pyrogram import Client, filters, types
import logging
import time

import calendar_table
import login
from session import Session, Course_link, User_detail
import reply_markups

from pyrogram.types.bots_and_keyboards import callback_query

bot = Client('my_bot', api_id='xxxx', api_hash='xxxxxx',
             bot_token='xxxx:xx')

# Getter and setter - session
my_session = Session()

# Getter and setter - course link
links = Course_link()

#Student detail to fetch name
detail = User_detail()

#course list links
course_list = []

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

    if query.data == 'calendar':
        cal_curr_month = calendar_table.global_calendar(session)
        await client.edit_message_text(query.message.chat.id, query.message.message_id,
                                       text=f"Hi! {detail.get_name()}\n\n"
                                            "Your Calendar of Current Month!\n",
                                       reply_markup=reply_markups.home_menu_reply_markup(course_list))
    elif query.data == 'prev_month':
        cal_prev_month = calendar_table.global_calendar(client, query)
    elif query.data == 'next_month':
        cal_next_month = calendar_table.global_calendar(client, query)

    elif query.data == 'python':
        recorded_links = []
        course_link = links.get_links()
        for course, link in course_link.items():
            if course == 'Python':
                recorded_links = login.course_detail(session, link)

        value = '\n'.join(recorded_links)
        await client.edit_message_text(query.message.chat.id, query.message.message_id,
                                       text=f"Welcome {detail.get_name()}\n\n"
                                            "Python course recorded lectures\n"
                                            f"{value}",
                                       reply_markup=reply_markups.home_menu_reply_markup(course_list)
                                       )

    elif query.data == 'back':
        await client.edit_message_text(query.message.chat.id, query.message.message_id,

                                       text=f"Welcome {detail.get_name()}\n\n"
                                            f"Please select the course\n"
                                            "from the below buttons",
                                       reply_markup=reply_markups.home_menu_reply_markup(course_list))



bot.run()
