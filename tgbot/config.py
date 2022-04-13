import os
from tgbot.services.repository.db import Repo
from typing import Set


root_path = os.path.abspath(os.path.dirname(__file__))


class DbConfig:
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE = os.getenv("DATABASE")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")


class FLBotConfig:
    TOKEN = os.getenv("TOKEN")
    ADMINS: Set[int] = {}
    LANGUAGES = {"en", "uk", "ru"}


class I18NConfig:
    I18N_DOMAIN = "default"
    LOCALES_DIR = os.path.join(root_path, "locales")


class GoogleSheetsAPIConfig:
    CREDENTIALS_FILE = os.path.join(root_path, "creds.json")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


class Config(DbConfig, FLBotConfig, I18NConfig, GoogleSheetsAPIConfig):
    pass


async def upload_admins(pool, admins):
    db = await pool.acquire()
    await Repo(db).upload_admins(admins)
    await db.close()

