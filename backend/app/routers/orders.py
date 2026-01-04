"""
Orders Router
- POST /api/orders - Place a takeaway order
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import OrderRequest, OrderResponse
from app.services.supabase import supabase

router = APIRouter()


@router.post("/orders", response_model=OrderResponse)
async def place_order(req: OrderRequest):
    """
    Place a takeaway order.
    Called by ElevenLabs agent when customer wants to order food for pickup.
    """
    # Calculate total
    total = sum(item.price * item.quantity for item in req.items)
    
    # Format items list for display
    items_summary = ", ".join([f"{item.quantity}x {item.name}" for item in req.items])
    
    if not supabase:
        # Demo mode without DB
        return OrderResponse(
            success=True,
            message=f"Commande confirmée pour {req.customer_name} ! {items_summary}. Total: {total:.2f}€. Prête dans environ 30 minutes.",
            order_id="demo-order-456",
            total=total
        )
    
    try:
        result = supabase.table("orders").insert({
            "customer_name": req.customer_name,
            "phone": req.phone,
            "items": [item.model_dump() for item in req.items],
            "total": total,
            "status": "pending"
        }).execute()
        
        order_id = result.data[0]["id"]
        
        return OrderResponse(
            success=True,
            message=f"Commande confirmée pour {req.customer_name} ! {items_summary}. Total: {total:.2f}€. Votre commande sera prête dans environ 30 minutes.",
            order_id=order_id,
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
