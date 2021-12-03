from pyrogram import types


def home_menu_reply_markup(course_list):
    button_list = [
        [ #Oth row for calendar
            types.InlineKeyboardButton(
                'Calendar',
                callback_data="calendar"
            )
        ]
    ]

    for course_name in course_list.keys():
        temp_list = []
        temp_list.append(types.InlineKeyboardButton(course_name, callback_data=course_name))
        button_list.append(temp_list)

    return types.InlineKeyboardMarkup(button_list)

CALENDAR_REPLY_MARKUP = types.InlineKeyboardMarkup(
    [
        [  # First row
            types.InlineKeyboardButton(
                'Previous Month',
                callback_data="previous_month"
            ),
        ],
        [  # second row
            types.InlineKeyboardButton(
                'Next Month',
                callback_data="next_month"
            ),
        ],
        [  # third row
            types.InlineKeyboardButton(
                'Back',
                callback_data="back"
            ),
        ]
    ]
)
