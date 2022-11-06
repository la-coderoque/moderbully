import os
import json

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = json.loads(os.environ['ADMIN_IDS'])

POSTGRES_URL = URL.create(
    'postgresql+asyncpg',
    username=os.getenv('DB_USER'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT'),
    password=os.getenv('DB_PASS'),
)
