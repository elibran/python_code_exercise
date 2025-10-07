import time
from utils.logging import get_logger

logger = get_logger(__name__)

class PaymentService:
    # Fake external payment service integration.
    # Set simulate_failure=True to force a failure (e.g. via header in endpoint).
    def __init__(self, simulate_failure: bool = False):
        self.simulate_failure = simulate_failure

    def process_payment(self, amount: float, user_id: int) -> bool:
        # Simulate latency
        time.sleep(0.05)
        logger.info("payment_attempt", extra={"user_id": user_id})
        if self.simulate_failure:
            return False
        # High probability success
        return True
