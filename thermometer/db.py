import os
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy import FLOAT, UUID, ForeignKey, DateTime, BOOLEAN
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql import func

db_engine = create_engine(os.getenv("DATABASE_URL"), echo=False)


# MODELS
class Base(DeclarativeBase):
    pass


class Thermometer(Base):
    __tablename__ = "thermometer_table"
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    freezing_threshold = mapped_column(FLOAT, default=0.0)
    boiling_threshold = mapped_column(FLOAT, default=10.0)
    ignore_notifs_within_range = mapped_column(FLOAT, default=0.0)
    notify_from_below_freezing = mapped_column(BOOLEAN, default=True)
    notify_from_above_freezing = mapped_column(BOOLEAN, default=True)
    notify_from_below_boiling = mapped_column(BOOLEAN, default=True)
    notify_from_above_boiling = mapped_column(BOOLEAN, default=True)

    # ForeignKeys & Associations
    temperatures = relationship("Temperature", back_populates="thermometer")


class Temperature(Base):
    __tablename__ = "temperature_table"
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    temperature = mapped_column(FLOAT, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    # ForeignKeys & Associations
    thermometer_id = mapped_column(ForeignKey("thermometer_table.id"))
    thermometer = relationship("Thermometer", back_populates="temperatures")


# Create Tables
Base.metadata.create_all(db_engine)

# Connect to postgres DB
connection = db_engine.connect()
