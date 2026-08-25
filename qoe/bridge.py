"""
qoe.bridge — the three-tier EBITDA walk.

    GAAP EBITDA
      +/- management-tier adjustments   -> Management-basis EBITDA (e.g. pre-SBC)
      +/- diligence-tier adjustments    -> Diligence Adjusted EBITDA (what we underwrite)
      +/- sensitivity items (range)     -> shown as a band, NOT booked

Adjustments are declarative (data/source/adjustments.yaml). Each must carry a rationale and a
counterargument or it will not load. Values come from the FactSet (source_fact) or explicit
`values`; an ACCEPT/REJECT adjustment whose value is null RAISES rather than booking zero.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
import yaml

from finlib.facts import FactSet
from . import labels as L

_ADJ_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "source", "adjustments.yaml")


def gaap_ebitda(fs: FactSet, period: str) -> float:
    """
    GAAP EBITDA = Operating income + D&A.
    Starting from OPERATING income (not net income) deliberately excludes interest income,
    other income, and the equity-method investee — none of which are operating. This sidesteps
    the interest-income-inflation trap. D&A is the cash-flow-statement line; for SMCI it is small
    and unlevered (asset-light model), so no debt-issuance-cost double-count risk of note.
    """
    return L.operating_income(fs, period) + L.dna(fs, period)


@dataclass
class Adjustment:
    id: str
    name: str
    tier: str
    treatment: str
    direction: str
    basis: str
    rationale: str
    counterargument: str
    market_practice: str
    source_fact: str | None = None
    values: dict | None = None
    sensitivity_bps: int | None = None

    REQUIRED = ("rationale", "counterargument", "market_practice")

    def signed_value(self, fs: FactSet, period: str) -> float | None:
        """Per-period signed dollar impact, or None if unquantifiable from sourced data."""
        raw = self._raw_value(fs, period)
        if raw is None:
            return None
        return raw if self.direction == "add_back" else -abs(raw)

    def _raw_value(self, fs: FactSet, period: str) -> float | None:
        if self.source_fact:
            if self.sensitivity_bps:  # exposure * bps -> a sensitivity magnitude
                return fs.value(self.source_fact, period) * (self.sensitivity_bps / 10_000)
            return fs.value(self.source_fact, period)
        if self.values:
            v = self.values.get(period)
            return None if v is None else float(v)
        return None


def load_adjustments(path: str = _ADJ_PATH) -> list[Adjustment]:
    with open(path) as fh:
        raw = yaml.safe_load(fh)
    adjs = []
    for d in raw:
        for req in Adjustment.REQUIRED:
            if not d.get(req):
                raise ValueError(f"Adjustment {d.get('id')} missing required field '{req}'. "
                                 f"Every adjustment must state its rationale AND counterargument.")
        adjs.append(Adjustment(**d))
    return adjs


@dataclass
class BridgeLine:
    id: str
    name: str
    tier: str
    treatment: str
    value: float | None      # None => unquantifiable / not booked
    booked: bool             # did it move the underwritten number?
    note: str = ""


@dataclass
class Bridge:
    period: str
    gaap_ebitda: float
    lines: list[BridgeLine] = field(default_factory=list)

    def _booked(self, management_tier: bool | None = None) -> float:
        return sum(l.value for l in self.lines if l.booked and l.value is not None
                   and (management_tier is None or (l.tier == "management") == management_tier))

    @property
    def management_ebitda(self) -> float:
        """GAAP EBITDA + management-tier add-backs (SBC). The seller's marketed 'pre-SBC' number."""
        return self.gaap_ebitda + self._booked(management_tier=True)

    @property
    def diligence_ebitda_pre_sbc(self) -> float:
        """SBC added back (consistent with SBC-excluded comps). Upper of the two bases."""
        return self.gaap_ebitda + self._booked()

    @property
    def diligence_ebitda_post_sbc(self) -> float:
        """SBC treated as a real recurring cost (not added back). Lower of the two bases."""
        return self.gaap_ebitda + self._booked(management_tier=False)


def build_bridge(fs: FactSet, period: str, adjustments: list[Adjustment] | None = None) -> Bridge:
    adjustments = adjustments or load_adjustments()
    br = Bridge(period=period, gaap_ebitda=gaap_ebitda(fs, period))

    for a in adjustments:
        v = a.signed_value(fs, period)

        # BOTH (SBC): book it into the management-basis subtotal, flagged as contested.
        if a.treatment == "BOTH":
            br.lines.append(BridgeLine(a.id, a.name, a.tier, a.treatment, v, booked=(v is not None),
                                       note="presented on two bases; also drives dilution analysis"))
        # ACCEPT: must be quantified or it raises (no silent zero).
        elif a.treatment == "ACCEPT":
            if v is None:
                raise ValueError(f"{a.id} is ACCEPT but has no sourced value for {period}.")
            br.lines.append(BridgeLine(a.id, a.name, a.tier, a.treatment, v, booked=True))
        # REJECT: reverses a seller add-back. Shown, not booked (we didn't add it in the first place).
        elif a.treatment == "REJECT":
            br.lines.append(BridgeLine(a.id, a.name, a.tier, a.treatment, v, booked=False,
                                       note="seller add-back we decline; unquantifiable from public data"
                                            if v is None else "seller add-back we decline"))
        # SENSITIVITY: exposure shown as a range/magnitude, never booked into the point estimate.
        elif a.treatment == "SENSITIVITY":
            note = "sensitivity / exposure — shown as a range, not booked"
            if a.sensitivity_bps:
                note = f"per {a.sensitivity_bps}bps: {v:,.0f}; exposure not booked"
            br.lines.append(BridgeLine(a.id, a.name, a.tier, a.treatment, v, booked=False, note=note))
        else:
            raise ValueError(f"{a.id}: unknown treatment '{a.treatment}'")

    return br
