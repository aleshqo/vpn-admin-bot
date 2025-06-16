from dotenv import load_dotenv

from google_client import get_google_sheet
from datetime import datetime, timedelta
import os
from aiogram import Bot

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))

CURATOR_TO_TAG = {
    "Петя": "@zdrpp",
    "Олег": "@oleg_vorobey1111 🐓",
    "Леха": "@gitfh"
}


def parse_date_safe(raw):
    try:
        return datetime.strptime(raw.strip(), "%d.%m.%Y")
    except Exception:
        return None

async def check_expired_clients():
    sheet = get_google_sheet()
    rows = sheet.get_all_values()[2:]  # пропускаем заголовки

    today = datetime.today()
    warning_date = today + timedelta(days=3)

    for row in rows:
        name = row[0] if len(row) > 0 else ""
        curator = resolve_curator_tag(row[2].strip() if len(row) > 2 else "")
        period = row[4] if len(row) > 4 else ""
        key_id = row[6] if len(row) > 6 else "?"

        date = parse_date_safe(period)
        if not date:
            continue

        if date <= warning_date:
            status = "истекает" if date > today else "ИСТЁК!"
            msg = (
                f"⚠️ {status} срок VPN-ключа!\n"
                f"👉 Клиент: \"<b>{name}</b>\"\n"
                f"💅 Куратор: {curator}\n"
                f"📅 До: <code>{date.strftime('%d.%m.%Y')}</code>\n"
                f"🆔 Key ID: <code>{key_id}</code>"
            )
            await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=msg, parse_mode="HTML")


def resolve_curator_tag(name: str) -> str:
    """
    Возвращает Telegram-ник по имени куратора, если есть в словаре.
    Если не найдено в словаре — возвращает оригинальное имя.
    Если имя не указано — возвращает "куратор не указан".
    """
    name = name.strip()
    if not name:
        return "Какой-то долбаеб не указал куратора!"
    return CURATOR_TO_TAG.get(name, name)
