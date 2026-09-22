from fastapi import APIRouter, HTTPException
from app.schemas.schedule import PayoffCompareRequest, ScheduleRequest
from app.services.mortgage_service import MortgageService
router = APIRouter()
@router.post("/schedule")
def post_schedule(body: ScheduleRequest):
    with MortgageService() as s:
        return s.schedule(body.principal, body.annual_rate, body.months, body.loan_id, body.persist, body.preview_rows)
@router.post("/payoff-compare")
def post_payoff_compare(body: PayoffCompareRequest):
    with MortgageService() as s:
        try:
            return s.payoff_compare(body.principal, body.annual_rate, body.months, body.elapsed, body.loan_id, body.persist)
        except ValueError:
            raise HTTPException(status_code=400, detail="elapsed 须在一到总期数减一之间")
