"""
Webhooks Router
- POST /webhook/call-ended - ElevenLabs post-call webhook
"""

import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
from app.services.supabase import supabase
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

WEBHOOK_SECRET = os.getenv("ELEVENLABS_WEBHOOK_SECRET")


def verify_webhook_signature(payload: bytes, signature: Optional[str]) -> bool:
    """
    Verify the webhook signature from ElevenLabs.
    Returns True if signature is valid or if no secret is configured.
    """
    if not WEBHOOK_SECRET:
        # No verification if secret not configured
        return True
    
    if not signature:
        return False
    
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/call-ended")
async def call_ended_webhook(
    request: Request,
    x_elevenlabs_signature: Optional[str] = Header(None)
):
    """
    ElevenLabs sends this webhook at the end of each call
    with the complete transcript.
    """
    body = await request.body()
    
    # Verify signature if configured
    if not verify_webhook_signature(body, x_elevenlabs_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    data = await request.json()
    
    call_id = data.get("call_id")
    transcript = data.get("transcript")
    duration = data.get("duration")
    caller_phone = data.get("caller_phone")
    
    if not supabase:
        # Demo mode - just log
        print(f"📞 Call ended: {call_id}")
        print(f"   Duration: {duration}s")
        print(f"   Phone: {caller_phone}")
        print(f"   Transcript: {transcript[:100] if transcript else 'N/A'}...")
        return {"status": "ok", "message": "Logged (demo mode)"}
    
    try:
        # Save transcript to database
        supabase.table("call_logs").insert({
            "call_id": call_id,
            "transcript": transcript,
            "duration": duration,
            "caller_phone": caller_phone
        }).execute()
        
        return {"status": "ok", "message": "Call log saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
