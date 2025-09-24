from typing import List, Optional, Tuple
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import desc, asc # type: ignore
from ..models.transaction import Transaction

MAX_LIMIT = 100

def list_by_account(
    db: Session,
    account_id: int,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    page: int = 1,
    limit: int = 25,
) -> List[Transaction]:
    # Enforce sensible pagination defaults & caps
    if limit is None:
        limit = 25
    limit = max(1, min(limit, MAX_LIMIT))
    page = max(1, page)
    offset = (page - 1) * limit

    # Finding all the records for a specific account
    query = db.query(Transaction).filter(Transaction.account_id == account_id)

    # Filtering
    if status:
        # Only show transactions with a specific status. or even you will consider type as international or domestic
        query = query.filter(Transaction.status == status)

    # Sorting
    # Expected format: field:direction (e.g., "date:desc", "amount:asc")
    sort_col = Transaction.date
    sort_dir = desc
    if sort_by:
        try:
            field, direction = sort_by.split(":")
            field = field.strip().lower()
            direction = direction.strip().lower()
        except ValueError:
            field, direction = sort_by.strip().lower(), "asc"

        column_map = {
            "date": Transaction.date,
            "amount": Transaction.amount,
            "id": Transaction.id,
            "status": Transaction.status,
        }
        sort_col = column_map.get(field, Transaction.date)
        sort_dir = desc if direction == "desc" else asc

    query = query.order_by(sort_dir(sort_col))

    # Pagination
    return query.offset(offset).limit(limit).all()
