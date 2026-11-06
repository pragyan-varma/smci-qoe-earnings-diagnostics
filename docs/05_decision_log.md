# Decision log

The design choices behind the model, what each one bought, and what it cost. Where
[`01_methodology.md`](01_methodology.md) already gives the full reasoning, the entry
summarizes it and links there. Code references are to `finlib/`, `qoe/`, and
`data/source/adjustments.yaml`.

### 1. Every value is a sourced fact, and missing values raise

**Decision.** Store each figure as a `Fact` carrying its source document, location, and a
provenance tag (`FILED` / `DERIVED` / `ASSUMPTION` / `NOT_DISCLOSED`). `FactSet.value`
raises `FactNotFound` for an item that was never sourced, and also for one recorded as
`NOT_DISCLOSED` (`finlib/facts.py`).
**Why.** A lookup that defaults to zero would turn a gap in the filings into a number in
the bridge. Raising forces each gap to be handled explicitly. See
[methodology §2](01_methodology.md#2-data-model-and-provenance).
**Tradeoff.** Strict lookup has a soft escape hatch: `FactSet.opt` returns a default.
`qoe/labels.py` uses it for the two term-loan and credit-line debt items, which default to
0 when absent. A missing debt line would therefore understate total debt rather than
raise.

### 2. Normalize units to whole dollars once, at load

**Decision.** XBRL values arrive in dollars and hand-read values in thousands.
`load_facts` multiplies the hand-read files by 1,000, so every `Fact` is in whole dollars.
**Why.** Mixing conventions caused a real error early on: operating income failed to foot
by $10k–$78k until MD&A figures stated in millions were replaced with exact XBRL values
([source documents §3](02_source_documents.md#3-verification-performed)).
**Tradeoff.** The workbook is presented in thousands to match the 10-K, so `qoe/excel.py`
divides by 1,000 again on the way out. That's two conversions to keep in step.

### 3. Controls are code, not a checklist

**Decision.** Tie-outs live in `qoe/validate.py` as functions that return
pass/fail with the difference: gross profit foots, operating income foots, net income
approximately equals pre-tax less tax, and the balance sheet balances, with equity
including non-controlling interest.
**Why.** The target's defining failure was internal control. A model of that company
should show its own controls and be able to rerun them.
**Tradeoff.** The checks aren't enforced. `scripts/build_deliverables.py` doesn't call
them, and `main.py` runs them with `tolerate=True`, so a failure prints but doesn't stop the
run. Of the 14 rows printed, 3 (`Pretax - Operating`) are informational and can't fail.
The net-income check uses an $8M tolerance because the equity-method investee sits below
the tax line. The FY2023 balance-sheet check is skipped because the equity-including-NCI
figure isn't sourced for that year. Tracked as
[#1](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/1).

### 4. Adjustments are declarative and must state the seller's counterargument

**Decision.** Each adjustment is a YAML entry with a tier, a treatment (`ACCEPT` /
`REJECT` / `SENSITIVITY` / `BOTH`), and a direction. `load_adjustments` refuses to load
one without a `rationale`, `counterargument`, and `market_practice`.
**Why.** It keeps the reasoning next to the number and makes a one-sided adjustment
impossible to add by accident.
**Tradeoff.** The check confirms only that the fields are filled in, not what they say.
Some values are also duplicated outside the YAML: the workbook recomputes ADJ-002 from the
audit-fee facts, and the ADJ-003 range is typed into the Assumptions tab. Tracked as
[#4](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/4).

### 5. Only quantified, accepted items move the underwritten number

**Decision.** In `build_bridge`, `ACCEPT` items are booked and raise if they have no value
for the period. `REJECT` and `SENSITIVITY` items are shown but never booked. `BOTH` (SBC)
is booked into one of the two bases only.
**Why.** Where public filings can't support a figure, the issue is shown as an exposure
rather than estimated
([methodology §1](01_methodology.md#1-scope-and-framing)).
**Tradeoff.** Of the unbooked items, only related-party pricing (ADJ-004) has a computed
exposure: $6.5M of FY2025 EBITDA per 100bps. Inventory reserve and revenue cut-off are
handled in prose, and ADJ-005 prints `n/q`. Tracked as
[#5](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/5).

### 6. Start EBITDA from operating income plus cash-flow D&A

**Decision.** `gaap_ebitda` = operating income + the cash-flow statement's D&A line.
**Why.** Operating income already excludes interest income, other income, and the
equity-method investee. SMCI's large cash balance would otherwise inflate EBITDA if the
walk started from net income
([methodology §3](01_methodology.md#3-ebitda-bridge-structure)).
**Tradeoff.** The cash-flow D&A line is also the depreciation proxy in the M-score's DEPI
component, because SMCI doesn't separately tag depreciation (`qoe/mscore.py`).

### 7. Present SBC on both bases instead of choosing one

**Decision.** SBC (ADJ-001, $314.5M in FY2025) has treatment `BOTH`. The bridge reports
Diligence Adjusted EBITDA with SBC added back ($1,612.0M) and with SBC as a cost
($1,297.6M).
**Why.** The add-back is contested. The case for and against is in
[methodology §4.1](01_methodology.md#41-stock-based-compensation--presented-on-both-bases).
The rule applied is that the multiple must be struck on the same basis as the EBITDA it
multiplies.
**Tradeoff.** The reader gets two numbers instead of one answer. The illustrative
multiple is also not defined in one place: `main.py` uses 15× (a $4.72B EV swing), while
the workbook uses the low end of Assumptions A-1 (12×). The dilution the counterargument
calls for isn't computed. Tracked as
[#4](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/4) and
[#8](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/8).

### 8. Hold the cost of a compliant finance function as a negative sensitivity

**Decision.** ADJ-003 is a deduction, not an add-back, held as a `SENSITIVITY` range of
$15–40M a year rather than booked.
**Why.** Remediating five material weaknesses implies a permanently higher G&A run-rate,
so a controlled business earns less than the historical one
([methodology §4.3](01_methodology.md#43-pro-forma-cost-of-a-compliant-finance-function--negative-sensitivity)).
**Tradeoff.** The range is a labelled assumption. Its peer inputs aren't in the repo. The
YAML stores it under keys (`FY2025_low` / `FY2025_high`) that the bridge doesn't read, so
the bridge prints `n/q` and the range appears only on the workbook's Assumptions tab.
Tracked as
[#4](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/4).

### 9. Sloan accruals and the Beneish M-score as screens, with components exposed

**Decision.** Use the Sloan cash-flow accruals ratio (net income minus operating cash flow
over average total assets) and the eight-variable Beneish M-score with the −1.78
threshold. `finlib/diagnostics.py` exposes every M-score component as its own function.
**Why.** Both are standard, need only public statement data, and test different things:
accruals measure how much profit is not cash, and the M-score combines several
manipulation-risk indicators. Exposing components lets a reader see what drives a flag
([methodology §6](01_methodology.md#6-cash-conversion)).
**Tradeoff.** The M-score was calibrated on manufacturers. For FY2024 (M = 0.56,
flagged), sales growth alone (SGI 2.10) adds about +1.9 to the score, which a
hyper-growth company produces for benign reasons. That is why the workbook asks the reader
to look at DSRI, GMI, and DEPI instead.

### 10. Turnover ratios on average balances where a prior year exists

**Decision.** DSO, DIO, and DPO use the average of opening and closing balances when the
prior year is in the data, and period-end balances otherwise (`qoe/metrics.py`).
**Why.** Average balances match the flow figures (revenue, COGS) they are divided by,
which matters when the balance sheet roughly tripled in a year.
**Tradeoff.** No FY2022 balance sheet is sourced, so the FY2023 column uses period-end
balances while FY2024 and FY2025 use averages. The three columns aren't on the same
basis. The accruals ratio is not reported for FY2023 for the same reason.

### 11. A cash-free, debt-free NWC definition, with a revenue-linked peg

**Decision.** NWC = receivables + inventories + prepaid and other current assets −
payables − accrued liabilities − current deferred revenue. Cash, debt, and income taxes
are excluded. The recommended peg is a percentage of LTM revenue rather than a trailing
dollar average
([methodology §5](01_methodology.md#5-net-working-capital)).
**Why.** SMCI's working capital compounds with revenue (NWC went from $1,663.6M in FY2023
to $5,337.1M in FY2024), so a backward-looking dollar peg would sit below NWC at close.
**Tradeoff.** The model computes NWC at fiscal year-ends only. Six quarter-ends of
committed data are unused, and the percentage-of-LTM peg is argued but not calculated.
Tracked as
[#6](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/6).

### 12. A workbook that links back to its sources

**Decision.** `qoe/excel.py` writes every fact to a Source Data tab with its reference and
provenance. The EBITDA Bridge and NWC tabs use live formulas pointing at those cells.
Assumptions sit on their own amber tab. Font colour follows the blue-input /
black-formula / green-link convention.
**Why.** A reviewer can click any bridge or NWC figure and trace it to a filing without
running Python.
**Tradeoff.** Only those two tabs are live. The CCC & Diagnostics tab holds values
computed in Python and pasted in, so editing a source cell doesn't update it. The bridge
is also built twice, once in Python (`qoe/bridge.py`) and once as Excel formulas, and
nothing checks that they agree. Tracked as
[#1](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/1) and
[#4](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/4).
