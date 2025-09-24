# Changelog


## v1.2 – Transactions API Enhancements
- Added `Transaction` model and schema
- Extended `GET /accounts/{account_id}/transactions` with **Filtering**, **Sorting**, and **Pagination**
- Enforced sensible defaults: `limit=25` and cap `limit<=100`
- Added tests covering filter/sort/pagination
- README updated with examples
