"""Transfer helpers (with a tiny currency conversion demo).

The conversion uses a public exchange-rate API. We keep it robust and
easy-to-read: clear types, explicit errors, and small functions.
"""
from __future__ import annotations

from typing import Optional
import requests  # type: ignore


class ExchangeRateError(RuntimeError):
    """Raised when exchange rate retrieval fails."""


def get_exchange_rate(base_currency: str, quote_currency: str, *, timeout: float = 10.0) -> float:
    """Fetch the FX rate from ``base_currency`` to ``quote_currency``.

    Parameters
    ----------
    base_currency : str
        ISO 4217 code (e.g., 'USD').
    quote_currency : str
        ISO 4217 code to convert *into* (e.g., 'EUR').
    timeout : float, optional
        HTTP timeout in seconds.

    Returns
    -------
    float
        The numeric exchange rate.

    Raises
    ------
    ExchangeRateError
        If the HTTP request fails or the payload is missing the rate.
    """
    base = base_currency.upper().strip()
    quote = quote_currency.upper().strip()
    if len(base) != 3 or len(quote) != 3:
        raise ValueError("Currencies must be 3-letter ISO codes.")

    # Use exchangerate.host (free, no key) to avoid legacy endpoints.
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={quote}"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        rate = float(data["rates"][quote])
        return rate
    except Exception as exc:  # noqa: BLE001 - show friendly domain error
        raise ExchangeRateError(f"Failed to retrieve rate {base}->{quote}: {exc}") from exc


def international_transfer(from_account: Optional[object], to_account: Optional[object], amount: float, currency: str) -> float:
    """Convert ``amount`` USD into ``currency`` for an international transfer.

    This function purposely focuses on the conversion step to keep the demo
    simple. The ``from_account`` and ``to_account`` are placeholders.

    Parameters
    ----------
    from_account, to_account : object or None
        Placeholders for future account models.
    amount : float
        Positive amount denominated in USD.
    currency : str
        3-letter ISO code to convert into.

    Returns
    -------
    float
        Converted amount.

    Raises
    ------
    ValueError
        If ``amount`` is not positive.
    ExchangeRateError
        If FX retrieval fails.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    rate = get_exchange_rate("USD", currency)
    return float(amount) * rate
