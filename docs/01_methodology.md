# Methodology

How this analysis was scoped, what it deliberately does and does not conclude, and the reasoning
behind each adjustment considered.

---

## 1. Scope and framing

This is a **public-information Quality of Earnings analysis** — a Phase 1 / pre-LOI workstream for
a hypothetical take-private of SMCI. A conventional QoE is performed on a target's trial balance,
monthly financials, and management representations. None of those are available here.

That constraint shapes the deliverable rather than undermining it. Where public data supports a
quantification, an adjustment is made. Where it does not, the issue is **sized as an exposure and
converted into a named confirmatory procedure** rather than estimated. Roughly half the issues
identified below are deliberately not booked for this reason.

**Periods:** FY2023, FY2024, FY2025 (fiscal years end June 30). FY2023 serves as the pre-crisis
baseline against which "normal" is measured — without it, every normalization adjustment would be
an assertion rather than a comparison.

---

## 2. Data model and provenance

Financial values are not stored as bare numbers. Each is a record carrying its own origin:

| Field | Purpose |
|---|---|
| `statement` | IS / BS / CF / NOTE / PROXY |
| `line_item` | Label as it appears in the filing |
| `period` | FY2023 … FY2025, or quarter-end |
| `value_usd` | Normalized to whole dollars at load |
| `source` / `ref` | Document and location (e.g. "Note 6, Inventories") |
| `provenance` | `FILED` / `DERIVED` / `ASSUMPTION` / `NOT_DISCLOSED` |

`FILED` is the only source of truth. `DERIVED` values are computed from filed facts and are
reproducible. `ASSUMPTION` values are inputs chosen by the analyst; they are isolated on their own
Excel tab and rendered in a distinct colour. `NOT_DISCLOSED` records the fact that a filing is
silent on something — which is a finding, not a zero.

A lookup for a value that was never sourced **raises an exception**. It does not return zero and
does not interpolate.

**Validation controls** run on every execution: the balance sheet must balance (equity including
non-controlling interest), income-statement subtotals must foot, and GAAP EBITDA must reconcile.
Non-operating items are surfaced explicitly rather than absorbed into a tolerance.

---

## 3. EBITDA bridge structure

The walk is built in three tiers rather than a single column:

```
  GAAP EBITDA  (Operating income + D&A)
    ± management-tier adjustments      → Management-basis EBITDA
    ± diligence-tier adjustments       → Diligence Adjusted EBITDA
    ± sensitivity items                → shown as a range, not booked
```

**Starting from operating income rather than net income is deliberate.** Operating income already
excludes interest income, other income, and the equity-method investee — none of which are
operating. SMCI carries a large cash and investments balance, so beginning from net income would
risk inflating EBITDA with interest income. D&A is taken from the cash flow statement; for an
asset-light model with minimal intangibles, the risk of double-counting debt-issuance-cost
amortization (already inside interest expense) is immaterial but was checked.

---

## 4. Adjustments considered

Every adjustment carries a rationale, the counterargument a seller would raise, and a verdict on
whether it reflects standard market practice. Treatments are `ACCEPT`, `REJECT`, `SENSITIVITY`,
or `BOTH`.

### 4.1 Stock-based compensation — presented on both bases

- **Case for the add-back:** non-cash; excluded from the company's own non-GAAP measures; and the
  comparable-company multiples typically used to value the business are themselves struck on an
  SBC-excluded basis. Excluding SBC from EBITDA while valuing on SBC-inclusive comparables
  double-counts the charge.
- **Case against:** SBC is compensation. Removing it requires replacing it with cash to retain
  engineers, making it a recurring economic cost, and it dilutes the acquirer.
- **Treatment:** neither position is booked. Both bases are presented, and the requirement is that
  the multiple applied be struck on the same basis as the EBITDA it multiplies. The decision is
  worth $314M of FY2025 EBITDA — material enough that consistency matters more than the verdict.

### 4.2 Incremental audit fees — accepted

- **Rationale:** discrete, non-recurring cost of the accounting crisis, sourced from the
  "Principal Accountant Fees and Services" tables in successive proxy statements. FY2025 audit fees
  of $8,084k against a FY2022 pre-crisis baseline of $4,488k gives a delta of $3,596k.
- **Counterargument:** the seller would characterise the entire crisis cost as non-recurring. The
  buy-side position accepts only the audit-fee component; the far larger forensic, legal, and
  consulting costs sit unquantifiably within G&A.
- **Treatment:** `ACCEPT`, presented explicitly as a **floor** on crisis cost, not a total.

### 4.3 Pro forma cost of a compliant finance function — negative sensitivity

- **Rationale:** remediating five material weaknesses is not a one-time event. It implies permanent
  incremental accounting and internal-audit headcount, a SOX programme, systems, and structurally
  higher ongoing audit fees. A properly controlled business carries a **higher** G&A run-rate than
  the historical company ever did — so the adjustment is negative.
- **Counterargument:** the seller would treat remediation as temporary project cost absorbed by
  scale, noting G&A has fallen as a percentage of revenue.
- **Treatment:** `SENSITIVITY`, held as a labelled range ($15–40M/yr) benchmarked to peers rather
  than booked as a point estimate. The same figure is carried into the post-close integration
  budget so the bridge and the integration plan remain consistent.

### 4.4 Related-party pricing — exposure quantified, adjustment not booked

- **Rationale:** 3.3%–6.6% of cost of sales flows through entities affiliated with the CEO's family
  (Ablecom, Compuware), per the Related Party Transactions note. If those entities supply below
  market, reported COGS is understated and margin is subsidised by a relationship the acquirer may
  not inherit.
- **Counterargument:** the arrangements are long-standing, fully disclosed, audit-committee
  reviewed, and represented as at-market.
- **Treatment:** `SENSITIVITY`. Testing related-party pricing is standard practice; booking a
  specific adjustment without a transfer-pricing benchmarking study is not. Exposure is quantified
  and the sensitivity expressed per 100bps of pricing benefit (~$6.5M of FY2025 EBITDA), with the
  benchmarking study made a condition precedent.

### 4.5 Management "non-recurring ramp cost" add-backs — rejected

- **Rationale for rejection:** in a hardware business that has ramped for several consecutive years,
  expedited freight and ramp inefficiency are the cost of operating. The test applied is not whether
  a cost is unusual but **whether it will exist for the buyer next year**.
- **Counterargument:** the seller would characterise these as genuinely one-time, with margins
  normalising at scale.
- **Treatment:** `REJECT`, with the note that the quantum cannot be isolated from public filings
  and would require management's non-GAAP schedule and general-ledger detail.

### 4.6 Issues tested but not adjusted

| Issue | Why no adjustment | What was done instead |
|---|---|---|
| Inventory excess & obsolescence | No reserve is separately disclosed; no aging data | Trend analysis (74% finished goods), flagged as the top confirmatory request |
| Warranty adequacy | Requires claims data | Trend only |
| Revenue cut-off / timing | Requires shipping documents and cut-off testing | Analytical procedures: DSO trend, AR-vs-revenue divergence, accruals ratio |
| Customer concentration | **Not an EBITDA adjustment** | Treated as a multiple and deal-structure issue |

### 4.7 Standard versus aggressive practice

| Adjustment | Verdict |
|---|---|
| Discrete investigation / incremental audit fees | Standard, if substantiated |
| Pro forma cost of a compliant finance function | Standard buy-side |
| SBC add-back | Genuinely contested — not a free add-back |
| Reversing seller "ramp cost" add-backs | Standard buy-side |
| Related-party pricing normalisation | Standard to test; aggressive to book without a study |
| Inventory reserve normalisation | Aggressive without aging data |
| Revenue cut-off adjustment | Cannot be booked without testing |
| Customer concentration | Not an EBITDA adjustment at all |

---

## 5. Net working capital

**Definition used for peg purposes:**

```
  Accounts receivable + Inventories + Prepaid & other current assets
- Accounts payable - Accrued liabilities - Deferred revenue (current)
```

Cash, debt, and income taxes are excluded per the cash-free / debt-free convention.

**On the peg mechanic.** The standard approach — a trailing twelve-month average of NWC — is
inappropriate here. SMCI's working capital is not oscillating around a stable mean; it is
compounding with revenue. A backward-looking dollar peg would sit materially below actual NWC at
close, producing a positive purchase-price adjustment for working capital the buyer was always
going to have to fund. The recommendation is to peg NWC as a **percentage of LTM revenue**, or to
pair a dollar peg with a revenue-linked collar.

Two further constraints are stated rather than worked around: only quarterly data is publicly
available (a negotiated peg requires monthly data, which captures intra-quarter swings that
period-end snapshots hide), and the peg should be adjusted for any inventory that should have been
reserved and for stretched payables at the measurement date.

---

## 6. Cash conversion

Computed on average balances where a prior period exists:

```
DIO = Inventory / COGS × 365      DSO = AR / Revenue × 365
DPO = AP / COGS × 365             CCC = DIO + DSO − DPO
```

Earnings quality is cross-checked with the Sloan cash-flow accruals ratio
`(Net income − Operating cash flow) / average total assets` and the eight-component Beneish
M-score. Both are screens rather than verdicts — the M-score in particular was calibrated on mature
manufacturers and will register elevated readings for a hyper-growth business for entirely benign
reasons, so components are reported individually rather than only as a composite.

The walk is completed as **Adjusted EBITDA less capital expenditure less the increase in net
working capital**, which is the measure a buyer actually underwrites.
