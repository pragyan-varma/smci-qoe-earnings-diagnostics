# Super Micro Computer (SMCI) — Quality of Earnings Analysis

A buy-side **Quality of Earnings (QoE)** analysis of Super Micro Computer, Inc. (NASDAQ: SMCI),
scoped as Phase 1 / pre-LOI financial due diligence for a hypothetical take-private, together with
a reusable earnings-quality diagnostics engine.

Every figure is sourced from SMCI's SEC filings and reproduced by the code. Nothing is estimated.
A lookup for a value that was never sourced raises an exception rather than defaulting to zero.

**Periods covered:** FY2023–FY2025 (fiscal years end June 30).

---

## Findings

**Reported profit does not convert to cash.** In FY2024 SMCI reported **+$1,153M of net income
against −$2,486M of operating cash flow**, a ~$3.6B divergence driven by an inventory build from
$1.4B to $4.3B. The Sloan accruals ratio reached **+53.9%**, and the Beneish M-score flags FY2024.
The conclusion of the analysis is that cash conversion, not the EBITDA bridge, is the substantive
finding — growth here consumes cash faster than it generates earnings.

**EBITDA margin compressed while revenue tripled**, from 11.2% (FY2023) to 5.9% (FY2025) as revenue
grew from $7.1B to $22.0B.

**The stock-based compensation treatment is material and is presented on both bases rather than
booked.** SBC was $314M in FY2025; at an illustrative 15× multiple the treatment decision moves
enterprise value by roughly $4.7B. The requirement applied is that the multiple be struck on the
same basis as the EBITDA it multiplies.

**A negative EBITDA adjustment is proposed** for the pro-forma cost of a compliant finance function.
Remediating five material weaknesses implies a permanently higher G&A run-rate than the historical
business carried.

**Governance.** The FY2024 10-K carries an **adverse opinion on internal control over financial
reporting alongside an unqualified opinion on the financial statements** — two distinct tests, not a
contradiction. Five material weaknesses were disclosed and none were remediated as of filing. All
five map to process-level COSO components, while the predecessor auditor resigned mid-engagement
over control-environment concerns that appear in none of them.

**About half the issues identified were deliberately not booked.** Inventory reserve adequacy,
revenue cut-off, and related-party pricing cannot be supported by public filings. Each is sized as
an exposure and mapped to a named confirmatory procedure instead.

---

## Repository

| Path | Contents |
|---|---|
| `docs/01_methodology.md` | Scope, provenance model, and every adjustment with its rationale, counterargument, and market-practice verdict |
| `docs/02_source_documents.md` | Filings used, note-level disclosures, verification performed, and what is not publicly disclosed |
| `docs/03_governance_and_controls.md` | Auditor timeline, the two opinions, material weaknesses mapped to COSO, Critical Audit Matters |
| `docs/04_ic_memo.md` | Three-page Investment Committee memo |
| `finlib/` | Company-agnostic engine: sourced-fact model with provenance, earnings-quality diagnostics (DSO/DIO/DPO/CCC, Sloan accruals, Beneish M-score), Excel styling |
| `qoe/` | SMCI-specific: validation controls, EBITDA bridge, net working capital, M-score wiring, workbook and chart generation |
| `data/source/` | Every fact as a sourced row (`facts*.csv`), adjustments defined declaratively (`adjustments.yaml`), raw SEC XBRL response |
| `outputs/` | Generated Excel model and charts |
| `scripts/pull_edgar.py` | Reproducible ingestion from the SEC EDGAR XBRL API |

## Design

1. **Provenance is enforced.** Facts carry `FILED` / `DERIVED` / `ASSUMPTION` / `NOT_DISCLOSED`.
   `NOT_DISCLOSED` records that a filing is silent on something, which is recorded as a finding
   rather than a zero.
2. **Adjustments are declarative and adversarial.** Each is defined in YAML and must carry a
   rationale *and* the counterargument a seller would raise, plus a treatment (`ACCEPT` / `REJECT` /
   `SENSITIVITY` / `BOTH`). An `ACCEPT` adjustment with no sourced value raises rather than booking
   zero.
3. **Controls run on every execution.** Fourteen tie-outs — balance sheet balances (equity including
   non-controlling interest), income-statement subtotals foot, EBITDA reconciles. All pass.
4. **The engine is reusable.** `finlib/` contains no company-specific logic and is intended for
   reuse on other issuers.

## Run it

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

./.venv/bin/python main.py                        # controls, cash conversion, bridge, M-score
./.venv/bin/python scripts/build_deliverables.py  # writes Excel model + charts to outputs/
```

Re-pulling source data from SEC requires a contact address in the User-Agent header, per SEC policy:

```bash
export SEC_CONTACT_EMAIL='you@example.com'
./.venv/bin/python scripts/pull_edgar.py
```

Dependencies: `openpyxl`, `matplotlib`, `pyyaml`. Financial logic uses the standard library only.

## Sources

SMCI filings via SEC EDGAR — FY2023 / FY2024 / FY2025 10-K; DEF 14A proxy statements covering
FY2021–FY2025 audit fees; 8-K dated 2024-10-30 (Item 4.01, auditor change). Structured financial
data from SEC's XBRL `companyfacts` API. Full filing index with URLs at `data/source/filings.csv`.

---

*Educational portfolio project analysing public information for a hypothetical transaction. Not
investment advice; not affiliated with or endorsed by SMCI or any advisory firm.*
