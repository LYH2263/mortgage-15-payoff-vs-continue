import json
import pytest
from app.engines.amortization import equal_payment_schedule, payoff_comparison

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

def test_payoff_compare_basic():
    c = payoff_comparison(1_000_000, 3.5, 360, 12)
    rows = equal_payment_schedule(1_000_000, 3.5, 360)["rows"]
    assert c["elapsed"] == 12
    assert c["remaining_principal"] == rows[11]["balance"]
    assert c["remaining_interest"] == round(sum(r["interest"] for r in rows[12:]), 2)
    assert c["payoff_amount"] == c["remaining_principal"]
    assert c["excess_interest"] == round(c["remaining_principal"] + c["remaining_interest"] - c["payoff_amount"], 2)

def test_payoff_compare_last_allowed_period():
    c = payoff_comparison(120000, 0, 12, 11)
    assert c["remaining_principal"] == 10000.0
    assert c["remaining_interest"] == 0
    assert c["excess_interest"] == 0

def test_payoff_compare_elapsed_out_of_range():
    for bad in (0, -1, 12, 13):
        with pytest.raises(ValueError):
            payoff_comparison(100000, 3.5, 12, bad)

def _service(tmp_path, monkeypatch):
    import app.db as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "t.db")
    from app import seed
    seed.init_db()
    from app.services.mortgage_service import MortgageService
    return MortgageService()

def test_payoff_compare_persist_and_reject(tmp_path, monkeypatch):
    with _service(tmp_path, monkeypatch) as s:
        before = len(s.history(100))
        with pytest.raises(ValueError):
            s.payoff_compare(100000, 3.5, 12, 12, None, True)
        assert len(s.history(100)) == before
        out = s.payoff_compare(100000, 3.5, 12, 6, None, True)
        rec = [x for x in s.history(100) if x["id"] == out["run_id"]][0]
        assert rec["kind"] == "payoff_compare"
        stored = json.loads(rec["result_json"])
        for k in ("remaining_principal", "remaining_interest", "payoff_amount"):
            assert stored[k] == out[k]
        trial = s.payoff_compare(100000, 3.5, 12, 6, None, False)
        assert trial["run_id"] is None
        assert len(s.history(100)) == before + 1

def test_payoff_compare_rate_change_only_affects_new(tmp_path, monkeypatch):
    with _service(tmp_path, monkeypatch) as s:
        a = s.payoff_compare(1_000_000, 3.5, 360, 60, None, True)
        b = s.payoff_compare(1_000_000, 6.0, 360, 60, None, True)
        assert a["remaining_interest"] != b["remaining_interest"]
        rec_a = [x for x in s.history(200) if x["id"] == a["run_id"]][0]
        stored = json.loads(rec_a["result_json"])
        assert stored["remaining_interest"] == a["remaining_interest"]
        assert stored["payoff_amount"] == a["payoff_amount"]
