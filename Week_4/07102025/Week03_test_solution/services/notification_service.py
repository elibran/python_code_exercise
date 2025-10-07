import time
from pathlib import Path
from utils.logging import get_logger

logger = get_logger(__name__)
LOG_FILE = Path("./notifications.log")

def send_order_notification(user_email: str, order_id: int):
    # simulate send email
    time.sleep(0.05)
    logger.info("notification_sent", extra={"order_id": order_id})
    LOG_FILE.write_text((LOG_FILE.read_text() if LOG_FILE.exists() else "") + f"Notified {user_email} for order {order_id}\n")
