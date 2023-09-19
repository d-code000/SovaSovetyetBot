from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_menu_approval = [
    [
     InlineKeyboardButton(text="Согласен ✔️ ", callback_data="agree"),
     InlineKeyboardButton(text="Не согласен ✖️", callback_data="disagree")
    ]
]

inline_menu_publicity = [
    [
     InlineKeyboardButton(text="Остаться анонимным 🔒", callback_data="anonymous"),
     InlineKeyboardButton(text="Можно публично 🔓", callback_data="publicly")
    ]

]

inline_menu_approval = InlineKeyboardMarkup(inline_keyboard=inline_menu_approval)
inline_menu_publicity = InlineKeyboardMarkup(inline_keyboard=inline_menu_publicity)
