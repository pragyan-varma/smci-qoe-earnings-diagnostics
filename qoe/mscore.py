"""
qoe.mscore — Beneish M-score for SMCI, wired from the FactSet into finlib.diagnostics.

Computed for FY2024 (vs FY2023) and FY2025 (vs FY2024) — the years for which both t and t-1 are
fully sourced. Every component is exposed, because the score is a screen, not a verdict: a
hyper-growth hardware company scores high on SGI and TATA for entirely benign reasons, and you
must be able to say which components drive the number and why.

Caveats stated honestly:
- DEPI uses cash-flow D&A as the depreciation proxy (SMCI does not separately tag depreciation);
  amortization is immaterial for an asset-light model, and DEPI's coefficient is small (0.115).
- The M-score was calibrated on manufacturers; treat SMCI's result as directional.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from finlib.facts import FactSet
from finlib import diagnostics as dx
from . import labels as L


def _ppe_net(fs, p):   return fs.value("Property plant and equipment net", p)
def _ppe_gross(fs, p): return fs.value("Property plant and equipment gross", p)


@dataclass
class MScore:
    period: str
    prior: str
    DSRI: float
    GMI: float
    AQI: float
    SGI: float
    DEPI: float
    SGAI: float
    TATA: float
    LVGI: float
    m_score: float
    flagged: bool

    def as_dict(self):
        return asdict(self)


def compute_mscore(fs: FactSet, period: str, prior: str) -> MScore:
    # helpers for the two years
    rev_t, rev_p = L.revenue(fs, period), L.revenue(fs, prior)
    ar_t, ar_p = L.ar(fs, period), L.ar(fs, prior)
    gp_t, gp_p = L.gross_profit(fs, period), L.gross_profit(fs, prior)
    ca_t, ca_p = L.cur_assets(fs, period), L.cur_assets(fs, prior)
    ta_t, ta_p = L.total_assets(fs, period), L.total_assets(fs, prior)
    tl_t, tl_p = L.total_liabs(fs, period), L.total_liabs(fs, prior)
    ni_t = L.net_income(fs, period)
    cfo_t = L.cfo(fs, period)
    sga_t, sga_p = L.sga(fs, period), L.sga(fs, prior)
    dep_t, dep_p = L.dna(fs, period), L.dna(fs, prior)          # proxy: CF D&A
    ppeg_t, ppeg_p = _ppe_gross(fs, period), _ppe_gross(fs, prior)
    ppen_t, ppen_p = _ppe_net(fs, period), _ppe_net(fs, prior)

    dsri = dx.dsri(ar_t, rev_t, ar_p, rev_p)
    gmi = dx.gmi(gp_p / rev_p, gp_t / rev_t)
    aqi = dx.aqi(ca_t, ppen_t, ta_t, ca_p, ppen_p, ta_p)
    sgi = dx.sgi(rev_t, rev_p)
    depi = dx.depi(dep_p, ppeg_p, dep_t, ppeg_t)
    sgai = dx.sgai(sga_t, rev_t, sga_p, rev_p)
    tata = dx.tata(ni_t, cfo_t, ta_t)
    lvgi = dx.lvgi(tl_t, ta_t, tl_p, ta_p)

    m = dx.m_score(dsri, gmi, aqi, sgi, depi, sgai, tata, lvgi)
    return MScore(period, prior, dsri, gmi, aqi, sgi, depi, sgai, tata, lvgi,
                  m, flagged=m > dx.M_SCORE_THRESHOLD)


def compute_all(fs: FactSet) -> list[MScore]:
    return [compute_mscore(fs, "FY2024", "FY2023"),
            compute_mscore(fs, "FY2025", "FY2024")]
