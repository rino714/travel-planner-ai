import json
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.spot import Spot
from app.models.trip import Trip, TripSpot
from app.schemas.trip import DaySchedule, ScheduleItem, TripCreate, TripResponse
from app.services.accommodation import suggest_accommodation
from app.services.route_optimizer import (
    estimate_travel_time_min,
    haversine_distance,
    optimize_route,
    split_spots_by_day,
)

router = APIRouter(tags=["trips"])

SPOT_VISIT_DURATION_MIN = 60  # 各スポットのデフォルト滞在時間
DAY_START_HOUR = 9  # 1日の開始時刻
DAY_END_HOUR = 18  # 1日の終了時刻（宿泊提案の目安）


def _build_schedule(
    spots: list[dict],
    start_date,
    days: int,
) -> list[dict]:
    """スポットリストからタイムスケジュールを生成する。"""
    optimized = optimize_route(spots)
    daily_spots = split_spots_by_day(optimized, days)

    schedule: list[dict] = []

    for day_idx, day_spots in enumerate(daily_spots):
        current_date = start_date + timedelta(days=day_idx)
        items: list[dict] = []
        current_minutes = DAY_START_HOUR * 60  # 分単位で管理

        for i, spot in enumerate(day_spots):
            # スポット訪問
            h, m = divmod(current_minutes, 60)
            items.append({
                "time": f"{h:02d}:{m:02d}",
                "type": "spot",
                "name": spot["name"],
                "duration_min": SPOT_VISIT_DURATION_MIN,
            })
            current_minutes += SPOT_VISIT_DURATION_MIN

            # 次のスポットへの移動
            if i < len(day_spots) - 1:
                next_spot = day_spots[i + 1]
                dist = haversine_distance(
                    spot["lat"], spot["lng"], next_spot["lat"], next_spot["lng"]
                )
                travel_min = estimate_travel_time_min(dist)

                h, m = divmod(current_minutes, 60)
                items.append({
                    "time": f"{h:02d}:{m:02d}",
                    "type": "move",
                    "name": f"{spot['name']} → {next_spot['name']}",
                    "from": spot["name"],
                    "to": next_spot["name"],
                    "duration_min": travel_min,
                })
                current_minutes += travel_min

        # 宿泊提案（最終日以外）
        if day_idx < days - 1 and day_spots:
            last_spot = day_spots[-1]
            accommodation = suggest_accommodation(last_spot["lat"], last_spot["lng"])
            end_h, end_m = divmod(max(current_minutes, DAY_END_HOUR * 60), 60)
            items.append({
                "time": f"{end_h:02d}:{end_m:02d}",
                "type": "accommodation",
                "name": accommodation,
                "duration_min": None,
            })

        schedule.append({
            "day": day_idx + 1,
            "date": current_date.isoformat(),
            "items": items,
        })

    return schedule


@router.post("/trips", response_model=TripResponse, status_code=201)
def create_trip(trip_in: TripCreate, db: Session = Depends(get_db)):
    # スポット取得
    spots = db.query(Spot).filter(Spot.id.in_(trip_in.spot_ids)).all()
    if not spots:
        raise HTTPException(status_code=400, detail="No valid spots found")

    found_ids = {s.id for s in spots}
    missing = [sid for sid in trip_in.spot_ids if sid not in found_ids]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Spots not found: {missing}",
        )

    spot_dicts = [
        {"id": s.id, "name": s.name, "lat": s.lat, "lng": s.lng}
        for s in spots
    ]

    schedule = _build_schedule(spot_dicts, trip_in.start_date, trip_in.days)

    # DB保存
    trip = Trip(
        start_date=trip_in.start_date,
        days=trip_in.days,
        schedule_json=json.dumps(schedule, ensure_ascii=False),
    )
    db.add(trip)
    db.flush()

    for spot in spots:
        db.add(TripSpot(trip_id=trip.id, spot_id=spot.id))

    db.commit()
    db.refresh(trip)

    return TripResponse(
        id=trip.id,
        start_date=trip.start_date,
        days=trip.days,
        schedule=[DaySchedule(**day) for day in schedule],
        created_at=trip.created_at,
    )


@router.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    schedule = json.loads(trip.schedule_json)
    return TripResponse(
        id=trip.id,
        start_date=trip.start_date,
        days=trip.days,
        schedule=[DaySchedule(**day) for day in schedule],
        created_at=trip.created_at,
    )
