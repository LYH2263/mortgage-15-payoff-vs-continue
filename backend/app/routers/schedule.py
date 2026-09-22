from fastapi import APIRouter, HTTPException
from app.schemas.schedule import ScheduleRequest, SettleCompareRequest
from app.services.mortgage_service import MortgageService
router = APIRouter()
@router.post("/schedule")
def post_schedule(body: ScheduleRequest):
    with MortgageService() as s:
        return s.schedule(body.principal, body.annual_rate, body.months, body.loan_id, body.persist, body.preview_rows)
@router.post("/settle-compare")
def post_settle_compare(body: SettleCompareRequest):
    # P 须落在 1..months-1，越界拒绝且不写记录
    if body.paid_periods < 1 or body.paid_periods >= body.months:
        raise HTTPException(status_code=400, detail="paid_periods 须落在 1 到 总期数-1")
    try:
        with MortgageService() as s:
            return s.settle_compare(body.principal, body.annual_rate, body.months, body.paid_periods, body.loan_id, body.persist)
    except ValueError:
        raise HTTPException(status_code=400, detail="paid_periods 须落在 1 到 总期数-1")
