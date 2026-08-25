"""
qoe.metrics — working-capital, cash-conversion, and earnings-quality metrics for SMCI.

Wires the FactSet (via qoe.labels) into finlib.diagnostics (pure math). Every output is
DERIVED from FILED facts and is reproducible. Uses AVERAGE balances for turnover ratios where
a prior period exists, and states that convention here so it isn't buried.
"""
from __future__ import annotations
from dataclasses import dataclass
from finlib.facts import FactSet
from finlib import diagnostics as dx
from . import labels as L


@dataclass
class PeriodMetrics:
    period: str
    dso: float
    dio: float
    dpo: float
    ccc: float
    nwc: float                 # net working capital (peg definition)
    nwc_pct_revenue: float
    accruals_ratio: float | None  # needs avg assets -> None for the first period
    cash_ebitda_proxy: float   # operating income + D&A - capex - dNWC (unlevered cash proxy)


def nwc(fs: FactSet, p: str) -> float:
    """
    Net working capital for peg purposes:
      AR + Inventory + Prepaid - AP - Accrued - Deferred revenue (current).
    Excludes cash, debt, and income taxes by convention (cash-free/debt-free).
    """
    return (L.ar(fs, p) + L.inventory(fs, p) + L.prepaid(fs, p)
            - L.ap(fs, p) - L.accrued(fs, p) - L.deferred_rev(fs, p))


def compute(fs: FactSet, periods=("FY2023", "FY2024", "FY2025")) -> list[PeriodMetrics]:
    out = []
    for i, p in enumerate(periods):
        prev = periods[i - 1] if i > 0 else None

        # Turnover on average balances where a prior period exists, else period-end.
        if prev:
            ar_b = dx.avg(L.ar(fs, p), L.ar(fs, prev))
            inv_b = dx.avg(L.inventory(fs, p), L.inventory(fs, prev))
            ap_b = dx.avg(L.ap(fs, p), L.ap(fs, prev))
        else:
            ar_b, inv_b, ap_b = L.ar(fs, p), L.inventory(fs, p), L.ap(fs, p)

        dso = dx.dso(ar_b, L.revenue(fs, p))
        dio = dx.dio(inv_b, L.cogs(fs, p))
        dpo = dx.dpo(ap_b, L.cogs(fs, p))
        ccc = dx.ccc(dso, dio, dpo)

        this_nwc = nwc(fs, p)
        nwc_pct = this_nwc / L.revenue(fs, p)

        # Accruals ratio needs average total assets (needs prior period).
        acc = None
        if prev:
            acc = dx.accruals_ratio_cf(
                L.net_income(fs, p), L.cfo(fs, p),
                dx.avg(L.total_assets(fs, p), L.total_assets(fs, prev)))

        # Unlevered cash proxy: OI + D&A - capex - increase in NWC.
        d_nwc = (this_nwc - nwc(fs, prev)) if prev else 0.0
        cash_ebitda = (L.operating_income(fs, p) + L.dna(fs, p)
                       - L.capex(fs, p) - d_nwc)

        out.append(PeriodMetrics(
            period=p, dso=dso, dio=dio, dpo=dpo, ccc=ccc,
            nwc=this_nwc, nwc_pct_revenue=nwc_pct,
            accruals_ratio=acc, cash_ebitda_proxy=cash_ebitda))
    return out


def related_party_exposure(fs: FactSet, periods=("FY2023", "FY2024", "FY2025")):
    """RP purchases as % of total COGS, and the $ EBITDA sensitivity to 100bps of pricing."""
    rows = []
    for p in periods:
        rp = L.rp_cogs(fs, p)
        tot = L.cogs(fs, p)
        rows.append({
            "period": p, "rp_cogs": rp, "total_cogs": tot,
            "pct_of_cogs": rp / tot,
            "ebitda_per_100bps": rp * 0.01,  # 1% pricing swing on RP COGS
        })
    return rows
