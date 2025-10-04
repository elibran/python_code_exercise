from pathlib import Path
import logging
from typing import Protocol
from app.core.config import get_settings

logger = logging.getLogger(__name__)

class EmailService(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...

class ConsoleEmailService:
    def send(self, to: str, subject: str, body: str) -> None:
        logger.info("DEV email -> to=%s subject=%s", to, subject)
        print(f"[EMAIL DEV] to={to} subject={subject}\n{body}")

class FileEmailService:
    def __init__(self, outbox_file: str) -> None:
        self.path = Path(outbox_file)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def send(self, to: str, subject: str, body: str) -> None:
        logger.info("FILE email -> file=%s to=%s subject=%s", self.path, to, subject)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"TO: {to}\nSUBJECT: {subject}\n{body}\n---\n")

def get_email_service() -> EmailService:
    settings = get_settings()
    if settings.app_env.lower().startswith("prod"):
        return FileEmailService(settings.email_outbox_file)
    return ConsoleEmailService()
