from pyrogram import Client, filters, types
import logging
import time
import login
from session import Session, Course_link, User_detail

from pyrogram.types.bots_and_keyboards import callback_query

bot = Client('my_bot', api_id=xxxxx, api_hash='xxxxxxxx',
             bot_token='xxxxxxxx')

# Getter and setter - session
my_session = Session()

# Getter and setter - course link
links = Course_link()

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
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [  # First row
                                    types.InlineKeyboardButton(
                                        'Python',
                                        callback_data="python"
                                    ),
                                ],
                                [  # second row
                                    types.InlineKeyboardButton(
                                        'Career in AI',
                                        callback_data="career"
                                    ),
                                ],
                                [  # third row
                                    types.InlineKeyboardButton(
                                        'Ds & ML',
                                        callback_data="ml"
                                    ),
                                ],
                                [  # fourth row
                                    types.InlineKeyboardButton(
                                        'Communication',
                                        callback_data="comm"
                                    ),
                                ],
                                [  # fifth row
                                    types.InlineKeyboardButton(
                                        'Big data',
                                        callback_data="big"
                                    ),
                                ],
                                [  # sixth row
                                    types.InlineKeyboardButton(
                                        'Intro to AI',
                                        callback_data="ai"
                                    ),
                                ],
                                [  # First row
                                    types.InlineKeyboardButton(
                                        "Others",
                                        callback_data="other"
                                    ),
                                ]

                            ]
                        )
                    )
                else:
                    print('error')
            else:
                message.reply_text(f'Enter the valid id and password with login')
        else:
            message.reply_text(f'Enter the valid id and password with login')


@bot.on_callback_query()
async def markup(client, query):
    if query.data == 'python':
        course_link = links.get_links()
        session = my_session.get_session()

        recorded_links = []
        for course, link in course_link.items():
            if course == 'Python':
                recorded_links = login.course_detail(session, link)

        value = '\n'.join(recorded_links)
        await client.edit_message_text(query.message.chat.id, query.message.message_id,
                                       text=f"Welcome {detail.get_name()}\n\n"
                                            "Python course recorded lectures\n"
                                            f"{value}",
                                       reply_markup=types.InlineKeyboardMarkup(
                                           [
                                               [  # First row
                                                   types.InlineKeyboardButton(
                                                       'Recorded lectures',
                                                       callback_data="record"
                                                   ),
                                               ],
                                               [  # second row
                                                   types.InlineKeyboardButton(
                                                       'Grades',
                                                       callback_data="grades"
                                                   ),
                                               ],
                                               [  # third row
                                                   types.InlineKeyboardButton(
                                                       'Back',
                                                       callback_data="back"
                                                   ),
                                               ]
                                           ]
                                       ))

    elif query.data == 'back':
        await client.edit_message_text(query.message.chat.id, query.message.message_id,

                                       text=f"Welcome {detail.get_name()}\n\n"
                                            f"Please select the course\n"
                                            "from the below buttons",
                                       reply_markup=types.InlineKeyboardMarkup(
                                           [
                                               [  # First row
                                                   types.InlineKeyboardButton(
                                                       'Python',
                                                       callback_data="python"
                                                   ),
                                               ],
                                               [  # second row
                                                   types.InlineKeyboardButton(
                                                       'Career in AI',
                                                       callback_data="career"
                                                   ),
                                               ],
                                               [  # third row
                                                   types.InlineKeyboardButton(
                                                       'Ds & ML',
                                                       callback_data="ml"
                                                   ),
                                               ],
                                               [  # fourth row
                                                   types.InlineKeyboardButton(
                                                       'Communication',
                                                       callback_data="comm"
                                                   ),
                                               ],
                                               [  # fifth row
                                                   types.InlineKeyboardButton(
                                                       'Big data',
                                                       callback_data="big"
                                                   ),
                                               ],
                                               [  # sixth row
                                                   types.InlineKeyboardButton(
                                                       'Intro to AI',
                                                       callback_data="ai"
                                                   ),
                                               ],
                                               [  # First row
                                                   types.InlineKeyboardButton(
                                                       "Others",
                                                       callback_data="other"
                                                   ),
                                               ]

                                           ]
                                       ))



bot.run()
