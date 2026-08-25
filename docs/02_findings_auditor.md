# Findings — Auditor, Controls, and the Central Tension (VERIFIED)

Sources: FY2024 10-K, FY2023 10-K, 8-K filed 2024-10-30 (Item 4.01, Ex. 16.1). Facts extracted
from filing text; interpretation flagged as such.

## 1. Auditor timeline (corrected — EY signed nothing)

| Period | Auditor | Note |
|---|---|---|
| Since 2003; through FY2023 | **Deloitte & Touche** (PCAOB 34) | Signed original FY2023 10-K; in FY2024 10-K, opines on FY2023/FY2022 comparatives |
| FY2024, engaged 3/15/2023 | **Ernst & Young** | Resigned 10/30/2024 **mid-engagement, never issued any report** on financials or ICFR |
| FY2024 completed; since 2024 | **BDO USA, P.C.** (PCAOB 243) | Clean opinion on FY2024 financials; **adverse** opinion on ICFR. Of the comparatives, BDO audited **only the retrospective stock-split adjustment**, not FY23/22 as a whole |

"Ernst & Young" appears 0 times in the FY2024 and FY2023 10-Ks. Never say "EY's opinions" — none exist.

## 2. Why EY resigned (8-K Item 4.01, Ex. 16.1)

- **No "disagreement"** under Reg S-K Item 304(a)(1)(iv) and **no "reportable event"** under (a)(1)(v),
  per the 8-K. So NOT a GAAP/accounting-treatment dispute.
- EY's stated basis: it could **no longer rely on management's and the Audit Committee's
  representations**, was **unwilling to be associated** with management-prepared financials, and
  could no longer provide audit services consistent with law/professional obligations.
- Trigger chain: late-July 2024 EY raised governance/transparency/completeness-of-communication and
  ICFR concerns to the Audit Committee → Board formed Special Committee (Cooley LLP + forensic
  accountants Secretariat Advisors) → after the review, EY questioned the Company's commitment to
  **integrity and ethical values (COSO Principle 1)** and whether the Board/Audit Committee could act
  **independently of the CEO (COSO Principle 2)**.
- Company response: disagreed with the resignation, called the Review incomplete, said it did **not
  expect restatements** of FY2024 quarters or prior years.

**Framing:** EY's objection was to the **control environment / governance — the top of the COSO
pyramid — not to any number.** An auditor that cannot trust management representations cannot audit
anything; the resignation was structurally unavoidable once EY reached that conclusion.

## 3. The two opinions (both verified verbatim, dated 2/25/2025)

- **Financial statements: UNQUALIFIED** — "present fairly, in all material respects... in conformity
  with [US GAAP]."
- **ICFR: ADVERSE** — "did not maintain, in all material respects, effective internal control over
  financial reporting as of June 30, 2024."
- Management also concluded **disclosure controls were not effective**, and that **as of the filing
  date none of the five material weaknesses had been remediated.**

**This IS the resolution of the central tension.** Restatement test (are the numbers materially
misstated?) → passed. ICFR test (was there a reasonable possibility a material misstatement would not
be prevented/detected?) → failed. Two different questions; both answers true at once. Not a paradox.

## 4. RESOLVED — the "retrospective adjustments" are the stock split (benign)

Earlier flagged as a possible hidden revision. **It is not.** The FY2023/FY2022 retrospective
adjustments are the **10-for-1 stock split** (effective Oct 2024) applied retroactively to
share/EPS figures. BDO audited only that adjustment to the prior years. **This is NOT a red flag** —
do not present it as one. Intellectual honesty: we chased it, and it's a stock split.

## 5. The five material weaknesses → COSO mapping (our analytical contribution)

The 10-K lists them but does **not** map them. The mapping is the value-add:

| # | Material weakness (disclosed) | COSO component | Principle |
|---|---|---|---|
| i | ITGCs for financial-reporting IT systems not properly identified/designed/implemented | Control Activities | P11 (tech general controls) |
| ii | Segregation-of-duties conflict controls not properly designed/implemented | Control Activities (2°: Control Environment) | P10; P3 |
| iii | Manual journal-entry review/approval controls not designed to prevent unauthorized posting | Control Activities (2°: Risk Assessment) | P10; P8 (fraud/override) |
| iv | Completeness/accuracy of information produced by the entity (IPE) not documented | Information & Communication | P13 |
| v | No documented controls for timely/complete/accurate recording & disclosure — incl. **new leases and new related party transactions** | Control Activities + Info & Comm (2°: Monitoring) | P12; P13; P16/17 |

**The killer point:** all five sit in **Control Activities** or **Information & Communication** —
process-level. **None is disclosed as a Control Environment failure** — yet Control Environment
(Principles 1–2: integrity and independent board oversight) is *exactly* what EY resigned over. **The
10-K's disclosure and EY's stated reasons do not line up.** Item (v)'s explicit callout of **related
party transactions** is the closest bridge between the disclosed (process) weaknesses and the
undisclosed (entity-level) governance concern — and given the RP exposure we quantified (§ related
party) and the short-seller allegations, that placement is not a coincidence.

Management's own language concedes the weaknesses could have increased risk of unauthorized system
access, **data manipulation**, and incomplete/inaccurate information — fraud-adjacent exposure,
described in the same filing that asserts the financials are fairly stated.

## 6. The two CAMs → they validate our QoE scope exactly

1. **Valuation of inventories** ($4.33B at 6/30/2024, LCM/NRV). Judgment: **E&O write-down
   percentages** by category. BDO procedures: product-lifecycle inquiry; recomputing inventory turns
   and historical write-down % across periods; testing aging-classification data; seeking
   contradictory evidence in press/industry reports.
   → Ties directly to our findings: **74% finished goods**, **no E&O reserve disclosed**. The auditor
   with the trial balance flagged the same account we did from the outside.
2. **Revenue recognition** ($14.99B FY2024, control transfers at shipment/delivery). Flagged for
   **audit effort**, not estimation. Procedures: source-document sample testing (PO, contract,
   invoice, proof of shipment/delivery, subsequent cash); **credit-memo-to-invoice period testing (a
   cutoff test)**; IPE completeness/accuracy; direct confirmation of contract terms.
   → Ties to the channel-stuffing / revenue-timing concern and to material weakness (iv) on IPE. The
   revenue **cutoff test** is precisely the confirmatory procedure we scoped and cannot run on public
   data.

**Framing:** a broken control environment forces the auditor to expand substantive testing — BDO
explicitly considered the weaknesses in setting the nature, timing, and extent of its tests. The
CAMs are the auditor telling us, in writing, that inventory valuation and revenue cutoff are the two
riskiest accounts. That is exactly our QoE scope, independently corroborated.

## 7. Both-sides discipline (for the interview)

For each sharp claim, hold the seller's rebuttal:

- **"COSO mismatch proves a cover-up."** Seller: management maps weaknesses to the specific failed
  *controls*; entity-level tone is a matter of judgment EY and management genuinely disagreed on, and
  the Special Committee's remediation addresses governance separately. → Your line: I'm not alleging
  concealment; I'm noting the disclosed weaknesses are necessary but arguably **not sufficient** to
  cover what EY described, and that gap is a diligence question, not an accusation.
- **"Adverse ICFR = the numbers are wrong."** Wrong — clean FS opinion. Adverse ICFR raises the
  *probability* of undetected error; it does not assert one occurred.
- **"None remediated = uninvestable."** Seller: remediation is underway with a defined plan; a buyer
  prices and structures around it (escrow, milestones, Day-1 finance build). → This is where the
  **negative EBITDA adjustment** for a compliant finance function comes from.
