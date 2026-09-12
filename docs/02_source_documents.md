# Source Documents and Verification

Every figure in this analysis traces to one of the filings below. Structured financial-statement
data was pulled programmatically from SEC's XBRL `companyfacts` API; note-level and narrative
disclosures were read directly from the filing text and verified against the source HTML.

---

## 1. Filings used

### Annual reports

| Filing | Filed | Accession | Used for |
|---|---|---|---|
| FY2025 10-K | 2025-08-28 | 0001375365-25-000027 | Primary financial statements; FY2024/FY2023 comparatives; Notes 1, 4, 6; Related Party Transactions |
| FY2024 10-K | 2025-02-25 | 0001375365-25-000004 | Item 9A (controls); auditor reports; Critical Audit Matters |
| FY2023 10-K | 2023-08-28 | 0001375365-23-000036 | Pre-crisis baseline; predecessor auditor confirmation |

The FY2024 10-K carries a 2025 accession number — the signature of the delayed filing.

### Proxy statements (audit fees)

| Filing | Filed | Fiscal years reported |
|---|---|---|
| DEF 14A | 2026-03-03 | FY2025, FY2024 |
| DEF 14A | 2025-04-24 | FY2024, FY2023 |
| DEF 14A | 2023-04-14 | FY2022, FY2021 |

A proxy reports audit fees for the two most recently completed fiscal years, so the three filings
together give a continuous FY2021–FY2025 series. The FY2022 figure is the pre-crisis baseline used
in the incremental-audit-fee adjustment.

### Current reports

| Filing | Date | Content |
|---|---|---|
| 8-K (Item 4.01) | 2024-10-30 | Auditor resignation; Exhibit 16.1 resignation letter |
| NT 10-K | 2024-08-30 | Late-filing notification and stated cause of delay |
| 8-K | 2024-12-02 | Special Committee review conclusion (Ex. 99.1) |
| 8-K | 2025-02-21 | Filing / listing-compliance announcement |

A complete filing index with direct URLs is generated at `data/source/filings.csv`.

---

## 2. Note-level disclosures relied upon

| Disclosure | Location | Used for |
|---|---|---|
| Inventories | FY2025 10-K, Note 6 (Balance Sheet Components) | Finished goods / WIP / raw materials split |
| Revenue recognition | FY2025 10-K, Notes 1 and 4 | Timing of transfer of control |
| Related party transactions | FY2025 10-K | Purchases, sales, and balances by counterparty |
| Controls and procedures | FY2024 10-K, Item 9A | Material weaknesses; remediation status |
| Auditor reports | FY2024 10-K, Item 8 (pp. 63–66) | Opinions on financial statements and ICFR; CAMs |
| Principal Accountant Fees | DEF 14A | Audit fees by year and firm |

---

## 3. Verification performed

**Cross-source agreement.** Figures pulled from the XBRL API were checked against the filing text.
Income-statement, balance-sheet, and cash-flow figures agreed exactly across both sources.

**Internal footing.** Operating expense components foot to total operating expenses in all three
years; inventory components foot to the balance sheet total; related-party components foot to the
disclosed totals.

**Automated controls.** Fourteen tie-out checks run on every execution of the model — balance sheet
balances (equity including non-controlling interest), gross profit reconciles to revenue less cost
of sales, and operating income reconciles to gross profit less operating expenses. All pass.

**Unit consistency.** SMCI reports in thousands. All values are normalized to whole dollars at load
so no downstream calculation mixes conventions. One early discrepancy — operating income failing to
foot by $10k–$78k — was traced to operating-expense figures transcribed from a MD&A table stated in
millions, and resolved by substituting exact-dollar XBRL values rather than widening the tolerance.

---

## 4. Disclosures not available

Recorded as `NOT_DISCLOSED` rather than assumed:

- **Inventory excess-and-obsolescence reserve.** Not separately disclosed. The note states that
  once inventory is written down the new value is maintained, so write-downs are embedded in the
  carrying value and no roll-forward is presented.
- **Crisis-related professional fees.** Not broken out; captured within general and administrative
  expense.
- **Warranty claims experience.** Not available at the level needed to test accrual adequacy.

---

## 5. Data not obtainable from public filings

The following would be requested in a live engagement and are listed in the IC memo as confirmatory
procedures:

- Monthly trial balance and financial statements, 24–36 months
- Inventory aging by SKU or generation and the E&O reserve calculation
- Revenue cut-off testing around each quarter-end (shipping documents against revenue dates)
- General-ledger detail for professional fees by vendor
- Customer-level revenue, margin, and receivables aging
- Transfer-pricing or arm's-length benchmarking study for related-party arrangements
