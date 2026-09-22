import pytest
from app.engines.amortization import equal_payment_schedule, settle_comparison

def test_monthly_payment():
    s = equal_payment_schedule(1_000_000, 3.5, 360)
    assert s["monthly_payment"] == 4490.45

def test_first_period_interest():
    s = equal_payment_schedule(1_000_000, 3.5, 360)
    assert s["rows"][0]["interest"] == 2916.67
    assert s["rows"][0]["period"] == 1

def test_zero_rate():
    s = equal_payment_schedule(120000, 0, 12)
    assert s["monthly_payment"] == 10000.0

def test_bad_months():
    with pytest.raises(ValueError):
        equal_payment_schedule(100, 3, 0)

def test_settle_values():
    r = settle_comparison(1_000_000, 3.5, 360, 120)
    # 结清余额等于第 P 期末剩余本金
    assert r["remaining_principal"] == r["settle_amount"]
    # 续还相对一次性结清的超额利息即剩余利息合计
    assert r["extra_interest"] == r["remaining_interest"]
    assert 0 < r["remaining_principal"] < 1_000_000
    assert r["remaining_interest"] > 0

def test_settle_zero_rate():
    r = settle_comparison(120000, 0, 12, 6)
    assert r["remaining_principal"] == 60000.0
    assert r["remaining_interest"] == 0.0
    assert r["extra_interest"] == 0.0

def test_settle_near_last_period():
    r = settle_comparison(1_000_000, 3.5, 360, 359)
    assert r["remaining_interest"] == round(
        equal_payment_schedule(1_000_000, 3.5, 360)["rows"][359]["interest"], 2)

@pytest.mark.parametrize("p", [0, 360, 400, -1])
def test_settle_paid_periods_out_of_range(p):
    with pytest.raises(ValueError):
        settle_comparison(1_000_000, 3.5, 360, p)
