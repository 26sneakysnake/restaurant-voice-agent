"""
Reservations Router
- POST /api/availability - Check table availability
- POST /api/reservations - Create reservation
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AvailabilityRequest, AvailabilityResponse,
    ReservationRequest, ReservationResponse
)
from app.services.supabase import supabase

router = APIRouter()

# Restaurant configuration
MAX_CAPACITY = 50  # Maximum seats at the restaurant


@router.post("/availability", response_model=AvailabilityResponse)
async def check_availability(req: AvailabilityRequest):
    """
    Check if a table is available for the given date, time, and party size.
    Called by ElevenLabs agent before making a reservation.
    """
    if not supabase:
        # Demo mode without DB
        return AvailabilityResponse(
            available=True,
            message=f"Table disponible pour {req.party_size} personnes le {req.date} à {req.time}."
        )
    
    try:
        # Check existing reservations for the same date and time
        result = supabase.table("reservations")\
            .select("party_size")\
            .eq("date", req.date)\
            .eq("time", req.time)\
            .eq("status", "confirmed")\
            .execute()
        
        current_bookings = sum([r["party_size"] for r in result.data])
        available = (current_bookings + req.party_size) <= MAX_CAPACITY
        
        if available:
            return AvailabilityResponse(
                available=True,
                message=f"Parfait ! Une table pour {req.party_size} personnes est disponible le {req.date} à {req.time}."
            )
        else:
            return AvailabilityResponse(
                available=False,
                message=f"Désolé, nous sommes complets pour ce créneau. Voulez-vous essayer un autre horaire ?"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reservations", response_model=ReservationResponse)
async def create_reservation(req: ReservationRequest):
    """
    Create a new reservation.
    Called by ElevenLabs agent after availability is confirmed.
    """
    if not supabase:
        # Demo mode without DB
        return ReservationResponse(
            success=True,
            message=f"Réservation confirmée pour {req.guest_name}, le {req.date} à {req.time} pour {req.party_size} personnes. À bientôt chez Marcel !",
            reservation_id="demo-123"
        )
    
    try:
        result = supabase.table("reservations").insert({
            "guest_name": req.guest_name,
            "phone": req.phone,
            "date": req.date,
            "time": req.time,
            "party_size": req.party_size,
            "status": "confirmed"
        }).execute()
        
        reservation_id = result.data[0]["id"]
        
        return ReservationResponse(
            success=True,
            message=f"Parfait ! Réservation confirmée pour {req.guest_name}, le {req.date} à {req.time} pour {req.party_size} personnes. À bientôt chez Marcel !",
            reservation_id=reservation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
