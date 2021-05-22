from os import getenv
from dotenv import load_dotenv
from errors import TokenNotFound

load_dotenv()

TOKEN  = getenv("DISCORD_TOKEN")
if not TOKEN:
    raise TokenNotFound("Discord bot token not found")

# minimum master password length
MIN_LENGTH = int(getenv("MIN_PASSWORD_LENGTH")) or 7
# timeout in minutes for logging out an inactive user
INACTIVE_TIMEOUT = int(getenv("INACTIVE_TIMEOUT")) or 15
# maximum length of password needed
# this can be changed to suit your password length
PASSWORD_LEN = int(getenv("PASSWORD_LEN")) or 16
DB_FILE = getenv("DB_FILE") or "db/data.db"
LOG_FILE= getenv("LOG_FILE") or "db/db-log.txt"
