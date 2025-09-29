# Detailed Requirements

See summary:
- CRUD for Practitioner, Slot
- GET /api/v1/slots filters: available, practitioner_id, date_from/date_to, limit/offset, sort_by (start_time|end_time), order (asc|desc)
- POST /api/v1/slots/{id}/book with 409 on already booked
- Pydantic settings for DATABASE_URL
- Global exception handler (JSON {detail: ...})
- ORM only / parameterized access; avoid raw string SQL
