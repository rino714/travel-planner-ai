from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import spots, trips

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spots.router, prefix="/api")
app.include_router(trips.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
