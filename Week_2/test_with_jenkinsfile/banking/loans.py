"""Loan processing utilities.

Intentionally simple: loan approval is based solely on a mocked credit score.
Tests patch :func:`check_credit_score` to simulate outcomes.
"""
from __future__ import annotations


def check_credit_score(customer_id: str) -> int:
    """Return a pretend credit score for the given ``customer_id``.

    In production this would call a bureau or scoring service. Kept as a stub
    so tests can patch it.
    """
    # Side-effect like I/O is omitted to keep logic deterministic in tests.
    return 750


def process_loan_application(customer_id: str, amount: float) -> str:
    """Approve or reject a loan based on a simple score threshold.

    Parameters
    ----------
    customer_id : str
        Applicant identifier (not used in the demo logic).
    amount : float
        Requested principal (not used in the demo logic).

    Returns
    -------
    str
        "Approved" if score > 700, else "Rejected".
    """
    score = check_credit_score(customer_id)
    return "Approved" if score > 700 else "Rejected"
