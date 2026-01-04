"""
Pydantic Models / Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


# ============ Reservations ============

class AvailabilityRequest(BaseModel):
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    party_size: int


class AvailabilityResponse(BaseModel):
    available: bool
    message: str


class ReservationRequest(BaseModel):
    guest_name: str
    phone: str
    date: str
    time: str
    party_size: int


class ReservationResponse(BaseModel):
    success: bool
    message: str
    reservation_id: Optional[str] = None


# ============ Menu ============

class MenuItem(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    category: str
    allergens: Optional[List[str]] = None
    available: bool = True


class MenuResponse(BaseModel):
    items: List[MenuItem]
    category: Optional[str] = None


# ============ Orders ============

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float


class OrderRequest(BaseModel):
    customer_name: str
    phone: str
    items: List[OrderItem]


class OrderResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[str] = None
    total: Optional[float] = None


# ============ Webhooks ============

class CallEndedWebhook(BaseModel):
    call_id: Optional[str] = None
    transcript: Optional[str] = None
    duration: Optional[int] = None
    caller_phone: Optional[str] = None


# ============ Restaurant Info ============

class RestaurantHours(BaseModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


class RestaurantInfo(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    hours: RestaurantHours
    capacity: int
