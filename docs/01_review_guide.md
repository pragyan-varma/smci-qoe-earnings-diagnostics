# SMCI QoE — Review Guide (what YOU check, and where)

I pulled the structured numbers from SEC's XBRL API into `data/source/facts.csv`, each row
stamped with the filing accession and a direct URL (`data/source/filings.csv`). This guide tells
you (A) how to spot-check that I pulled them correctly, and (B) the narrative sections only you
can read — the part that actually wins the interview.

**Fiscal years end June 30. All values below are in whole USD as SEC tagged them.**

---

## Part A — Spot-check the numbers (15 minutes)

Don't re-verify all 247. Open the **FY2025 10-K** and confirm five values against the income
statement and balance sheet. If these five tie, trust the pull; if any is off, tell me and I'll
investigate the tag.

**FY2025 10-K:** https://www.sec.gov/Archives/edgar/data/1375365/000137536525000027/smci-20250630.htm

| Check | Where in the 10-K | Value I pulled (FY2025) |
|---|---|---|
| Revenue | Consolidated Statements of Operations, top line | $21,972,042,000 |
| Net income | Same statement, bottom line | $1,048,854,000 |
| Inventories, net | Consolidated Balance Sheets, current assets | $4,680,375,000 |
| Operating cash flow | Statement of Cash Flows, subtotal of operating section | $1,659,524,000 |
| Total assets = Total liab. & equity | Balance Sheet (both should equal) | $14,018,429,000 |

The FY2025 10-K shows FY2024 and FY2023 as comparatives, so you can eyeball those columns too.

---

## Part B — The five concepts SEC did NOT tag (read these notes by hand)

These came back `NOT_TAGGED` because SMCI reports them under a label the standard tag didn't catch.
That's normal — and each gap is a note you needed to read anyway. Find the value and I'll add it
to `facts.csv` as a FILED fact with the note reference.

1. **SG&A** — SMCI likely splits operating expense into **"Sales and marketing"** and **"General
   and administrative"** as two lines (not one "SG&A"). Grab both, all three years, from the income
   statement. *G&A is the line that carries the crisis costs — you need it.*
2. **Inventory — gross, and the reserve.** The balance sheet shows inventory *net*. The
   **Inventories note (Balance Sheet Components)** may show the write-down/reserve. If it shows only
   a net number with no reserve disclosed, **that itself is a finding** — write it down as a
   disclosure gap.
3. **Short-term investments** — check whether SMCI holds any, or parks everything in cash. Balance
   sheet, current assets.
4. **Cost of revenue** — I *did* capture this (under the alt tag `CostOfRevenue`): FY23 $5.84B /
   FY24 $12.93B / FY25 $19.54B. Just confirm the FY25 figure on the income statement.

---

## Part C — The narrative sections (this is the interview, not the numbers)

Read these in order. For each, I've said exactly what to extract.

### C1. The EY resignation — the single most important document
**8-K filed 2024-10-30 (likely Item 4.01):**
https://www.sec.gov/Archives/edgar/data/1375365/000137536524000036/smci-20241024.htm

- Confirm this is the auditor-resignation 8-K (Item 4.01 — Changes in Registrant's Certifying Accountant).
- Find the **EY letter filed as an exhibit** (usually Exhibit 16.1). Read its *exact* words.
- Extract: Does EY cite **disagreements**? Does it cite **"reportable events"** under Reg S-K Item
  304(a)(1)(v)? Does it say it is **unwilling to be associated** with management's financial
  statements or with the board's representations? Quote the operative sentence verbatim in your notes.
- *Why:* the strength of your whole governance thesis rests on whether EY quit over a **disagreement**
  (mild) or over an **inability to rely on management** (severe). Get the exact language.

### C2. The crisis timeline (skim, log dates)
8-Ks in the window, newest first:
- 2024-08-28 — https://www.sec.gov/Archives/edgar/data/1375365/000137536524000030/smci-20240828.htm
- 2024-09-03 — https://www.sec.gov/Archives/edgar/data/1375365/000137536524000032/smci-20240903.htm  *(likely NT 10-K / delay context)*
- 2024-12-02 — https://www.sec.gov/Archives/edgar/data/1375365/000137536524000044/smci-20241127.htm  *(likely Special Committee conclusion — read Ex-99.1)*
- 2025-02-11 — https://www.sec.gov/Archives/edgar/data/1375365/000137536525000001/smci-20250211.htm
- 2025-02-21 — https://www.sec.gov/Archives/edgar/data/1375365/000137536525000003/smci-20250220.htm  *(likely regained-compliance / filing announcement)*

**NT 10-K (late-filing notice), filed 2024-08-30:**
https://www.sec.gov/Archives/edgar/data/1375365/000137536524000031/smci-form12bx25nt10xkx2024.htm
- Extract management's *stated reason* for the delay. You'll compare it against what the 10-K
  ultimately said.

For the **Special Committee 8-K** (the ~Dec 2 filing), read the press-release exhibit and extract:
Did they find misconduct? How many remedial actions were recommended? Were they *implemented* by the
time the FY24 10-K was filed?

### C3. FY2024 10-K — Item 9A and the auditor's report (the technical heart)
**FY2024 10-K (the delayed one):**
https://www.sec.gov/Archives/edgar/data/1375365/000137536525000004/smci-20240630.htm

- **Item 9A — Controls and Procedures.** Extract:
  - Management's conclusion on disclosure controls: effective or **not** effective?
  - Management's conclusion on ICFR: effective or **not** effective?
  - The **enumerated material weaknesses** — copy the exact list. For each, decide which **COSO
    component** it maps to: Control Environment / Risk Assessment / Control Activities / Information
    & Communication / Monitoring. *Control Environment weaknesses are entity-level and severe;
    Control Activities weaknesses are process-level and more contained. This distinction is your
    best technical talking point.*
  - The remediation plan and its stated timeline/cost.
- **The auditor's report(s):**
  - Who signed the opinion? (Confirm the successor auditor — verify the name; do not assume.)
  - Is there a **separate opinion on ICFR**, and is it **adverse**? (Expect: unqualified on the
    financials, adverse on ICFR. Confirm.)
  - **Critical Audit Matters (CAMs)** — list them. Whatever accounts they name are your QoE scope.
  - **Who audited FY2023/FY2022 comparatives?** If a predecessor (EY) report is still carried, note
    whether any prior opinion was withdrawn or investors were told not to rely on it. *This is the
    "no restatement yet reporting risk existed" tension — get the facts exact.*

### C4. Related-party transactions note (the highest-value finding)
In the **FY2024 and FY2025 10-Ks**, find the **Related Party Transactions note**.
- Confirm the counterparties (industry reporting names Ablecom and Compuware as CEO-family-affiliated
  — **verify against the note itself**, don't take my word or the press's).
- Extract, for every year: purchases from / sales to each related party, and any receivable/payable
  balances. Note whether the filing asserts the pricing is **at market / arm's-length**.
- *Why:* if a related party supplies below market, reported COGS is understated and EBITDA is
  subsidized by the founder's family — a subsidy the buyer may not inherit.

### C5. Revenue recognition note
In the FY2025 10-K:
- Point-in-time vs. over-time; when control transfers.
- Any **bill-and-hold** language (strict 5-criteria test under ASC 606 — a classic aggressive-recognition vehicle).
- Distributor / channel arrangements; contract balances (deferred revenue roll-forward).

### C6. DEF 14A proxy — the one hard number for "crisis costs"
Audit fees by year and by firm live in the **"Principal Accountant Fees and Services"** table.
- **FY2025 proxy (2025-04-24):** https://www.sec.gov/Archives/edgar/data/1375365/000137536525000009/smci-20250424.htm
- **FY2026 proxy (2026-03-03):** https://www.sec.gov/Archives/edgar/data/1375365/000137536526000008/smci-20260303.htm
- **FY2022 proxy (pre-crisis baseline, 2023-04-14):** https://www.sec.gov/Archives/edgar/data/1375365/000137536523000024/proxystatement2022.htm

Extract Audit Fees / Audit-Related / Tax / All Other, per year, per firm. The pre-crisis-vs-crisis
delta is your only *hard, sourced* quantification of the accounting-crisis cost — present it as a
**floor**, not the total.

### C7. The prior SEC matter (establish pattern vs. first offense)
Search SEC's own site for the **2020 SMCI enforcement action** (AAER / litigation release re:
prematurely recognized revenue). Cite SEC's release, not a news article. You need to know whether
2024 is a repeat.

---

## Part D — What I do next (once you've done Part B)

1. You send me the ~8 hand-read values from Part B (the SG&A split, gross inventory & reserve, audit
   fees). I add them to `facts.csv` with their note references.
2. I build `finlib` (facts loader + validation controls + diagnostics/CCC/M-score) on the confirmed data.
3. We build the bridge, NWC schedule, Excel, and waterfall.

**You do not need to transcribe the financial statements — that's done.** Your job is Part B: the
words, the material weaknesses, the auditor's opinion, and the related-party note. That's the part a
CPA will actually test you on.
