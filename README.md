# Super Micro Computer (SMCI) — Quality of Earnings Analysis

A buy-side **Quality of Earnings (QoE)** analysis of Super Micro Computer, Inc. (NASDAQ: SMCI),
framed as Phase 1 / pre-LOI financial due diligence for a hypothetical take-private. Built to the
standard of a Transaction Advisory Services / Financial Due Diligence workstream.

Every figure in this repository is sourced from SMCI's SEC filings and reproduced by the code.
No number is estimated or illustrative. The model **raises an error** rather than defaulting a
missing figure to zero — controls are built into the analysis of a company whose defining failure
was a lack of controls.

## Headline findings

- **Profit does not convert to cash.** In FY2024 SMCI reported **+$1,153M net income against
  −$2,486M operating cash flow** — a ~$3.6B divergence driven by an inventory build from $1.4B to
  $4.3B. The Sloan accruals ratio hit **+53.9%**; the Beneish M-score flags FY2024. The cash
  conversion cycle — not the EBITDA bridge — is the finding.
- **The SBC decision is worth ~$4.7B of enterprise value.** Stock-based compensation ($314M in
  FY2025) is presented on two bases rather than booked, with the multiple held consistent with the
  metric it multiplies.
- **A negative EBITDA adjustment** for the pro-forma cost of a compliant finance function — the
  buy-side move a growth-stage seller's bankers never make.
- **Governance:** an **adverse ICFR opinion alongside an unqualified opinion on the financials**,
  five unremediated material weaknesses (mapped to COSO), and an auditor (EY) that resigned
  mid-engagement over the control environment — the one COSO area the disclosed weaknesses omit.

## What's in here

| Path | Contents |
|---|---|
| `docs/00_architecture.md` | Data requirements, adjustment hypotheses (with seller counterarguments), roadmap |
| `docs/01_review_guide.md` | Primary-source pull list and exactly what to verify in each filing |
| `docs/02_findings_auditor.md` | Auditor timeline, the two opinions, material-weakness → COSO mapping, CAMs |
| `docs/03_IC_memo.md` | 3-page buy-side Investment Committee memo |
| `finlib/` | Reusable engine: sourced-fact model, earnings-quality diagnostics (DSO/DIO/DPO/CCC, Sloan accruals, Beneish M-score), Excel styling |
| `qoe/` | SMCI-specific: validation controls, EBITDA bridge, NWC, M-score, workbook, charts |
| `data/source/` | Every fact as a sourced row (`facts*.csv`), declarative adjustments (`adjustments.yaml`), raw SEC XBRL (`companyfacts_raw.json`) |
| `outputs/` | `SMCI_QoE_model.xlsx` (live-formula workbook) and the waterfall / CCC charts |
| `scripts/pull_edgar.py` | Reproducible ingestion from SEC EDGAR |

## Design principles

1. **No fabricated numbers.** Facts carry provenance (`FILED` / `DERIVED` / `ASSUMPTION` /
   `NOT_DISCLOSED`). Lookups raise on a missing sourced value.
2. **Adjustments are declarative and adversarial.** Each carries a rationale *and* the seller's
   counterargument, and a treatment (`ACCEPT` / `REJECT` / `SENSITIVITY` / `BOTH`). About half the
   issues identified are deliberately **not booked** — sized as exposures with a scoped diligence
   request instead.
3. **Controls run on every execution.** Balance sheet balances, income-statement subtotals foot,
   and the model ties to the filing before it produces a number.
4. **The engine is reusable.** `finlib/` is company-agnostic and feeds a separate financial-anomaly
   screener.

## Run it

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

./.venv/bin/python main.py                       # console: controls, diagnostics, bridge, M-score
./.venv/bin/python scripts/build_deliverables.py # writes the Excel model + charts to outputs/
```

## Sources

SMCI filings via SEC EDGAR: FY2023 / FY2024 / FY2025 10-K; FY2022 / FY2025 / FY2026 DEF 14A;
8-K dated 2024-10-30 (Item 4.01, auditor change). Structured financials from SEC's XBRL
`companyfacts` API. Fiscal years end June 30.

---

*Educational portfolio project. This is an analysis of public information for a hypothetical
transaction; it is not investment advice and not affiliated with SMCI or any advisory firm.*
