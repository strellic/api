from fastapi import APIRouter
from ocflib.lab.stats import (
    get_connection,
    list_desktops,
    users_in_lab_count,
    staff_in_lab,
)
from ocflib.infra.hosts import hostname_from_domain

router = APIRouter()


@router.get("/desktops", tags=["lab"])
async def lab_desktops():
    public_desktops = list_desktops(public_only=True)

    with get_connection() as c:
        c.execute(
            "SELECT * FROM `desktops_in_use_public`;",
        )
    desktops_in_use = {hostname_from_domain(session["host"]) for session in c}

    return {
        "public_desktops_in_use": desktops_in_use.intersection(public_desktops),
        "public_desktops_num": len(public_desktops),
    }


@router.get("/num_users", tags=["lab"])
async def lab_users():
    return users_in_lab_count()


@router.get("/staff", tags=["lab"])
async def lab_staff():
    return staff_in_lab()
