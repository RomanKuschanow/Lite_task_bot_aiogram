from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_reminders_inline_markup(hidden_button: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    tiles = [{'text': _("все"), 'callback': "all"},
             {'text': _("старые"), 'callback': "old"},
             {'text': _("предстоящие"), 'callback': "actual"}]

    for tile in range(3):
        if tiles[tile - 1]['callback'] == hidden_button:
            tiles.pop(tile - 1)

    markup.row(InlineKeyboardButton(tiles[0]['text'], callback_data=f'{tiles[0]["callback"]}'),
               InlineKeyboardButton(tiles[1]['text'], callback_data=f'{tiles[1]["callback"]}'))
    return markup
