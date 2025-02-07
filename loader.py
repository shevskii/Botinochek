from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN

dp = Dispatcher(storage=MemoryStorage())

# if PLACE_OF_LAUNCH == 1:
#     session = AiohttpSession(proxy='http://proxy.server:3128')
#     bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML, session=session)

# else:
#     bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

router = Router()



