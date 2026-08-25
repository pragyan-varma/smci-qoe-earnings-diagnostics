# SMCI Quality of Earnings — Project Architecture

**Status:** Design only. No code, no numbers. Every figure below is a placeholder to be
populated from a primary source document.

**Standing rule for this project:** no figure enters the model unless it carries a source
reference (document, statement or note, line-item label). Anything I cannot source, I flag
as an open diligence item rather than estimating.

---

## 0. Scope decisions to lock before we build

### 0.1 The deal framing

A QoE is normally performed on a private target where you have the trial balance, monthly
financials, and management access. We have none of that. **Do not pretend otherwise — say it
out loud in the memo.** The honest framing, and the one that survives a CPA's questioning:

> "Buy-side diligence workstream for a hypothetical take-private of SMCI. This is a
> *public-information QoE* — Phase 1. I identify and, where possible, quantify the earnings
> quality issues; where public data cannot support a quantification, I convert the issue into
> a specific confirmatory diligence procedure with a named data request."

That reframe turns your biggest weakness (no data room) into the structure of the deliverable.
A real Phase 1 / pre-LOI diligence memo looks exactly like this. Own it.

### 0.2 Period scope — I recommend changing yours

You proposed FY2024 10-K + FY2025 10-Qs. That was the right scope in early 2025. It is stale
now (July 2026). The FY2025 10-K (FYE June 30, 2025) and subsequent FY2026 10-Qs should be on
EDGAR. Recommended scope:

- **Historical period:** FY2023, FY2024, FY2025 (fiscal years end June 30).
- **LTM / stub:** trailing twelve months through the most recent filed 10-Q.
- **Why LTM matters:** QoE is underwritten on LTM Adjusted EBITDA, not the last audited year.
  Presenting only FY24 tells an interviewer you copied a 2025 blog post.

**Why FY2023 must be in the walk:** you need a *pre-crisis* baseline. Almost every adjustment
below is an argument about what "normal" looks like. Without FY23, you have nothing to
normalize against and every adjustment becomes an assertion.

Confirm the actual fiscal-period coverage from the filings themselves before committing.

---

## 1. Primary source pull list (SEC EDGAR)

Pull these from `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=SMCI&type=...`
or EDGAR full-text search. **Verify every date yourself — I am telling you what to look for,
not asserting what you will find.**

### 1.1 The event chain (8-Ks and related)

| # | Document | What it establishes | What to extract |
|---|---|---|---|
| 1 | **8-K, Item 4.01 — auditor resignation (expected on/around Oct 30, 2024)** | EY's resignation and its stated reasons | The **EY resignation letter, filed as an exhibit** (usually Ex-16.1). Read the *exact* language. Note whether EY states it is unwilling to be associated with management-prepared financials, whether it identifies disagreements, and whether it identifies reportable events under Reg S-K Item 304(a)(1)(v). |
| 2 | **NT 10-K (late-filing notification), FY2024 (expected ~Aug/Sept 2024)** | The original delay and management's stated reason | Management's stated cause of delay — compare it later to what the 10-K actually says. |
| 3 | **8-K — Nasdaq deficiency notice (expected Sept 2024)** and **8-K — compliance plan** | The listing-compliance timeline | Dates and the deadline granted. |
| 4 | **8-K — Special Committee investigation conclusion (expected ~Dec 2, 2024)** | Findings; whether misconduct was found; remedial recommendations | The **press release exhibit (Ex-99.1)**. Critically: how many remedial actions were recommended, and were they *implemented* by the time of the FY24 10-K? |
| 5 | **8-K, Item 4.01 — new auditor engagement (BDO expected, late 2024)** | Successor auditor appointment | Engagement date. This drives the audit-fee bridge in §3. |
| 6 | **8-K — regained Nasdaq compliance (expected Feb 2025)** | Closure of the listing issue | Date. |
| 7 | **Any 8-K disclosing DOJ / SEC inquiry or subpoena** | Regulatory exposure | Whether an inquiry is *disclosed by the company* vs. only press-reported. This distinction matters — do not cite press reporting as fact in the memo. |

### 1.2 The core financial documents

| # | Document | Why |
|---|---|---|
| 8 | **FY2024 10-K (FYE 6/30/2024, expected filed ~Feb 25, 2025)** | The central document. |
| 9 | **FY2025 10-K (FYE 6/30/2025)** | Full audited FY25, plus FY24/FY23 comparatives. Your primary source now. |
| 10 | **FY2023 10-K** | Pre-crisis baseline; also the *original* FY23/FY22 figures as filed. |
| 11 | **All FY2025 and FY2026 10-Qs filed to date** | LTM build and quarter-end skew testing. |
| 12 | **DEF 14A proxy statements, FY2023 / FY2024 / FY2025** | Two things: (a) the **"Principal Accountant Fees and Services"** table — this is your *hard, sourced* audit-fee delta; (b) the **related-party transaction** disclosure. |
| 13 | **SEC enforcement record from 2020** (AAER / litigation release re: the prior SMCI accounting matter) | Establishes whether this is a first offense or a pattern. Pull the SEC's own release, not a news article. |

### 1.3 The specific sections to read closely, in priority order

Within the FY2024 and FY2025 10-Ks:

1. **Item 9A — Controls and Procedures.** Read every word.
   - Management's conclusion on disclosure controls (effective / not effective?).
   - Management's conclusion on ICFR.
   - The **enumerated material weaknesses** — extract the *exact* list and the COSO component
     each maps to (Control Environment / Risk Assessment / Control Activities / Information &
     Communication / Monitoring). The COSO mapping tells you whether these are *entity-level*
     weaknesses (severe — implicates tone at the top) or *process-level* (contained). This
     distinction is the single most defensible technical point you can make in the interview.
   - The **remediation plan** and its stated timeline and cost.
2. **The auditor's report(s).** This is subtle and it is where you differentiate:
   - Who signed the opinion on the FY2024 financial statements?
   - Is there a **separate opinion on ICFR**? SMCI is very likely a large accelerated filer, so
     auditor attestation on ICFR is required. If material weaknesses exist, expect an **adverse
     opinion on ICFR alongside an unqualified opinion on the financial statements.** Confirm this.
   - **Critical Audit Matters (CAMs)** — the auditor is telling you, in writing, which accounts
     it found hardest to audit. Whatever the CAMs are, those accounts belong in your QoE scope.
     This is free diligence direction from a professional who had the trial balance.
   - **Who audited the comparative years?** If the FY24 10-K carries a predecessor auditor's
     report for FY23/FY22, then the prior-year opinions are still standing — issued by a firm
     that later resigned. Determine whether any prior opinion was **withdrawn** or whether
     investors were told they could no longer rely on it. *This is the technical heart of your
     "no restatement, yet reporting risk existed" tension.*
3. **Note — Revenue Recognition** (timing of transfer of control; any bill-and-hold language;
   distributor / channel arrangements; contract balances).
4. **Note — Related Party Transactions.** Expect to find purchases from and sales to entities
   affiliated with the CEO's family. Extract *every* number in this note for all periods.
5. **Note — Balance Sheet Components** (inventory by category; accrued liabilities detail;
   prepaid expenses detail).
6. **Note — Product Warranty** (accrual roll-forward).
7. **Note — Concentration of Credit Risk / Segment** (customers >10% of revenue, by year).
8. **Note — Debt** (convertible notes: principal, coupon, conversion terms, maturities; term
   loans; revolver).
9. **Note — Commitments and Contingencies** (litigation, purchase commitments).
10. **Note — Income Taxes** (including the unrecognized tax benefits / uncertain tax positions
    roll-forward — this is a debt-like item).
11. **Schedule II — Valuation and Qualifying Accounts**, if presented (allowance and reserve
    roll-forwards). If it is not presented, note that as a data gap.
12. **MD&A** — the gross-margin walk and the operating-expense commentary. This is where
    management will *characterize* costs as non-recurring; capture their exact language, because
    in the memo you will litigate each characterization.
13. **Risk Factors** — Item 1A. Skim for newly added risk factors year-over-year; new risk
    factors are a disclosure signal.

### 1.4 What you will *not* find, and must therefore request

Build this list into the memo as the "Confirmatory Diligence Request" appendix. It proves you
know what a real QoE requires:

- Monthly trial balance / monthly P&L for 24–36 months (for seasonality, cut-off, and a
  monthly NWC trend).
- General ledger detail for professional fees by vendor (to substantiate the crisis-cost add-back).
- Inventory aging by SKU / generation, and the E&O reserve calculation and policy.
- Revenue cut-off testing around each quarter-end (shipping documents vs. revenue date).
- Customer-level revenue, margin, and AR aging.
- The related-party contracts and any transfer-pricing / arm's-length benchmarking study.
- The Special Committee's underlying report and the forensic accountants' workpapers (you will
  not get these; ask anyway and note the refusal).

---

## 2. Data model: how a number gets into this project

Before any adjustment logic, the ingestion layer enforces the no-fabrication rule structurally.
Every value is a record, not a float:

```
Fact:
  period          FY2023 | FY2024 | FY2025 | Q1FY26 | ... | LTM
  statement       IS | BS | CF | NOTE | PROXY | XBRL
  line_item       exact label as it appears in the filing
  value           the number, in the filing's units
  units           USD thousands / USD millions  (normalize once, at the boundary)
  source_doc      e.g. "SMCI FY2025 10-K"
  source_ref      e.g. "Note 5 — Balance Sheet Components, Inventories"
  provenance      FILED | DERIVED | ASSUMPTION
```

`provenance` is the whole point:

- **FILED** — typed or parsed directly from a filing. The only thing allowed to be a source of truth.
- **DERIVED** — computed from FILED facts by code. Must be reproducible.
- **ASSUMPTION** — an input we chose (e.g., an EBITDA multiple for the sensitivity grid). Must
  be small in number, listed on its own tab in the Excel output, and **rendered in a different
  font color** so nobody — including the interviewer — can mistake it for a sourced figure.

If code asks for a Fact that does not exist, it raises. It does not default to zero and it does
not interpolate. That behavior *is* the deliverable's credibility.

**Do not scrape XBRL as the primary path.** Type the source facts into a CSV by hand, with the
note reference in a column. It is maybe 150 numbers. Hand-entry forces you to actually read the
filings, which is the part that makes you defensible in the interview, and it eliminates a whole
class of tagging bugs you would otherwise have to explain. Optionally use XBRL (via the SEC
`companyfacts` API) as an *independent tie-out check* against your hand-entered file — that's a
control, and describing it as one is a good interview beat.

---

## 3. The EBITDA bridge — adjustment hypotheses

### 3.1 Structure the bridge the way a real QoE report does

Not a single-column walk. Three tiers:

```
  GAAP Net Income                                    [Income Statement]
    + Interest expense, net                          [IS / Note — Debt]
    + Provision for income taxes                     [IS]
    + Depreciation & amortization                    [Cash Flow Statement]
    - Other (income) expense, net                    [IS — see trap below]
  = GAAP EBITDA
    ± Management-proposed adjustments (each shown separately)
  = "Management Adjusted EBITDA"                     ← what the seller will market
    ± Diligence adjustments: ACCEPT / REJECT / RE-MEASURE
  = Diligence Adjusted EBITDA                        ← what we underwrite
    ± Sensitivity items (not booked; shown as a range)
  = Adjusted EBITDA — downside case
```

The middle tier is the differentiator. SMCI publishes its own non-GAAP measures. Reproducing
management's number, then *litigating each of their add-backs line by line*, is exactly what a
QoE report does and exactly what an interviewer wants to see you do.

**D&A trap (a CPA will check this).** The D&A line on the cash flow statement may bundle
amortization of debt issuance costs and/or operating-lease ROU amortization. Debt issuance cost
amortization is already inside interest expense — add it back twice and your EBITDA is wrong.
Tie D&A to the PP&E and intangibles notes, not just to the cash flow line. Document the tie-out.

**Interest income trap.** SMCI holds a large cash and investments balance. Interest *income* is
non-operating and must not inflate EBITDA. Check whether management's non-GAAP measures net it
in. If they do, that is a finding.

### 3.2 The adjustment inventory

For each: the hypothesis, the source, the seller's counterargument, and — most importantly —
whether it is **market-standard** or **aggressive**. Know the difference cold; the fastest way
to lose credibility with a CPA is to book an aggressive adjustment as if it were routine.

---

#### A. Stock-based compensation — **the contested one. Do not pick a side; price both.**

- **Source:** Income statement / SBC note (expense by line: COGS, R&D, S&M, G&A) and the cash
  flow statement add-back.
- **Buy-side position (reject the add-back):** SBC is compensation. If you strip it out, you must
  replace it with cash to retain the engineers, so it is a real, recurring, run-rate economic
  cost. It also transfers value away from the buyer through dilution.
- **Seller position (add it back):** it is non-cash, it is excluded from the company's own
  reported non-GAAP measures, and the comparable-company multiples that will be used to value the
  business are themselves computed on an SBC-excluded basis. Excluding it from EBITDA but valuing
  on SBC-inclusive comps double-counts the charge.
- **Market practice:** In tech/hardware deals, adding back SBC is *common* but genuinely
  contested — it is not the free add-back it is often treated as. Sponsors increasingly haircut it.
- **How to be right:** present **both** — "Adjusted EBITDA (pre-SBC)" and "Adjusted EBITDA
  (post-SBC)" as parallel columns, and show the purchase-price delta between them at a constant
  multiple. Then separately quantify **dilution**: pull diluted share count and the SBC note, and
  show the annual dilution rate. The correct answer in an interview is: *"I don't book it either
  way. I show that the entire debate is worth $X of enterprise value, and I make sure the
  valuation multiple I apply is computed on the same basis as the EBITDA I apply it to."*
  Multiple-and-metric consistency is the point. That answer is unassailable.
- **Extra credit:** split recurring SBC from any discrete/one-off grants (mega-grants, retention
  awards tied to the crisis). Those may deserve different treatment. Check the SBC note and the proxy.

---

#### B. Non-recurring costs of the accounting crisis — **standard in principle, but the naive version is a trap**

- **Hypothesis:** Investigation costs, forensic accountants, Special Committee counsel,
  incremental audit fees, and re-audit/catch-up costs are discrete and non-recurring. Add back.
- **Source problem — say this out loud:** the 10-K will almost certainly **not** break these out
  as a separate line. MD&A may *characterize* an increase in G&A, but a characterization is not a
  quantification. **You cannot book this add-back from public filings.** State that. It is a
  finding, not a failure.
- **What you *can* source, hard:** the **DEF 14A "Principal Accountant Fees and Services" table.**
  Audit fees by year, by firm. FY23 (pre-crisis) vs. FY24/FY25 gives you a defensible, fully
  sourced quantification of *the audit-fee component*. That is a real number with a real citation.
  It is a floor on the crisis cost, and you should present it as exactly that — a floor, not the
  total.
- **Seller counterargument:** "Obviously non-recurring — the investigation is over."
- **The buy-side answer that wins the room:** *"Partially. I'll accept the discrete
  investigation and incremental audit costs, subject to invoice-level substantiation. But I will
  not accept the remediation costs, and I'm going to add a cost back the other way."*

  **This is the most important idea in the whole project.** Remediating material weaknesses is
  not a one-time event. It means permanent incremental headcount in accounting and internal audit,
  a real SOX program, systems, and higher ongoing audit fees. A properly controlled SMCI has a
  **structurally higher G&A run-rate than the historical SMCI ever had.** So the bridge needs a
  **negative** adjustment: *"Pro forma cost of a compliant finance function."*

  A negative EBITDA adjustment, in a project where every student instinct is to add things back to
  make EBITDA bigger, is the single clearest signal that you are thinking like a buyer instead of
  a banker. Lead the interview with this.
- **How to size it without fabricating:** you cannot know it precisely. Do it as a **labeled
  ASSUMPTION with a stated methodology** — e.g., benchmark accounting/finance headcount and audit
  fees against a peer set you build from public filings (peers' proxy audit-fee tables and 10-K
  G&A), express it as a range, and run it as a *sensitivity*, not a booked adjustment. Sourced
  methodology + labeled assumption + presented as a range = defensible. A single made-up number =
  indefensible. This is the difference and you should be able to articulate it.

---

#### C. Related-party transactions — **the highest-value finding in the filings, and almost nobody doing a student project will touch it**

- **Hypothesis:** SMCI has long disclosed transactions with entities affiliated with the CEO's
  family (expect names along the lines of Ablecom and Compuware — **verify in the Related Party
  Transactions note**), covering contract manufacturing, chassis/component purchases, and
  distribution. Confirm the counterparties, the nature of the transactions, and the dollar amounts
  for every period, from the note itself.
- **Why it belongs in a QoE:** if the related party supplies SMCI **below market**, reported COGS
  is understated and **EBITDA is flattered by a subsidy from the founder's family.** A buyer
  acquiring the company does not necessarily inherit that pricing. The correct treatment is a
  **negative adjustment to restate COGS to arm's-length pricing.** If the pricing runs the other
  way, the adjustment is positive. Either way, the *quality* of that earnings stream is impaired
  because it depends on a relationship, not a contract.
- **Also a control issue:** related-party transactions with the CEO's family, at a company with an
  identified control-environment material weakness, is precisely the fact pattern that governance
  and audit committees exist to catch. Tie this back to your COSO mapping in §1.3.
- **Seller counterargument:** these arrangements are long-standing, fully disclosed, reviewed by
  the audit committee, and priced at market; the auditor and the Special Committee examined them.
- **Market practice:** testing related-party pricing is **absolutely standard** in FDD. Booking a
  specific pricing adjustment without a benchmarking study is **aggressive**. So: quantify the
  *exposure* (total related-party COGS as a % of total COGS — fully sourced from the note), state
  the *sensitivity* (each 100bps of pricing benefit = $X of EBITDA — mechanically derived, not
  invented), and make the arm's-length benchmarking study a **condition precedent** in your
  diligence request list. That is exactly how a Director would land it.

---

#### D. Inventory reserves and E&O — **standard to test, aggressive to book on public data**

- **Hypothesis:** rapid scaling plus generational GPU/platform transitions creates obsolescence
  risk on prior-generation inventory. If the E&O reserve rate declined while inventory days rose
  and product cycles shortened, the reserve may be inadequate and EBITDA overstated.
- **Source:** inventory note (raw materials / WIP / finished goods split), Schedule II if present,
  MD&A gross-margin commentary, and any disclosed write-down.
- **The tests you can actually run on public data:**
  - Reserve as % of gross inventory, by period (needs Schedule II or the note; if neither
    discloses gross vs. net, **say so — that is itself a disclosure finding**).
  - Days inventory outstanding, by period, against revenue growth.
  - Finished goods vs. raw materials mix shift (a finished-goods build is a demand signal;
    a raw-materials build is a supply/pre-buy signal — very different stories).
- **Seller counterargument:** reserves are set per a consistent policy, the auditor tested them,
  and the build-to-order model plus committed customer demand limits true obsolescence exposure.
- **Treatment:** **Do not book a reserve adjustment.** You cannot support it. Present the trend
  analysis, state the directional risk, quantify a sensitivity (a 100bps change in reserve rate =
  $X — mechanically derived from the sourced gross inventory balance), and make inventory aging
  the #2 item on the confirmatory diligence list. Booking an unsupported reserve adjustment is
  precisely the "aggressive" move a CPA will call you on.

---

#### E. Warranty provisioning — same logic, smaller magnitude

- **Source:** product warranty accrual roll-forward (beginning balance, provision, utilization,
  ending balance).
- **Test:** warranty provision as % of revenue, by period. If it fell while product complexity
  rose (higher GPU density, direct liquid cooling, more field-serviceable systems), that is a
  potential under-accrual.
- **Seller counterargument:** improved product reliability; more of the fleet under
  customer-negotiated service contracts rather than base warranty; mix shift to hyperscale
  customers who self-service.
- **Treatment:** same as inventory — trend + sensitivity, not a booked adjustment. Market practice
  is that normalizing an under-accrued warranty *is* a legitimate QoE adjustment, but only with
  claims data. You do not have claims data. Say so.

---

#### F. Revenue recognition timing — **the one you flag loudest and book least**

- **Why it's live:** the prior SEC matter and the short-seller allegations both centered on
  revenue timing and channel behavior. Whatever you find, this is the account with the highest
  inherent risk, and the auditor's CAMs will likely confirm it.
- **What to read:** the revenue recognition note (point-in-time vs. over-time; transfer of
  control; any **bill-and-hold** language — bill-and-hold has a strict five-criteria test under
  ASC 606 and is a classic aggressive-recognition vehicle); contract balances / deferred revenue;
  distributor and channel arrangements; and the treatment of partial shipments.
- **What you can test from public data (all legitimate analytical procedures):**
  - **DSO by period.** Rising DSO against flat terms is a timing signal.
  - **Revenue growth vs. AR growth divergence.** AR outgrowing revenue persistently is the single
    most cited earnings-quality red flag.
  - **Quarter-end skew.** Using the 10-Qs, look at the distribution of revenue across quarters and
    at Q4 (fiscal June) specifically. Disproportionate period-end loading is a cut-off signal.
  - **Accruals ratio** — (Net income − Operating cash flow) / average total assets. This is a
    published academic earnings-quality metric (Sloan) and it is *devastating* for a company with
    positive net income and deeply negative operating cash flow. It is also a clean, citable,
    non-fabricated number.
- **Treatment:** **You cannot book a revenue adjustment.** Cut-off testing requires shipping
  documents you will never see. Correct answer: "Revenue cut-off testing is the #1 confirmatory
  procedure and I would not sign a purchase agreement without it. Here are the four analytical
  procedures I ran on public data, here is what they suggest, and here is the specific testing I'd
  scope." That answer is *better* than a fake adjustment, and a CPA will recognize it as such.

---

#### G. Costs management will call "non-recurring ramp costs" — **reject most of it**

- Expect MD&A to attribute gross-margin compression to things like expedited freight, air
  shipments, direct-liquid-cooling ramp inefficiency, and competitive pricing on AI platforms.
  Capture their exact words.
- **Seller position:** one-time ramp costs; margins normalize at scale.
- **Buy-side position:** in a hardware business that has been "ramping" for several consecutive
  years, expedite freight and ramp inefficiency are the **cost of operating**, not an anomaly.
  Recurring costs do not become non-recurring because they are inconvenient. Reject, or accept only
  a discrete, substantiated slice.
- This is a good place to demonstrate the general principle: **the test for a non-recurring
  add-back is not "unusual" — it is "will this cost exist for the buyer next year?"** Say that
  sentence in the interview.

---

#### H. Customer concentration — **NOT an EBITDA adjustment. Do not put it in the bridge.**

Putting concentration in the EBITDA bridge is a tell that someone doesn't understand what the
bridge is. It is a **risk and multiple issue**, and it belongs in the memo, not the walk.

- **Source:** the concentration-of-credit-risk / segment note (customers >10% of revenue, by year).
- **Where it goes:**
  1. **Valuation:** concentration compresses the multiple. Argue it explicitly.
  2. **Working capital:** a small number of large customers drives AR credit risk and gives those
     customers leverage over payment terms. It is a direct input to the DSO story.
  3. **Deal structure:** it drives escrow, earn-out, and customer-consent conditions.
- **The one case where it *does* hit the bridge:** if a >10% customer was lost or materially
  reduced after the period end, you take a **pro forma adjustment to remove that revenue and its
  contribution margin.** Check subsequent events and the risk factors for exactly this.

---

### 3.3 The standard-vs-aggressive cheat sheet

Memorize this table. It is the most likely thing you get quizzed on.

| Adjustment | Verdict | Why |
|---|---|---|
| Discrete investigation / forensic / incremental audit fees | **Standard** — *if substantiated at invoice level* | Genuinely discrete event. But quantum requires GL detail; unsubstantiated, it's a plug. |
| Pro forma cost of a compliant finance function (**negative**) | **Standard buy-side** | Correcting for an under-resourced function is textbook FDD. |
| SBC add-back | **Contested, not free** | Present both bases; keep metric and multiple consistent. |
| Reversing seller's "ramp cost" add-backs | **Standard buy-side** | Multi-year recurring costs are not non-recurring. |
| Related-party pricing normalization | **Standard to test / aggressive to book** without a benchmarking study | Quantify exposure + sensitivity; make the study a condition precedent. |
| Inventory E&O reserve normalization | **Aggressive** without aging data | Trend + sensitivity only. |
| Warranty normalization | **Aggressive** without claims data | Trend + sensitivity only. |
| Revenue cut-off / timing adjustment | **Cannot book** without cut-off testing | Analytical procedures + scoped test request. |
| Customer concentration | **Not an EBITDA adjustment at all** | Multiple and structure, not the bridge. |

**The meta-point, and your best single line in the interview:**

> "About half of what I found, I refused to book. Not because it isn't real, but because the
> public record can't support it. In a live deal I'd have the trial balance and I'd test it. What
> I can do from here is size the exposure and tell the deal team exactly what to test — and how
> much of the purchase price is riding on each answer."

That is a Director's answer. Booking eight confident adjustments off a 10-K is an intern's answer.

---

## 4. Net working capital analysis

### 4.1 Definition (state it explicitly in the memo — every NWC fight is a definition fight)

Start from the balance sheet, then justify each exclusion:

```
  Accounts receivable, net
+ Inventories
+ Prepaid expenses and other current assets       ← decompose this; see below
- Accounts payable
- Accrued liabilities                              ← decompose; see below
- Deferred revenue, current                        ← see debate below
= Net Working Capital (for peg purposes)
```

**Excluded, and why:**
- **Cash and investments** — cash-free / debt-free convention.
- **Current portion of debt, accrued interest** — debt, not working capital.
- **Income taxes payable / receivable** — conventionally excluded from the peg and settled
  separately in the equity bridge. State the convention you chose; either can be defended, but
  you must be consistent between the peg and the actual.

**Items that require you to look inside the notes, not just the face of the balance sheet:**
- **Prepaid expenses and other current assets.** Expect supplier prepayments/deposits (paying
  upfront for constrained components). That is a *real cash drag* and it is a genuine working
  capital item. If it is material, it deserves its own line in your NWC schedule rather than
  being buried. Pull the composition from the balance-sheet-components note.
- **Accrued liabilities.** Expect a mix: payroll, warranty, customer deposits, accrued
  professional fees. **Customer deposits are the one to argue about** — they are a source of
  cash but they represent an obligation to deliver product. Are they working capital, or are they
  debt-like? Take a position and defend it. (Reasonable position: they are working capital if
  they cycle with the business, but you must confirm they are not a financing arrangement in
  disguise.)
- **Deferred revenue.** Standard working capital item, but note the classic tension: in a deal,
  deferred revenue is sometimes haircut to the cost of fulfilling the obligation plus a margin.
  Flag the debate; you don't need to resolve it.

### 4.2 The peg — and why the obvious answer is wrong

The standard mechanic is a peg set at a trailing 12-month average of NWC. **For SMCI that is
actively dangerous, and explaining why is a strong interview moment.**

SMCI's NWC is not oscillating around a stable mean — it is *growing violently and monotonically
with revenue*. A trailing-average peg on a business whose working capital is compounding will
systematically **advantage the seller**: the target (a backward-looking average) sits far below
the actual NWC at close (a forward-looking, much larger number), and the buyer pays a positive
purchase-price adjustment for working capital it was always going to have to fund anyway. The
buyer effectively finances the seller's growth and calls it a true-up.

**The defensible answer:** peg NWC as a **percentage of LTM revenue**, not as an absolute dollar
amount — or set a dollar peg and pair it with a revenue-linked collar. Then:

1. Compute NWC % of revenue for every period you have. Show whether it is stable, deteriorating,
   or improving. That ratio, not the dollar amount, is the real operating metric.
2. Adjust the peg for anything that shouldn't be in it: inventory that should have been reserved,
   AR that is not collectible, and any **stretched AP at the measurement date** (an artificially
   high AP balance at close flatters NWC in the seller's favor — check whether DPO spikes at
   period ends).
3. Say clearly: *"A conventional 12-month-average peg transfers value to the seller in a
   working-capital-hungry growth business. I'd negotiate the peg as a percentage of LTM revenue,
   and I'd want monthly NWC data for 24 months before I'd agree to any number."*

The last clause matters: **you only have quarterly data.** A real peg is negotiated off monthly
data because it captures intra-quarter swings and seasonality that quarter-end snapshots hide —
and quarter-end snapshots are exactly the dates a company is most motivated to manage. State this
limitation. It is a strength.

### 4.3 The cash conversion cycle — and the punchline of the whole project

Compute, per period:

- **DIO** = Inventory ÷ COGS × 365
- **DSO** = Accounts receivable ÷ Revenue × 365
- **DPO** = Accounts payable ÷ COGS × 365
- **CCC** = DIO + DSO − DPO

*(Use average balances where you have them; be consistent; state the convention.)*

**The story you are testing** — and you must let the data confirm or refute it, not assume it:
revenue grows fast, inventory grows faster (pre-buying constrained components), suppliers demand
cash or prepayment rather than extending terms (so DPO does not keep up), and a concentrated
customer base has leverage on payment terms (so DSO does not improve). CCC extends. Every
incremental dollar of revenue consumes cash. Reported net income is positive; operating cash flow
is negative.

**Then land the plane:**

```
  Diligence Adjusted EBITDA
- Capital expenditures                     [Cash Flow Statement — investing]
- Increase in net working capital          [derived from your NWC schedule]
= Cash EBITDA / unlevered cash conversion
```

If that number is negative or near zero while Adjusted EBITDA is meaningfully positive, then
**the QoE bridge, however carefully built, is not the finding — the cash conversion is.** A buyer
underwrites cash, not accruals. An LBO on this asset does not fail because EBITDA was $X instead
of $Y; it fails because growth is unfundable without a revolver the size of the EBITDA.

That is the memo's thesis and it is the answer to "so what did you actually conclude?"

---

## 5. Python roadmap

### 5.1 Design principle: build the shared library first, the QoE second

You said you want to reuse components for an anomaly screener. Then the QoE is a *consumer* of a
core library, not a script that you will later cannibalize. Structure accordingly:

```
smci_qoe_project/
├── data/
│   ├── source/
│   │   ├── facts.csv                # hand-entered, one row per Fact (see §2). The source of truth.
│   │   ├── adjustments.yaml         # adjustment definitions: rationale, counterargument, treatment
│   │   └── assumptions.yaml         # every ASSUMPTION, isolated and few. Nothing else may be one.
│   └── raw/                         # the actual filings (PDF/HTML) — commit these; provenance matters
│
├── finlib/                          # ← the reusable core. Project 2 imports THIS.
│   ├── facts.py                     # Fact, FactSet, provenance enum, strict lookup (raises on miss)
│   ├── statements.py                # typed accessors: revenue(p), cogs(p), inventory(p)...
│   ├── diagnostics.py               # ← the shared brain. DSO/DIO/DPO/CCC, accruals ratio,
│   │                                #   margin trends, reserve rates, AR-vs-revenue divergence,
│   │                                #   Beneish M-score components, Sloan accruals.
│   ├── validate.py                  # tie-out controls (see below)
│   └── xlsx/
│       ├── styles.py                # number formats, fonts, the input-vs-formula color convention
│       └── writer.py                # generic "write a schedule to a sheet" helper
│
├── qoe/                             # ← project-specific
│   ├── ebitda.py                    # GAAP EBITDA build (with the D&A tie-out)
│   ├── bridge.py                    # Adjustment model + the three-tier walk
│   ├── nwc.py                       # NWC schedule, peg analysis, CCC
│   ├── excel.py                     # the deliverable workbook
│   └── charts.py                    # waterfall
│
├── outputs/
└── main.py
```

`finlib/diagnostics.py` is the piece that carries straight into the anomaly screener. **Beneish
M-score is the natural bridge between the two projects** — its inputs (DSRI, GMI, AQI, SGI, DEPI,
SGAI, LVGI, TATA) are exactly the ratios a QoE computes anyway, and it was built for precisely
this question. Compute it here, reuse the engine there. Mentioning that you found the M-score
components fall out of the QoE for free is a good way to make the two projects sound like one
coherent body of work rather than two assignments.

### 5.2 Step 1 — Ingestion and normalization → GAAP EBITDA

- Load `facts.csv` into a `FactSet`. Enforce: every row has a `source_doc` and `source_ref`, or
  ingestion fails.
- Normalize units once, at the boundary (10-Ks are usually in thousands; don't let a mixed-unit
  bug into the model).
- **Build a validation layer that runs on every execution and fails loudly:**
  - Balance sheet balances (assets = liabilities + equity), per period.
  - Cash flow statement ties to the change in the cash balance.
  - Income statement subtotals foot.
  - GAAP EBITDA reconciles from both net income *and* operating income; if the two paths
    disagree, the difference is other income/expense — and it must be *explained*, not silenced.
  - Optional: tie every hand-entered fact to the SEC XBRL `companyfacts` API and report variances.
- **Why this matters more than it looks:** you are building a QoE on a company whose defining
  failure was a lack of controls. Building *controls into your own model* — and describing them
  as controls — is a rhetorical layup. Have a slide/section for it.

### 5.3 Step 2 — The bridge

Each adjustment is a declarative object, defined in YAML, not buried in code:

```yaml
- id: ADJ-002
  name: Incremental audit fees (crisis-related)
  category: non_recurring_professional_fees
  treatment: ACCEPT            # ACCEPT | REJECT | SENSITIVITY
  direction: add_back
  basis: FILED                 # FILED | DERIVED | ASSUMPTION
  source_doc: SMCI DEF 14A FY2025
  source_ref: "Principal Accountant Fees and Services — Audit Fees"
  method: "FY24/FY25 audit fees less FY23 (pre-crisis) baseline"
  rationale: "..."
  counterargument: "Seller: ..."
  market_practice: standard
  values:
    FY2024: null               # ← populate from filing. null until sourced. Code raises if ACCEPT and null.
    FY2025: null
```

Design consequences that matter:

- The bridge is a **reduce over adjustments filtered by treatment**. Changing an adjustment from
  ACCEPT to SENSITIVITY changes the answer without touching a line of logic.
- `rationale` and `counterargument` are **required fields**. They flow straight into the Excel
  adjustment schedule and into the memo. You cannot define an adjustment without articulating the
  pushback — which is exactly the discipline the interview will test.
- An `ACCEPT` adjustment with a `null` value **raises**. It cannot silently become zero.
- The adjustment schedule renders itself: every row shows value, source, treatment, and
  counterargument. That is your "auditable" claim, made concrete.

### 5.4 Step 3 — Excel (openpyxl)

Tabs: `Cover` · `Assumptions` · `EBITDA Bridge` · `Adjustment Schedule` · `NWC` · `CCC & Diagnostics` · `Source Data`

Two conventions that make it read as professional rather than student:

1. **Follow the finance color convention:** blue font = hard-coded input, black = formula, green =
   link to another sheet. Every `ASSUMPTION` fact renders in a distinct color and appears on the
   `Assumptions` tab. An interviewer who has spent five years in Excel will register this in half a
   second, without you saying anything.
2. **Write live formulas, not values.** Where the bridge sums adjustments, write
   `=SUM(D8:D14)` into the cell — not the computed number. The workbook should be a *working
   model*: click a cell, see it compute, trace it to `Source Data`. This is the difference between
   "I exported a table" and "I built a model." It costs you very little in openpyxl and it is
   worth a disproportionate amount in the interview.

Also: a **tickmark column** on every schedule with the source reference (`"FY25 10-K, Note 5"`).
That is literally what an audit workpaper looks like, and it makes "every number is traceable"
a demonstrable claim rather than an assertion.

### 5.5 Step 4 — The waterfall

`matplotlib`, one chart, GAAP EBITDA → Adjusted EBITDA. Conventions:

- Green = increases, red = decreases, and **the two endpoints are a distinct neutral color** — they
  are levels, not deltas. Getting this wrong is the most common waterfall error.
- Label each bar with its value *and* its adjustment ID (`ADJ-002`), so the chart cross-references
  the adjustment schedule.
- Show the three-tier structure visually: GAAP EBITDA → (management adjustments) → Management
  Adjusted EBITDA → (diligence adjustments) → Diligence Adjusted EBITDA. **A waterfall that shows
  you taking things back *out* of management's number is a far more interesting chart than one that
  only goes up.**
- Consider a second chart: the CCC trend (DIO / DSO / DPO stacked, CCC as a line) across periods.
  Honestly, that chart may tell the story better than the waterfall does.

---

## 6. Investment committee memo — 3-page outline

**Audience:** IC of a hypothetical buyer. **Tone:** conclusions first, evidence second, hedging
never. **Constraint:** if a number appears, it is sourced in a footnote.

### Page 1 — Recommendation and QoE findings

**§1. Recommendation (5 lines, at the very top).** A clear verdict — proceed / proceed with
conditions / decline — with the price and structural implications stated immediately. Do not make
the reader wait. If the recommendation is conditional, name the conditions in the same paragraph.

**§2. Basis of preparation and limitations (short, and unusually important here).** Public
information only; no trial balance, no management access, no cut-off testing. State that this is a
Phase 1 analysis. *Putting your limitations on page 1 rather than in an appendix is what a
credible professional does, and it inoculates you against the entire class of "but you couldn't
really know that" questions.*

**§3. The EBITDA bridge.** The waterfall, plus a table with the three tiers. Then the three
takeaways in prose:
- What management's own non-GAAP presentation adds back, and which of those we reject and why.
- The **negative** adjustment for the cost of a compliant finance function — with the reasoning.
- The adjustments we **refused to book** for lack of support, sized as exposures, each mapped to a
  specific confirmatory procedure.

**§4. Purchase price implications.** Enterprise value at a range of multiples applied to *each*
EBITDA basis (management's, ours, downside). The multiple is a labeled assumption — say so. Present
the *spread* as the finding: "the range between management's number and our downside is $X of
enterprise value, which is what the confirmatory diligence is worth."

### Page 2 — Working capital and cash conversion

**§5. NWC composition and trend.** The schedule, and the NWC-as-%-of-revenue trend.

**§6. The peg.** Your recommended construct (% of LTM revenue, not a trailing dollar average) and
the argument for why the conventional mechanic transfers value to the seller in a
working-capital-hungry growth business. Note the monthly-data limitation.

**§7. Cash conversion — the core finding.** DIO/DSO/DPO/CCC trend. The accruals ratio. And the
central exhibit: **reported profitability against operating cash flow.** Then the conclusion —
Adjusted EBITDA less capex less ΔNWC. Say plainly what it implies: growth here is cash-consuming,
so the acquisition must be underwritten on a revolver and a working capital facility, and the
sensitivity of the deal to a single quarter of inventory build is high.

*This section is the reason the project is interesting. Give it the space.*

### Page 3 — Deal risk, and the central tension

**§8. The governance and controls finding.** The material weaknesses, mapped to COSO components.
Make the entity-level vs. process-level distinction explicitly — it is the difference between "the
accounting department needs more people" and "management's assertions cannot be relied upon."

**§9. The central tension — no restatement, yet reporting risk plainly existed.** This is the
question you will be asked, so answer it head-on rather than describing it. The components of a
real answer:

- **A restatement and a control failure are different tests.** Restatement asks: *were the
  reported numbers materially misstated?* ICFR asks: *was there a reasonable possibility that a
  material misstatement would not be prevented or detected on a timely basis?* **You can answer
  "no" to the first and "yes" to the second without any contradiction.** An adverse ICFR opinion
  alongside an unqualified opinion on the financial statements is not a paradox — it is the system
  working exactly as designed. Most people cannot articulate this. If you can, you will sound like
  you have done the job.
- **But it does not mean nothing.** "No material misstatement was *found*" is not "no material
  misstatement *exists*." The absence of a restatement tells you the errors found did not cross a
  materiality threshold; it does not tell you the controls would have caught one that did.
- **What follows for a buyer** — and this is where you convert an accounting observation into a
  deal recommendation:
  - **Diligence:** expand scope. Full cut-off testing, inventory aging, related-party pricing
    benchmarking. Do not rely on management representations for anything material — that is
    precisely the control that was found deficient.
  - **Price:** you do not take a "governance discount" as a made-up haircut. You take it through
    the (a) rejected add-backs, (b) the pro forma cost of a compliant finance function, and
    (c) a multiple that reflects the risk. Being explicit that you do *not* invent a discount
    percentage is itself a mark of discipline.
  - **Structure:** this is where the risk actually goes. Indemnity escrow sized to the exposures,
    a specific indemnity for the regulatory matters and securities litigation, R&W insurance
    (with the near-certainty that the insurer excludes the known accounting and regulatory
    matters — *known* risks are not insurable, and saying so shows you understand what R&W
    insurance is actually for), and closing conditions tied to remediation milestones.
  - **Post-close:** the finance function is a Day-1 integration priority with a real budget,
    which is the same number you put in the bridge as a negative adjustment. **Make sure those
    two numbers are the same number.** Internal consistency between your EBITDA bridge and your
    integration plan is the kind of thing a Director notices.

**§10. Confirmatory diligence request list.** The specific documents and procedures, prioritized,
each mapped to the adjustment or exposure it resolves and the dollar amount at stake.

---

## 7. Sequencing

1. **You:** pull the documents in §1. Read Item 9A, the auditor's report and CAMs, and the
   related-party note first — those three shape everything downstream.
2. **You:** hand-enter `facts.csv` with source references. Slow, unglamorous, and it is what makes
   you able to answer follow-up questions.
3. **Me:** `finlib` core — facts, validation, diagnostics.
4. **Me:** the bridge and NWC engines.
5. **Me:** Excel and charts.
6. **You + me:** the memo, written from the model's actual output.

Do not skip step 1. The value of this project to you is not the code — it is that you will have
read a real 10-K in anger and can talk about what you found. The code is what makes it defensible;
the reading is what makes it yours.

---

## 8. Decisions locked (2026-07-29)

1. **Scope: LTM in.** Historical FY2023 / FY2024 / FY2025, plus LTM through the most recent filed
   FY2026 10-Q. FY23 is the pre-crisis baseline; LTM is what we underwrite.
2. **Deal type: take-private of the whole company.** No carve-out; no stand-alone-cost analysis.
3. **Beneish M-score: built here.** The engine lives in `finlib/diagnostics.py` and is shared with
   project 2 (the anomaly screener). How prominently the M-score features in each deliverable is a
   later call; the code is written once, here.

## 9. Open questions for you (superseded — see §8)

1. Do you want the LTM/FY2026 data in scope (recommended), or are you deliberately freezing the
   analysis at the February 2025 filings as a point-in-time exercise? Either is defensible — the
   point-in-time framing ("diligence as of the reopening of the filings") is actually a clean
   story, but you must *choose* it rather than back into it.
2. Take-private (whole company) or a carve-out? I have assumed whole-company. A carve-out would
   substantially change the NWC and stand-alone-cost analysis.
3. Do you want the Beneish M-score built here (feeding project 2), or held back entirely for the
   screener?
