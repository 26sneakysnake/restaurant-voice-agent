"""
Menu Router
- GET /api/menu - Get menu items (with optional category filter)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.schemas import MenuItem, MenuResponse
from app.services.supabase import supabase

router = APIRouter()

# Demo menu for when Supabase is not configured
DEMO_MENU = [
    MenuItem(id="1", name="Soupe à l'oignon gratinée", description="Soupe traditionnelle avec croûtons et fromage gratiné", price=8.50, category="entrées", allergens=["gluten", "lactose"]),
    MenuItem(id="2", name="Escargots de Bourgogne", description="6 escargots au beurre persillé", price=12.00, category="entrées", allergens=["lactose"]),
    MenuItem(id="3", name="Foie gras maison", description="Servi avec chutney de figues et toast", price=18.00, category="entrées", allergens=["gluten"]),
    MenuItem(id="4", name="Boeuf Bourguignon", description="Mijoté au vin rouge, carottes et champignons", price=24.00, category="plats", allergens=[]),
    MenuItem(id="5", name="Confit de canard", description="Cuisse confite, pommes sarladaises", price=22.00, category="plats", allergens=[]),
    MenuItem(id="6", name="Sole meunière", description="Sole entière, beurre citronné, pommes vapeur", price=28.00, category="plats", allergens=["lactose", "poisson"]),
    MenuItem(id="7", name="Steak frites", description="Entrecôte 300g, frites maison, sauce au poivre", price=26.00, category="plats", allergens=["lactose"]),
    MenuItem(id="8", name="Crème brûlée", description="À la vanille de Madagascar", price=9.00, category="desserts", allergens=["lactose", "oeufs"]),
    MenuItem(id="9", name="Tarte Tatin", description="Tarte aux pommes caramélisées, crème fraîche", price=10.00, category="desserts", allergens=["gluten", "lactose"]),
    MenuItem(id="10", name="Fondant au chocolat", description="Coeur coulant, glace vanille", price=11.00, category="desserts", allergens=["gluten", "lactose", "oeufs"]),
]


@router.get("/menu", response_model=MenuResponse)
async def get_menu(category: Optional[str] = Query(None, description="Filter by category: entrées, plats, desserts")):
    """
    Get the restaurant menu.
    Called by ElevenLabs agent when customer asks about dishes.
    """
    if not supabase:
        # Demo mode without DB
        items = DEMO_MENU
        if category:
            items = [item for item in items if item.category.lower() == category.lower()]
        return MenuResponse(items=items, category=category)
    
    try:
        query = supabase.table("menu_items").select("*").eq("available", True)
        
        if category:
            query = query.eq("category", category.lower())
        
        result = query.execute()
        
        items = [
            MenuItem(
                id=str(item["id"]),
                name=item["name"],
                description=item.get("description"),
                price=float(item["price"]),
                category=item["category"],
                allergens=item.get("allergens", []),
                available=item.get("available", True)
            )
            for item in result.data
        ]
        
        return MenuResponse(items=items, category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
