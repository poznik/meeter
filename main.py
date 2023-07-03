import config
from meeter import Meeter

print('Lets go')

# точка входа. После нужно будет разнести на скрипт для винды и app для macos
meeter = Meeter(config.EWS_LOGIN, config.EWS_PASSWORD, config.DAYS_TO_LOAD, config.BOT_API_TOKEN, config.BOT_OWNER_ID)

