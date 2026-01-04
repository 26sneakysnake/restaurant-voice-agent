"""
FastAPI Application - Restaurant Voice Agent Backend
Handles webhooks from ElevenLabs Conversational AI Agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import reservations, menu, orders, webhooks, info

app = FastAPI(
    title="Restaurant Voice Agent API",
    description="Backend API for ElevenLabs Conversational AI integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reservations.router, prefix="/api", tags=["Reservations"])
app.include_router(menu.router, prefix="/api", tags=["Menu"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(info.router, prefix="/api", tags=["Restaurant Info"])
app.include_router(webhooks.router, prefix="/webhook", tags=["Webhooks"])


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Restaurant Voice Agent API - Chez Marcel",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
