"""
Sales Reporting - Final Refactored Solution

This module demonstrates a clean, testable, and extensible design for generating sales reports.
Key improvements:
- Dependency Injection for data sources (IDataSource)
- Single Responsibility across data fetching, processing, and formatting
- Encapsulation: safe accessors return copies
- Flexible output via pluggable formatters (Open/Closed Principle)
- Clear data contracts with dataclasses
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Protocol, runtime_checkable
import json
import copy


# -----------------------------
# Data Model
# -----------------------------

@dataclass(frozen=True)
class SaleItem:
    """A simple, immutable data container for a sale record."""
    item: str
    quantity: int
    price: float

    @property
    def revenue(self) -> float:
        return self.quantity * self.price


# -----------------------------
# Data Sources
# -----------------------------

class IDataSource(ABC):
    """Interface for any data source that can provide sales data."""
    @abstractmethod
    def get_sales_data(self) -> List[SaleItem]:
        raise NotImplementedError


class MySqlDataSource(IDataSource):
    """A concrete implementation for a MySQL database."""
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def get_sales_data(self) -> List[SaleItem]:
        # NOTE: In real code, connect and fetch via a DB client.
        # This print is only illustrative.
        print(f"[MySqlDataSource] Connecting to {self._connection_string} and fetching data...")
        return [
            SaleItem(item="Laptop", quantity=2, price=1200.0),
            SaleItem(item="Mouse", quantity=5, price=25.0),
        ]


class InMemoryDataSource(IDataSource):
    """A simple in-memory data source (handy for tests and demos)."""
    def __init__(self, items: List[SaleItem] | None = None):
        self._items = items or []

    def get_sales_data(self) -> List[SaleItem]:
        return list(self._items)  # return a shallow copy


# -----------------------------
# Report Core
# -----------------------------

class SalesReport:
    """
    Processes sales data but does NOT handle fetching or formatting.
    Its single responsibility is holding the processed report data.
    """
    def __init__(self, user: str, source: IDataSource):
        self.user = user
        self._source = source
        self._items: List[SaleItem] = self._source.get_sales_data()

    @property
    def total_revenue(self) -> float:
        """Calculates total revenue from the items."""
        return sum(item.revenue for item in self._items)

    def get_items(self) -> List[SaleItem]:
        """Return a copy to prevent external modification."""
        return list(self._items)


# -----------------------------
# Formatters
# -----------------------------

class IReportFormatter(ABC):
    """Interface for any class that can format a SalesReport."""
    @abstractmethod
    def format(self, report: SalesReport) -> str:
        raise NotImplementedError


class PlainTextFormatter(IReportFormatter):
    def format(self, report: SalesReport) -> str:
        lines: List[str] = []
        lines.append(f"Sales Report for {report.user}")
        lines.append("---------------------------------")
        for item in report.get_items():
            lines.append(f"- Item: {item.item}, Quantity: {item.quantity}, Unit Price: ${item.price:,.2f}, Revenue: ${item.revenue:,.2f}")
        lines.append("---------------------------------")
        lines.append(f"Total Revenue: ${report.total_revenue:,.2f}")
        return "\n".join(lines)


class JsonFormatter(IReportFormatter):
    def format(self, report: SalesReport) -> str:
        payload: Dict = {
            "report_user": report.user,
            "total_revenue": report.total_revenue,
            "items": [
                {"item": i.item, "quantity": i.quantity, "price": i.price, "revenue": i.revenue}
                for i in report.get_items()
            ],
        }
        return json.dumps(payload, indent=2)


class CsvFormatter(IReportFormatter):
    """Optional: demonstrate easy extensibility with CSV output."""
    def format(self, report: SalesReport) -> str:
        # Simple CSV with header
        rows: List[str] = ["item,quantity,price,revenue"]
        for i in report.get_items():
            rows.append(f"{i.item},{i.quantity},{i.price},{i.revenue}")
        # You might include total on last line or separate footers in a real CSV export.
        return "\n".join(rows)


# -----------------------------
# Example usage
# -----------------------------

def _example() -> None:
    # 1) Choose your data source
    mysql_source = MySqlDataSource("mysql://user:pass@localhost/sales")

    # 2) Create the report object, injecting the dependency
    report = SalesReport("admin_user", source=mysql_source)

    # 3) Choose your desired output format and format the report
    text_formatter = PlainTextFormatter()
    json_formatter = JsonFormatter()
    csv_formatter = CsvFormatter()

    print("--- Plain Text Report ---")
    print(text_formatter.format(report))

    print("\n--- JSON Report ---")
    print(json_formatter.format(report))

    print("\n--- CSV Report ---")
    print(csv_formatter.format(report))


if __name__ == "__main__":
    _example()
