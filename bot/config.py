import os
import json

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = json.loads(os.environ['ADMIN_IDS'])
