"""
qoe.excel — the QoE deliverable workbook (openpyxl).

Design choices that make it read as professional, not student:
  * Values are in $ thousands, matching the 10-K exactly (so the model ties to the filing).
  * The colour convention is enforced (blue input / black formula / green cross-sheet link).
  * Key cells are LIVE FORMULAS that reference the Source Data tab — click a bridge cell and it
    computes from sourced inputs. It is a working model, not an exported table.
  * Every schedule carries a tickmark column citing the source (document + note), like a workpaper.
  * Assumptions live on their own tab, amber-flagged, and are the only non-sourced numbers.

Tabs: Cover · Assumptions · EBITDA Bridge · Adjustment Schedule · NWC · CCC & Diagnostics · Source Data
"""
from __future__ import annotations
import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from finlib.facts import FactSet, Provenance
from finlib.xlsx import styles as S
from . import labels as L, metrics as M, bridge as B, mscore as MS

PERIODS = ("FY2023", "FY2024", "FY2025")
K = 1000.0  # whole dollars -> thousands


def _k(v):
    return None if v is None else v / K


class _Ref:
    """Maps (line_item, period) -> a cell address on the Source Data sheet for live linking."""
    def __init__(self):
        self.map: dict[tuple[str, str], str] = {}

    def add(self, line_item, period, addr):
        self.map[(line_item, period)] = addr

    def cell(self, line_item, period) -> str:
        return self.map[(line_item, period)]  # raises if we try to link something unsourced

    def link(self, line_item, period) -> str:
        return f"='Source Data'!{self.cell(line_item, period)}"


# ---------------------------------------------------------------- Source Data
def _build_source_data(wb, fs: FactSet) -> _Ref:
    ws = wb.create_sheet("Source Data")
    S.title_block(ws, "Source Data — every figure, with provenance",
                  "$ in thousands. FILED = from filing; ASSUMPTION = chosen input; "
                  "NOT_DISCLOSED = filing is silent (a finding).")
    hdr = 4
    S.header_row(ws, hdr, ["Line item", "Period", "Value ($000s)", "Source", "Reference", "Provenance"])
    ref = _Ref()
    r = hdr + 1
    facts = sorted(fs._facts, key=lambda f: (f.statement, f.line_item, f.period))
    for f in facts:
        S.write(ws, f"A{r}", f.line_item, font=S.label_font(), border=S.BORDER)
        S.write(ws, f"B{r}", f.period, align=S.CENTER, border=S.BORDER)
        val = _k(f.value_usd)
        prov_input = f.provenance in (Provenance.FILED,)
        S.write(ws, f"C{r}", val, font=S.input_font() if prov_input else S.label_font(),
                fmt=S.MONEY_FMT, align=S.RIGHT, border=S.BORDER)
        S.write(ws, f"D{r}", f.source, font=S.note_font(), border=S.BORDER)
        S.write(ws, f"E{r}", f.ref, font=S.note_font(), border=S.BORDER)
        S.write(ws, f"F{r}", f.provenance.value, align=S.CENTER, border=S.BORDER,
                font=S.note_font())
        ref.add(f.line_item, f.period, f"C{r}")
        r += 1
    for col, w in zip("ABCDEF", (38, 12, 14, 22, 40, 14)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    return ref


# ---------------------------------------------------------------- Cover
def _build_cover(wb):
    ws = wb.create_sheet("Cover")
    S.title_block(ws, "Super Micro Computer, Inc. — Quality of Earnings",
                  "Buy-side diligence (public-information Phase 1)")
    rows = [
        ("Prepared as", "Illustrative buy-side QoE for a hypothetical take-private of SMCI."),
        ("Basis of preparation", "Public SEC filings only. No trial balance, no management access, "
                                 "no cut-off testing. Phase 1 / pre-LOI scope."),
        ("Periods", "FY2023 / FY2024 / FY2025 (fiscal years end June 30)."),
        ("Currency / units", "USD, in thousands (matches the 10-K)."),
        ("", ""),
        ("Colour convention", ""),
        ("  Blue", "Hard-coded input — a sourced or assumed number."),
        ("  Black", "Formula — a computed cell."),
        ("  Green", "Link to another sheet."),
        ("  Amber tab", "Assumptions — the only non-sourced numbers in the model."),
        ("", ""),
        ("Source documents", "SMCI FY2023/FY2024/FY2025 10-K; FY2022/FY2025/FY2026 DEF 14A; "
                             "8-K 2024-10-30 (Item 4.01, EY resignation)."),
        ("Control note", "Balance sheet balances and income-statement subtotals are re-derived on "
                         "every run; the model raises on any missing sourced figure."),
    ]
    r = 4
    for k, v in rows:
        S.write(ws, f"A{r}", k, font=S.subtotal_font() if k and not k.startswith(" ") else S.label_font())
        S.write(ws, f"B{r}", v, align=S.WRAP)
        r += 1
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 86
    # colour the legend swatches
    ws["A10"].font = S.input_font()
    ws["A11"].font = S.formula_font()
    ws["A12"].font = S.link_font()
    return ws


# ---------------------------------------------------------------- Assumptions
def _build_assumptions(wb):
    ws = wb.create_sheet("Assumptions")
    S.title_block(ws, "Assumptions — non-sourced inputs (amber)",
                  "Everything here is a CHOICE, not a filing figure. Kept few and explicit.")
    hdr = 4
    S.header_row(ws, hdr, ["ID", "Assumption", "Low", "High", "Basis"])
    data = [
        ("A-1", "Illustrative EV / EBITDA multiple (x)", 12, 18,
         "Sensitivity range only; not a valuation opinion."),
        ("A-2", "Pro forma compliant finance-function cost ($000s/yr)", 15000, 40000,
         "Benchmarked to peer proxy audit-fee + G&A headcount; ADJ-003."),
    ]
    r = hdr + 1
    for id_, name, lo, hi, basis in data:
        S.write(ws, f"A{r}", id_, align=S.CENTER, fill=S.ASSUMPTION_FILL, border=S.BORDER)
        S.write(ws, f"B{r}", name, fill=S.ASSUMPTION_FILL, border=S.BORDER)
        S.write(ws, f"C{r}", lo, font=S.assumption_font(), fmt=S.MONEY_FMT, align=S.RIGHT,
                fill=S.ASSUMPTION_FILL, border=S.BORDER)
        S.write(ws, f"D{r}", hi, font=S.assumption_font(), fmt=S.MONEY_FMT, align=S.RIGHT,
                fill=S.ASSUMPTION_FILL, border=S.BORDER)
        S.write(ws, f"E{r}", basis, font=S.note_font(), fill=S.ASSUMPTION_FILL, border=S.BORDER)
        r += 1
    for col, w in zip("ABCDE", (8, 46, 12, 12, 52)):
        ws.column_dimensions[col].width = w
    return ws


# ---------------------------------------------------------------- EBITDA Bridge
def _build_bridge(wb, fs, ref: _Ref):
    ws = wb.create_sheet("EBITDA Bridge")
    S.title_block(ws, "EBITDA Bridge — three-tier walk (FY2025)",
                  "$ in thousands. Green cells link to Source Data; black cells are formulas.")
    hdr = 4
    S.header_row(ws, hdr, ["ID", "Line", "Amount", "Treatment", "Tickmark (source)"])
    p = "FY2025"
    r = hdr + 1

    # GAAP EBITDA = Operating income + D&A  (live link to Source Data)
    op = ref.cell("Operating income", p)
    da = ref.cell("D&A (cash flow)", p)
    S.write(ws, f"A{r}", "", border=S.BORDER)
    S.write(ws, f"B{r}", "GAAP EBITDA (Operating income + D&A)", font=S.subtotal_font(), border=S.BORDER)
    S.write(ws, f"C{r}", f"='Source Data'!{op}+'Source Data'!{da}", font=S.link_font(),
            fmt=S.MONEY_FMT, align=S.RIGHT, border=S.BORDER)
    S.write(ws, f"D{r}", "subtotal", align=S.CENTER, border=S.BORDER, font=S.note_font())
    S.write(ws, f"E{r}", "IS: Operating income; CF: D&A", font=S.note_font(), border=S.BORDER)
    gaap_row = r
    r += 1

    # SBC add-back (live link)
    sbc = ref.cell("Stock-based compensation", p)
    S.write(ws, f"A{r}", "ADJ-001", align=S.CENTER, border=S.BORDER)
    S.write(ws, f"B{r}", "+ Stock-based compensation (contested)", border=S.BORDER)
    S.write(ws, f"C{r}", f"='Source Data'!{sbc}", font=S.link_font(), fmt=S.MONEY_FMT,
            align=S.RIGHT, border=S.BORDER)
    S.write(ws, f"D{r}", "BOTH", align=S.CENTER, border=S.BORDER)
    S.write(ws, f"E{r}", "CF: Stock-based compensation", font=S.note_font(), border=S.BORDER)
    sbc_row = r
    r += 1

    # Audit-fee delta = FY2025 audit fees less FY2022 baseline (LIVE formula across two facts)
    af_t = ref.cell("Audit fees (BDO)", "FY2025")
    af_b = ref.cell("Audit fees (Deloitte)", "FY2022")
    S.write(ws, f"A{r}", "ADJ-002", align=S.CENTER, border=S.BORDER)
    S.write(ws, f"B{r}", "+ Incremental audit fees vs FY22 baseline", border=S.BORDER)
    S.write(ws, f"C{r}", f"='Source Data'!{af_t}-'Source Data'!{af_b}", font=S.link_font(),
            fmt=S.MONEY_FMT, align=S.RIGHT, border=S.BORDER)
    S.write(ws, f"D{r}", "ACCEPT", align=S.CENTER, border=S.BORDER)
    S.write(ws, f"E{r}", "DEF 14A: Principal Accountant Fees", font=S.note_font(), border=S.BORDER)
    af_row = r
    r += 1

    # Management-basis subtotal (GAAP + SBC)
    S.write(ws, f"B{r}", "= Management-basis EBITDA (SBC added back)", font=S.subtotal_font(),
            border=S.TOP_BORDER)
    S.write(ws, f"C{r}", f"=C{gaap_row}+C{sbc_row}", font=S.subtotal_font(), fmt=S.MONEY_FMT,
            align=S.RIGHT, border=S.TOP_BORDER)
    r += 1

    # Diligence Adjusted EBITDA — two bases
    S.write(ws, f"B{r}", "= Diligence Adj. EBITDA — SBC added back", font=S.subtotal_font(), border=S.BORDER)
    S.write(ws, f"C{r}", f"=C{gaap_row}+C{sbc_row}+C{af_row}", font=S.subtotal_font(),
            fmt=S.MONEY_FMT, align=S.RIGHT, border=S.BORDER)
    r += 1
    S.write(ws, f"B{r}", "= Diligence Adj. EBITDA — SBC as real cost", font=S.subtotal_font(),
            border=S.DBL_TOP)
    S.write(ws, f"C{r}", f"=C{gaap_row}+C{af_row}", font=S.subtotal_font(), fmt=S.MONEY_FMT,
            align=S.RIGHT, border=S.DBL_TOP)
    r += 2

    # The SBC swing note (the headline)
    S.write(ws, f"B{r}", "SBC decision swing (EBITDA):", font=S.note_font())
    S.write(ws, f"C{r}", f"=C{sbc_row}", font=S.formula_font(), fmt=S.MONEY_FMT, align=S.RIGHT)
    r += 1
    S.write(ws, f"B{r}", "SBC swing at Assumptions A-1 low multiple (EV):", font=S.note_font())
    S.write(ws, f"C{r}", f"=C{sbc_row}*Assumptions!C5", font=S.formula_font(), fmt=S.MONEY_FMT, align=S.RIGHT)
    r += 2
    S.write(ws, f"B{r}", "Not booked (shown as exposures on Adjustment Schedule): "
                         "ADJ-003 finance-function cost, ADJ-004 related-party pricing, "
                         "ADJ-005 ramp-cost reversal.", font=S.note_font(), align=S.WRAP)

    for col, w in zip("ABCDE", (10, 44, 16, 12, 40)):
        ws.column_dimensions[col].width = w
    return ws


# ---------------------------------------------------------------- Adjustment Schedule
def _build_adjustments(wb):
    ws = wb.create_sheet("Adjustment Schedule")
    S.title_block(ws, "Adjustment Schedule — rationale AND counterargument",
                  "Every adjustment carries the seller's pushback. Nothing is booked without it.")
    hdr = 4
    S.header_row(ws, hdr, ["ID", "Adjustment", "Tier", "Treatment", "Mkt practice",
                           "Rationale", "Counterargument (seller)"])
    r = hdr + 1
    for a in B.load_adjustments():
        S.write(ws, f"A{r}", a.id, align=S.CENTER, border=S.BORDER)
        S.write(ws, f"B{r}", a.name, align=S.WRAP, border=S.BORDER)
        S.write(ws, f"C{r}", a.tier, align=S.CENTER, border=S.BORDER)
        S.write(ws, f"D{r}", a.treatment, align=S.CENTER, border=S.BORDER)
        S.write(ws, f"E{r}", a.market_practice, align=S.CENTER, border=S.BORDER, font=S.note_font())
        S.write(ws, f"F{r}", a.rationale.strip(), align=S.WRAP, border=S.BORDER)
        S.write(ws, f"G{r}", a.counterargument.strip(), align=S.WRAP, border=S.BORDER)
        ws.row_dimensions[r].height = 66
        r += 1
    for col, w in zip("ABCDEFG", (9, 30, 12, 12, 14, 52, 52)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    return ws


# ---------------------------------------------------------------- NWC
def _build_nwc(wb, fs, ref: _Ref):
    ws = wb.create_sheet("NWC")
    S.title_block(ws, "Net Working Capital — peg schedule",
                  "$ in thousands. Cash-free/debt-free; excludes cash, debt, income taxes.")
    hdr = 4
    comps = [("Accounts receivable, net", "+"), ("Inventories, net", "+"),
             ("Prepaid & other current assets", "+"), ("Accounts payable", "-"),
             ("Accrued liabilities", "-"), ("Deferred revenue, current", "-")]
    S.header_row(ws, hdr, ["Component", *PERIODS, "Tickmark"])
    r = hdr + 1
    first = r
    for name, sign in comps:
        S.write(ws, f"A{r}", f"{sign} {name}", border=S.BORDER)
        for i, p in enumerate(PERIODS):
            col = get_column_letter(2 + i)
            base = f"'Source Data'!{ref.cell(name, p)}"
            formula = f"={base}" if sign == "+" else f"=-{base}"
            S.write(ws, f"{col}{r}", formula, font=S.link_font(), fmt=S.MONEY_FMT,
                    align=S.RIGHT, border=S.BORDER)
        S.write(ws, f"E{r}", "Balance sheet / Note 6", font=S.note_font(), border=S.BORDER)
        r += 1
    last = r - 1
    # NWC subtotal (live SUM)
    S.write(ws, f"A{r}", "= Net working capital", font=S.subtotal_font(), border=S.TOP_BORDER)
    for i in range(len(PERIODS)):
        col = get_column_letter(2 + i)
        S.write(ws, f"{col}{r}", f"=SUM({col}{first}:{col}{last})", font=S.subtotal_font(),
                fmt=S.MONEY_FMT, align=S.RIGHT, border=S.TOP_BORDER)
    nwc_row = r
    r += 1
    # NWC % of revenue (live)
    S.write(ws, f"A{r}", "  NWC as % of revenue", font=S.note_font())
    for i, p in enumerate(PERIODS):
        col = get_column_letter(2 + i)
        S.write(ws, f"{col}{r}", f"={col}{nwc_row}/'Source Data'!{ref.cell('Revenue', p)}",
                font=S.formula_font(), fmt=S.PCT_FMT, align=S.RIGHT)
    r += 2
    S.write(ws, f"A{r}", "Peg note: recommend pegging NWC as a % of LTM revenue, not a trailing "
                         "dollar average — a dollar peg transfers value to the seller in a "
                         "working-capital-hungry growth business.", align=S.WRAP, font=S.note_font())
    for col, w in zip("ABCDE", (30, 15, 15, 15, 26)):
        ws.column_dimensions[col].width = w
    return ws


# ---------------------------------------------------------------- CCC & Diagnostics
def _build_diagnostics(wb, fs):
    ws = wb.create_sheet("CCC & Diagnostics")
    S.title_block(ws, "Cash conversion & earnings quality",
                  "Turnover on average balances where a prior period exists.")
    mets = M.compute(fs, PERIODS)
    hdr = 4
    S.header_row(ws, hdr, ["Metric", *PERIODS, "Read"])
    rows = [
        ("DIO (days)", [m.dio for m in mets], S.DAYS_FMT, "Inventory days"),
        ("DSO (days)", [m.dso for m in mets], S.DAYS_FMT, "Receivable days"),
        ("DPO (days)", [m.dpo for m in mets], S.DAYS_FMT, "Payable days — falling = suppliers want cash"),
        ("CCC (days)", [m.ccc for m in mets], S.DAYS_FMT, "DIO+DSO-DPO"),
        ("NWC ($000s)", [_k(m.nwc) for m in mets], S.MONEY_FMT, "Absolute NWC"),
        ("NWC / revenue", [m.nwc_pct_revenue for m in mets], S.PCT_FMT, "The operating metric"),
        ("Accruals ratio", [m.accruals_ratio for m in mets], S.PCT_FMT, "(NI-CFO)/avg assets — Sloan"),
    ]
    r = hdr + 1
    for name, vals, fmt, note in rows:
        S.write(ws, f"A{r}", name, font=S.label_font(), border=S.BORDER)
        for i, v in enumerate(vals):
            col = get_column_letter(2 + i)
            S.write(ws, f"{col}{r}", (None if v is None else v),
                    font=S.input_font(), fmt=fmt, align=S.RIGHT, border=S.BORDER)
        S.write(ws, f"E{r}", note, font=S.note_font(), border=S.BORDER)
        r += 1

    r += 1
    S.write(ws, f"A{r}", "Beneish M-score (screen; read components)", font=S.subtotal_font())
    r += 1
    S.header_row(ws, r, ["Year", "DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "TATA", "LVGI", "M", "Flag"])
    r += 1
    for ms in MS.compute_all(fs):
        vals = [ms.period, ms.DSRI, ms.GMI, ms.AQI, ms.SGI, ms.DEPI, ms.SGAI, ms.TATA, ms.LVGI,
                ms.m_score, "FLAG" if ms.flagged else "ok"]
        for i, v in enumerate(vals):
            col = get_column_letter(1 + i)
            fmt = S.RATIO_FMT if isinstance(v, float) else None
            S.write(ws, f"{col}{r}", v, fmt=fmt, align=S.CENTER if i == 0 else S.RIGHT,
                    border=S.BORDER, font=S.input_font() if isinstance(v, float) else S.label_font())
        r += 1
    r += 1
    S.write(ws, f"A{r}", "Note: FY2024 flags, driven partly by SGI (sales doubled — benign growth). "
                         "The components that matter are DSRI>1, GMI>1, DEPI>1; corroborated by the "
                         "54% accruals ratio.", align=S.WRAP, font=S.note_font())
    for col, w in zip("ABCDEFGHIJK", (26, 9, 8, 8, 8, 8, 8, 8, 8, 9, 7)):
        ws.column_dimensions[col].width = w
    return ws


# ---------------------------------------------------------------- orchestrator
def build_workbook(fs: FactSet, out_path: str) -> str:
    wb = Workbook()
    wb.remove(wb.active)  # drop default sheet
    # Source Data first (others link to it), but order tabs for the reader afterwards.
    ref = _build_source_data(wb, fs)
    _build_cover(wb)
    _build_assumptions(wb)
    _build_bridge(wb, fs, ref)
    _build_adjustments(wb)
    _build_nwc(wb, fs, ref)
    _build_diagnostics(wb, fs)
    # reorder: Cover first, Source Data last
    order = ["Cover", "Assumptions", "EBITDA Bridge", "Adjustment Schedule",
             "NWC", "CCC & Diagnostics", "Source Data"]
    wb._sheets.sort(key=lambda s: order.index(s.title))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    return out_path
