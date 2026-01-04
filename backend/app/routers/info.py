"""
Restaurant Info Router
- GET /api/restaurant-info - Get restaurant information
"""

from fastapi import APIRouter
from app.models.schemas import RestaurantInfo, RestaurantHours

router = APIRouter()

# Restaurant configuration
RESTAURANT_INFO = RestaurantInfo(
    name="Chez Marcel",
    address="12 Rue de la Paix, 75002 Paris",
    phone="+33 1 23 45 67 89",
    email="contact@chezmarcel.fr",
    hours=RestaurantHours(
        monday="12:00-14:30, 19:00-22:30",
        tuesday="12:00-14:30, 19:00-22:30",
        wednesday="12:00-14:30, 19:00-22:30",
        thursday="12:00-14:30, 19:00-22:30",
        friday="12:00-14:30, 19:00-23:00",
        saturday="12:00-15:00, 19:00-23:00",
        sunday="Fermé"
    ),
    capacity=50
)


@router.get("/restaurant-info", response_model=RestaurantInfo)
async def get_restaurant_info():
    """
    Get restaurant information (address, hours, contact).
    Called by ElevenLabs agent when customer asks about the restaurant.
    """
    return RESTAURANT_INFO
