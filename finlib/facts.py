"""
finlib.facts — the source-of-truth layer.

Every financial value in this project is a Fact: a number plus its provenance. Code never
holds a bare float. If you ask for a value that was never sourced, lookup RAISES — it does not
return zero and it does not interpolate. That behavior is the project's credibility guarantee.

Reused by project 2 (the anomaly screener) unchanged.
"""
from __future__ import annotations
import csv
import glob
import os
from dataclasses import dataclass
from enum import Enum


class Provenance(str, Enum):
    FILED = "FILED"                 # typed/parsed directly from a filing — the only source of truth
    DERIVED = "DERIVED"             # computed from FILED facts by code
    ASSUMPTION = "ASSUMPTION"       # an input we chose; must be labelled and few
    NOT_DISCLOSED = "NOT_DISCLOSED"  # the filing does not disclose it — a finding, not a zero


class FactNotFound(KeyError):
    """Raised when a requested (line_item, period) was never sourced. Never silently defaulted."""


@dataclass(frozen=True)
class Fact:
    statement: str          # IS | BS | CF | NOTE | PROXY
    line_item: str          # canonical label
    period: str             # FY2023 | FY2024 | FY2025 | Q/E YYYY-MM-DD | LTM
    value_usd: float | None  # ALWAYS whole US dollars (normalized at load); None if not disclosed
    source: str             # document, e.g. "SMCI FY2025 10-K"
    ref: str                # where in the document, e.g. "Note 6, Inventories"
    provenance: Provenance

    @property
    def is_usable(self) -> bool:
        return self.value_usd is not None and self.provenance in (
            Provenance.FILED, Provenance.DERIVED
        )


class FactSet:
    """Immutable-ish collection of Facts keyed by (line_item, period), with strict lookup."""

    def __init__(self, facts: list[Fact]):
        self._facts = facts
        self._index: dict[tuple[str, str], Fact] = {}
        for f in facts:
            key = (f.line_item, f.period)
            # First writer wins; flag genuine contradictions so a mis-entry can't hide.
            if key in self._index:
                prior = self._index[key]
                if prior.value_usd != f.value_usd:
                    raise ValueError(
                        f"Conflicting values for {key}: {prior.value_usd} ({prior.source}) "
                        f"vs {f.value_usd} ({f.source}). Resolve the source data."
                    )
                continue
            self._index[key] = f

    # ---- lookup ---------------------------------------------------------------
    def get(self, line_item: str, period: str) -> Fact:
        """Return the Fact or RAISE. Never returns a default."""
        try:
            return self._index[(line_item, period)]
        except KeyError:
            raise FactNotFound(
                f"No sourced value for '{line_item}' in {period}. "
                f"Find it in the filing and add it to data/source/ — do not estimate."
            )

    def value(self, line_item: str, period: str) -> float:
        """Return the usable dollar value or RAISE (incl. when disclosed as NOT_DISCLOSED)."""
        f = self.get(line_item, period)
        if not f.is_usable:
            raise FactNotFound(
                f"'{line_item}' in {period} is {f.provenance.value} "
                f"({f.ref}); it has no usable value. Handle it explicitly."
            )
        return f.value_usd

    def opt(self, line_item: str, period: str, default: float | None = None) -> float | None:
        """Soft lookup for genuinely-optional items. Use sparingly and never to paper over a gap."""
        try:
            return self.value(line_item, period)
        except FactNotFound:
            return default

    def has(self, line_item: str, period: str) -> bool:
        return (line_item, period) in self._index

    def periods(self) -> list[str]:
        order = {"FY2023": 0, "FY2024": 1, "FY2025": 2}
        ps = {f.period for f in self._facts}
        return sorted(ps, key=lambda p: (order.get(p, 99), p))

    def line_items(self, statement: str | None = None) -> list[str]:
        return sorted({f.line_item for f in self._facts
                       if statement is None or f.statement == statement})

    def __len__(self) -> int:
        return len(self._facts)


# ---- loading ------------------------------------------------------------------
# The source CSVs use two unit conventions. We normalize everything to WHOLE DOLLARS here,
# once, at the boundary — so no downstream code ever worries about thousands-vs-dollars.

_SOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "source")


def _to_float(s: str) -> float | None:
    s = (s or "").strip().replace(",", "")
    if s == "" or s.upper() in ("NA", "N/A", "NOT_TAGGED", "NONE"):
        return None
    return float(s)


def _load_xbrl_csv(path: str) -> list[Fact]:
    """facts.csv from the EDGAR pull: value already in whole dollars."""
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("provenance") != "FILED":
                continue
            out.append(Fact(
                statement=r["statement"], line_item=r["line_item"], period=r["period"],
                value_usd=_to_float(r["value"]),
                source=r.get("form", "SMCI 10-K/Q (XBRL)"),
                ref=f"XBRL {r.get('concept','')} | {r.get('accession','')}",
                provenance=Provenance.FILED,
            ))
    return out


def _load_handentered_csv(path: str) -> list[Fact]:
    """Hand-read CSVs: value in USD thousands -> normalize to whole dollars."""
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            prov = Provenance(r["provenance"]) if r["provenance"] in Provenance.__members__ \
                else Provenance(r["provenance"])
            raw = _to_float(r["value_usd_thousands"])
            val = raw * 1000 if raw is not None else None
            out.append(Fact(
                statement=r["statement"], line_item=r["line_item"], period=r["period"],
                value_usd=val, source=r["source_doc"], ref=r["source_ref"],
                provenance=prov,
            ))
    return out


def load_facts(source_dir: str = _SOURCE_DIR) -> FactSet:
    """Load and merge every source CSV into one FactSet in whole dollars."""
    facts: list[Fact] = []
    xbrl = os.path.join(source_dir, "facts.csv")
    if os.path.exists(xbrl):
        facts += _load_xbrl_csv(xbrl)
    for path in sorted(glob.glob(os.path.join(source_dir, "facts_*.csv"))):
        facts += _load_handentered_csv(path)
    if not facts:
        raise RuntimeError(f"No source facts found in {source_dir}. Run scripts/pull_edgar.py.")
    return FactSet(facts)
