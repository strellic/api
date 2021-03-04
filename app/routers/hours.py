from fastapi import APIRouter
from ocflib.lab.staff_hours import get_staff_hours
from ocflib.lab.hours import read_hours_listing

router = APIRouter()


@router.get("/staff", tags=["hours"])
async def staff_hours():
    hours = get_staff_hours()
    return [h._asdict() for h in hours]


@router.get("/today", tags=["hours"])
async def today_hours():
    return read_hours_listing().hours_on_date()
