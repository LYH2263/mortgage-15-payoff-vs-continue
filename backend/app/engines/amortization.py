def equal_payment_schedule(principal: float, annual_rate: float, months: int) -> dict:
    P = float(principal)
    n = int(months)
    r = float(annual_rate) / 12.0 / 100.0
    if n <= 0:
        raise ValueError("months")
    if r == 0:
        pay = P / n
    else:
        pay = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
    rows = []
    bal = P
    interest_sum = 0.0
    for i in range(1, n + 1):
        interest = bal * r
        principal_part = pay - interest
        if i == n:
            principal_part = bal
            pay_i = principal_part + interest
        else:
            pay_i = pay
        bal = max(0.0, bal - principal_part)
        interest_sum += interest
        rows.append({
            "period": i,
            "payment": round(pay_i, 2),
            "principal": round(principal_part, 2),
            "interest": round(interest, 2),
            "balance": round(bal, 2),
        })
    return {
        "monthly_payment": round(pay if n else 0, 2),
        "total_interest": round(interest_sum, 2),
        "total_payment": round(sum(x["payment"] for x in rows), 2),
        "rows": rows,
    }

def settle_comparison(principal: float, annual_rate: float, months: int, paid_periods: int) -> dict:
    """第 P 期末一次性结清 vs 继续按原表还完的对照。

    P 须落在 1..months-1：第 0 期无已还期、最后一期已无剩余利息可对照。
    返回剩余本金（即一次性结清所需余额）、续还剩余利息、超额利息。
    """
    n = int(months)
    p = int(paid_periods)
    if p < 1 or p > n - 1:
        raise ValueError("paid_periods out of range")
    sched = equal_payment_schedule(principal, annual_rate, months)
    rows = sched["rows"]
    remaining_principal = rows[p - 1]["balance"]
    remaining_interest = round(sum(r["interest"] for r in rows[p:]), 2)
    settle_amount = remaining_principal
    extra_interest = remaining_interest
    return {
        "paid_periods": p,
        "remaining_principal": round(remaining_principal, 2),
        "remaining_interest": remaining_interest,
        "settle_amount": round(settle_amount, 2),
        "extra_interest": round(extra_interest, 2),
    }
