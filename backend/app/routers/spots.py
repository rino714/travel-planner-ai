from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.spot import Spot
from app.schemas.spot import SpotCreate, SpotResponse

router = APIRouter(tags=["spots"])


@router.post("/spots", response_model=SpotResponse, status_code=201)
def create_spot(spot_in: SpotCreate, db: Session = Depends(get_db)):
    spot = Spot(
        name=spot_in.name,
        address=spot_in.address,
        lat=spot_in.lat,
        lng=spot_in.lng,
    )
    db.add(spot)
    db.commit()
    db.refresh(spot)
    return spot


@router.get("/spots", response_model=list[SpotResponse])
def list_spots(db: Session = Depends(get_db)):
    return db.query(Spot).order_by(Spot.created_at.desc()).all()


@router.delete("/spots/{spot_id}", status_code=204)
def delete_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    db.delete(spot)
    db.commit()
