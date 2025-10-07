from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, status, Header, APIRouter, Request
from sqlalchemy.orm import Session
import uuid
import time

from database import Base, engine, get_db, init_db
from models import Order, User, RoleEnum
from schemas import OrderCreate, OrderOut, UserOut
from auth import get_current_user, auth_router
from services.payment_service import PaymentService
from services.notification_service import send_order_notification
from utils.decorators import log_operation
from utils.exceptions import PaymentFailed, AppException, register_exception_handlers
from utils.logging import configure_logging, get_logger, set_correlation_id

logger = get_logger(__name__)

# Initialize DB on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure JSON logging first so all startup logs are structured
    configure_logging()
    logger.info("Starting FIL Order Service")
    init_db()
    yield
    logger.info("Shutting down FIL Order Service")

app = FastAPI(title="FIL Order Service", version="1.1.0", lifespan=lifespan)

# Include auth routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Register exception handlers
register_exception_handlers(app)

# ---- Request/Response logging middleware with correlation id ----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Correlation id from header or generated
    cid = request.headers.get("x-request-id") or str(uuid.uuid4())
    set_correlation_id(cid)

    start = time.time()
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.time() - start) * 1000)
        # Attach correlation id to response for traceability
        response.headers["x-request-id"] = cid
        logger.info(
            "request_completed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": getattr(response, "status_code", 0),
                "duration_ms": duration_ms,
            },
        )

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
@log_operation("create_order")
def create_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_simulate_payment_failure: Optional[str] = Header(default=None),
):
    '''
    Create an order transactionally. Simulates an external payment service.
    Uses BackgroundTasks to send async notification on success.
    '''
    try:
        logger.info("create_order_received", extra={"user_id": current_user.id})
        # Persist the order in "pending" state
        order = Order(
            user_id=current_user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            price=payload.price,
            status="pending",
        )
        db.add(order)
        db.flush()  # get order.id

        payment_service = PaymentService(simulate_failure=bool(x_simulate_payment_failure))
        amount = payload.quantity * payload.price
        ok = payment_service.process_payment(amount=amount, user_id=current_user.id)
        if not ok:
            logger.warning("payment_failed", extra={"user_id": current_user.id, "order_id": order.id})
            raise PaymentFailed("Payment processing failed, transaction rolled back")

        # mark as confirmed
        order.status = "confirmed"
        db.commit()
        db.refresh(order)

        logger.info("order_confirmed", extra={"user_id": current_user.id, "order_id": order.id})

        # kick off async notification
        background_tasks.add_task(send_order_notification, current_user.email, order.id)

        return order
    except PaymentFailed:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.exception("unexpected_error_create_order", extra={"user_id": current_user.id})
        raise AppException(f"Unexpected error while creating order: {str(e)}")


@router.get("", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Admin can see all orders; normal users only see their own.
    '''
    query = db.query(Order)
    if current_user.role != RoleEnum.admin:
        query = query.filter(Order.user_id == current_user.id)
    orders = query.order_by(Order.id.desc()).all()
    logger.info("list_orders", extra={"user_id": current_user.id})
    return orders


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        logger.warning("order_not_found", extra={"user_id": current_user.id, "order_id": order_id})
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != RoleEnum.admin and order.user_id != current_user.id:
        logger.warning("forbidden_order_access", extra={"user_id": current_user.id, "order_id": order_id})
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    logger.info("get_order", extra={"user_id": current_user.id, "order_id": order_id})
    return order


app.include_router(router)

@app.get("/", tags=["health"])
def health():
    logger.info("health_check")
    return {"status": "ok"}
