from apscheduler.schedulers.asyncio import AsyncIOScheduler
from notify_logic import check_expired_clients
import pytz

def start_scheduler():
    scheduler = AsyncIOScheduler()
    timezone = pytz.timezone("Asia/Novosibirsk")
    scheduler.add_job(check_expired_clients, "cron", hour=11, minute=00, timezone=timezone)
    scheduler.start()
