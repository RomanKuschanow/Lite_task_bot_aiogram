from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _

from services.timer import get_timer


def get_control_inline_markup(timer_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(resize_keyboard=True)

    timer = get_timer(timer_id)

    markup.row()

    if (timer.end_date - timer.start_date).total_seconds() > 120:
        markup.insert(InlineKeyboardButton(_("📝 Задать текст"), callback_data=f"timer:text:{timer_id}"))

    if not timer.is_paused:
        markup.insert(InlineKeyboardButton(_("⏸ Стоп"), callback_data=f"timer:pause:{timer_id}"))
    else:
        markup.insert(InlineKeyboardButton(_("▶ Запуск"), callback_data=f"timer:play:{timer_id}"))

    markup.insert(InlineKeyboardButton(_("🗑 Удалить"), callback_data=f"timer:delete:{timer_id}"))

    markup.row(InlineKeyboardButton(_('🔄 Обновить'), callback_data=f"timer:update:{timer_id}"))

    markup.insert(InlineKeyboardButton(_('❎ Готово'), callback_data=f'done'))

    return markup
