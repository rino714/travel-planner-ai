from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    trip_spots: Mapped[list["TripSpot"]] = relationship(back_populates="trip")


class TripSpot(Base):
    __tablename__ = "trip_spots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False)
    spot_id: Mapped[int] = mapped_column(ForeignKey("spots.id"), nullable=False)

    trip: Mapped["Trip"] = relationship(back_populates="trip_spots")
    spot: Mapped["Spot"] = relationship()


from app.models.spot import Spot  # noqa: E402, F401
