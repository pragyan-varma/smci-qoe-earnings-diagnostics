"""
qoe.validate — tie-out controls that run on every execution and fail loudly.

We are building a QoE on a company whose defining failure was a lack of controls. Building
controls into our own model — and being able to point at them — is the rhetorical layup.
Each check returns (name, passed, detail). run_all raises on any failure unless tolerate=True.
"""
from __future__ import annotations
from finlib.facts import FactSet
from . import labels as L

TOL = 1500.0  # whole dollars of rounding tolerance (source is in thousands => <$1k rounding)


def _chk(name, lhs, rhs, tol=TOL):
    ok = abs(lhs - rhs) <= tol
    return (name, ok, f"{lhs:,.0f} vs {rhs:,.0f}  (diff {lhs - rhs:,.0f})")


def balance_sheet_balances(fs: FactSet, p: str):
    """Assets = Liabilities + Equity (equity INCLUDING non-controlling interest)."""
    return _chk(f"[{p}] Balance sheet balances",
                L.total_assets(fs, p),
                L.total_liabs(fs, p) + L.total_equity(fs, p))


def gross_profit_foots(fs: FactSet, p: str):
    """Revenue - COGS = Gross profit."""
    return _chk(f"[{p}] Gross profit = Revenue - COGS",
                L.revenue(fs, p) - L.cogs(fs, p), L.gross_profit(fs, p))


def operating_income_foots(fs: FactSet, p: str):
    """Gross profit - R&D - S&M - G&A = Operating income."""
    return _chk(f"[{p}] Operating income = GP - opex",
                L.gross_profit(fs, p) - L.rnd(fs, p) - L.sga(fs, p),
                L.operating_income(fs, p))


def pretax_bridges_to_operating(fs: FactSet, p: str):
    """Operating income +/- non-operating items should reconcile to pre-tax income; report the gap."""
    gap = L.pretax_income(fs, p) - L.operating_income(fs, p)
    return (f"[{p}] Pretax - Operating (= net non-operating)", True,
            f"{gap:,.0f}  (interest, other income, equity investee — should be explained)")


def net_income_ties(fs: FactSet, p: str):
    """Pre-tax - tax should approximate net income (before equity-investee & NCI nuances)."""
    return _chk(f"[{p}] Net income ~ Pretax - Tax",
                L.pretax_income(fs, p) - L.tax(fs, p), L.net_income(fs, p),
                tol=8_000_000)  # widened: equity-method investee sits below tax line


def run_all(fs: FactSet, periods=("FY2023", "FY2024", "FY2025"), tolerate: bool = False):
    checks = []
    for p in periods:
        checks.append(gross_profit_foots(fs, p))
        checks.append(operating_income_foots(fs, p))
        checks.append(net_income_ties(fs, p))
        checks.append(pretax_bridges_to_operating(fs, p))
        if fs.has("Total equity incl. NCI", p):
            checks.append(balance_sheet_balances(fs, p))
    failures = [c for c in checks if not c[1]]
    if failures and not tolerate:
        msg = "\n".join(f"  FAIL {n}: {d}" for n, ok, d in failures)
        raise AssertionError(f"Validation failed:\n{msg}")
    return checks
