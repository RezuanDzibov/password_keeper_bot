import os

from pathlib import Path

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BASE_DIR = Path(__file__).parent

dotenv_path = Path(f"{BASE_DIR}/.env")
load_dotenv(dotenv_path=dotenv_path)


API_TOKEN = os.getenv('API_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))


bot = Bot(API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
