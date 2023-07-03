"""

Конфигурационный файл для python-скрипта Meeter
Переименуй в config.py

me@poznik.ru
07-2023

"""

# токен персонального бота для оповещения о встречах в Telegram.
# нужно получить у @BotFather перед использованием бота
BOT_API_TOKEN = "your token here"

# ID вашего пользователя Telegram, нужно для отправки сообщений
# можно узнать у @userinfobot
BOT_OWNER_ID = 0000000

# данные для работы с календарем. Логин указывается с @domain.com
EWS_LOGIN = "your_email@here.com"
EWS_PASSWORD = "password here"
DAYS_TO_LOAD = 1  # количество дней для загрузки встреч из календаря. Считается от момента запуска скрипта

"""

настройки нотификаций и задержек

"""

# за сколько минут уведомлять о предостоящей встрече
PRENOTIFY_DELAY_MINUTES = 5  #default = 5

# периоды срабатывания таймеров загрузки встреч из календаря и оповещения о встречах
NOTIFICATION_TIMER_DELAY_SEC = 30  # default = 30
LOAD_MEETING_TIMER_DELAY_SEC = 5 * 60  # default = 5 * 60

# локальный сдвиг от UTC. Например для UTC+4 указывается 4
LOCAL_UTC_PLUS = 4

# Задержка в секундах от старта скрипта до запуска таймеров.
LOAD_MEETING_TIMER_START_DELAY_SEC = 2  # default = 2
NOTIFICATION_TIMER_START_DELAY_SEC = 15  # default = 15
