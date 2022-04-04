from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class Menu(BoundFilter):
    key = 'menu'

    def __init__(self, menu):
        self.menu = menu

    async def check(self, message: Message):
        if message.text in ["➕ Новое напоминание", "📝 Список напоминаний", "🛠 Админ клавиатура", "💵 Донат",
                            "❔ Помощь по командам", "➕ New reminder", "📝 Reminder List", "🛠 Admin keyboard",
                            "💵 Donat", "❔ Help by commands", "➕ Добавить Админа", "🎁 Выдать VIP", "🔖 Рассылка",
                            "📫 Личка", "🧾 Меню", "➕ Add Admin", "🎁 Issue VIP", "🔖 Newsletter", "📫 Personal",
                            "🧾 Menu"]:
            return self.menu == True
        else:
            return True
