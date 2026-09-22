from pydantic import BaseModel, Field
class ScheduleRequest(BaseModel):
    principal: float = Field(gt=0)
    annual_rate: float = Field(ge=0)
    months: int = Field(gt=0, le=600)
    loan_id: int | None = None
    persist: bool = True
    preview_rows: int = Field(default=12, ge=1, le=120)
class SettleCompareRequest(BaseModel):
    principal: float = Field(gt=0)
    annual_rate: float = Field(ge=0)
    months: int = Field(gt=0, le=600)
    paid_periods: int = Field(ge=1, description="已过期数 P，须小于总期数")
    loan_id: int | None = None
    persist: bool = False
