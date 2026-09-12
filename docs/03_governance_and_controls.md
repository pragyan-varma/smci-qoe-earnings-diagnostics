# Auditor, Internal Controls, and the Restatement Question

Sources: FY2024 10-K, FY2023 10-K, 8-K filed 2024-10-30 (Item 4.01, Ex. 16.1). Facts extracted
from filing text; interpretation flagged as such.

## 1. Auditor timeline

| Period | Auditor | Note |
|---|---|---|
| Since 2003; through FY2023 | **Deloitte & Touche** (PCAOB 34) | Signed original FY2023 10-K; in FY2024 10-K, opines on FY2023/FY2022 comparatives |
| FY2024, engaged 3/15/2023 | **Ernst & Young** | Resigned 10/30/2024 **mid-engagement, never issued any report** on financials or ICFR |
| FY2024 completed; since 2024 | **BDO USA, P.C.** (PCAOB 243) | Clean opinion on FY2024 financials; **adverse** opinion on ICFR. Of the comparatives, BDO audited **only the retrospective stock-split adjustment**, not FY23/22 as a whole |

"Ernst & Young" appears nowhere in either the FY2024 or FY2023 10-K. No EY audit opinion on SMCI's
financial statements exists, which is a distinction worth preserving: the resignation was an event,
not the withdrawal of a prior opinion.

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

## 3. The two opinions (dated 2025-02-25)

- **Financial statements: UNQUALIFIED** — "present fairly, in all material respects... in conformity
  with [US GAAP]."
- **ICFR: ADVERSE** — "did not maintain, in all material respects, effective internal control over
  financial reporting as of June 30, 2024."
- Management also concluded **disclosure controls were not effective**, and that **as of the filing
  date none of the five material weaknesses had been remediated.**

**This IS the resolution of the central tension.** Restatement test (are the numbers materially
misstated?) → passed. ICFR test (was there a reasonable possibility a material misstatement would not
be prevented/detected?) → failed. Two different questions; both answers true at once. Not a paradox.

## 4. The retrospective adjustments to FY2023/FY2022

Deloitte's re-issued report on the comparative periods refers to "retrospective adjustments
discussed in Note 1," which on its face could indicate a revision to previously reported figures.
It does not. The adjustments are the **10-for-1 stock split** (effective October 2024) applied
retroactively to share and per-share figures, and BDO audited only that adjustment to the prior
years. This is not an accounting red flag and is not presented as one.

## 5. The five material weaknesses mapped to COSO

The 10-K lists them but does **not** map them. The mapping is the value-add:

| # | Material weakness (disclosed) | COSO component | Principle |
|---|---|---|---|
| i | ITGCs for financial-reporting IT systems not properly identified/designed/implemented | Control Activities | P11 (tech general controls) |
| ii | Segregation-of-duties conflict controls not properly designed/implemented | Control Activities (2°: Control Environment) | P10; P3 |
| iii | Manual journal-entry review/approval controls not designed to prevent unauthorized posting | Control Activities (2°: Risk Assessment) | P10; P8 (fraud/override) |
| iv | Completeness/accuracy of information produced by the entity (IPE) not documented | Information & Communication | P13 |
| v | No documented controls for timely/complete/accurate recording & disclosure — incl. **new leases and new related party transactions** | Control Activities + Info & Comm (2°: Monitoring) | P12; P13; P16/17 |

**The principal observation:** all five sit in **Control Activities** or **Information &
Communication** — process-level. **None is disclosed as a Control Environment failure** — yet
Control Environment (Principles 1–2: integrity and independent board oversight) is precisely what
EY resigned over. The disclosed weaknesses and the stated reasons for the auditor's resignation do
not align. Item (v)'s explicit reference to **related party transactions** is the closest bridge
between the disclosed process-level weaknesses and the entity-level governance concern, which is
notable given the related-party exposure quantified elsewhere in this analysis.

The conclusion drawn is one of **sufficiency, not concealment**: the five disclosed weaknesses are
necessary but arguably not sufficient to describe the condition the predecessor auditor identified.
Remediating all five would not, on its face, resolve an entity-level governance concern. That is a
diligence question rather than an allegation.

Management's own language concedes the weaknesses could have increased risk of unauthorized system
access, **data manipulation**, and incomplete/inaccurate information — fraud-adjacent exposure,
described in the same filing that asserts the financials are fairly stated.

## 6. Critical Audit Matters

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

Deficient controls force an auditor to expand substantive testing, and BDO states explicitly that
it considered the material weaknesses in determining the nature, timing, and extent of its
procedures. The two CAMs identify inventory valuation and revenue recognition as the accounts
requiring the most audit judgment and effort — the same two accounts this analysis independently
identified as the highest-risk areas from public data alone.

## 7. Counterarguments considered

Each observation above was tested against the position a seller would take:

- **On the COSO mismatch.** A seller would argue that management maps weaknesses to the specific
  controls that failed, that entity-level tone was a matter of genuine judgment on which the
  predecessor auditor and management disagreed, and that the Special Committee's remediation
  addresses governance separately. The position taken here is deliberately narrower than
  concealment — the disclosed weaknesses are necessary but arguably not sufficient, which is a
  scoping question for confirmatory diligence.
- **On the adverse ICFR opinion.** It does not follow that the reported figures are wrong; the
  financial-statement opinion is unqualified. An adverse ICFR opinion raises the *probability* of
  an undetected material misstatement without asserting that one occurred.
- **On unremediated weaknesses.** A seller would note that remediation is underway against a
  defined plan. The buy-side response is not to decline the asset but to price and structure around
  it — escrow, remediation-linked closing conditions, and a funded Day-1 finance build, the last of
  which is the basis for the negative EBITDA adjustment described in the methodology.
