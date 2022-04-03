from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class Menu(BoundFilter):
    key = 'menu'

    def __init__(self, menu):
        self.menu = menu

    async def check(self, message: Message):
        if message.text in ["➕ Новое напоминание", "📝 Список напоминаний", "🛠 Админ клавиатура", "💵 Донат",
                            "❔ Помощь по командам", "➕ New reminder", "📝 Reminder List", "🛠 Admin keyboard",
                            "💵 Donat", "❔ Help by commands"]:
            print(message.text)
            print(self.menu == True)
            return self.menu == True
        else:
            return True
