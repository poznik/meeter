import telebot


class MeetBot:
    bot_api_token = ""
    bot_owner_id = 0
    bot: telebot.TeleBot

    def __init__(self, bot_api_token, bot_owner_id):
        self.bot_owner_id = bot_owner_id
        self.bot_api_token = bot_api_token
        self.bot = telebot.TeleBot(token=bot_api_token)

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            self.bot.send_message(message.from_user.id, "Hi man, your id is " + str(message.from_user.id))

    def send_message(self, text):
        self.bot.send_message(self.bot_owner_id, text, disable_web_page_preview=True, parse_mode="Markdown")

    def go(self):
        self.bot.polling(non_stop=True, interval=0)
