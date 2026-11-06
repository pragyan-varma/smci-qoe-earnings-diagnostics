# Roadmap

Ordered by dependency rather than appeal: work that makes later changes safe or
measurable comes first. Each item links to its backlog issue. None of these items has
been built yet. This is planned work.

## Now

- **Validation controls don't stop a bad build** ([#1](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/1)) — the
  deliverables script never runs the tie-outs, and `main.py` reports a failure but still
  exits successfully. A correctness bug in the model's main safeguard, so it goes first.
- **Period ordering hard-codes SMCI's fiscal years** ([#2](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/2)) — the
  shared fact layer mis-orders any year outside FY2023–FY2025. Small bug, and both the
  quarterly peg work (#6) and reuse on another company (#7) build on this ordering.
- **Regression tests, CI, and pinned dependencies** ([#3](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/3)) — every
  item below changes how figures are calculated. Tests that pin the headline numbers come
  first so those changes can't silently move them.
- **Memo figures that don't match the model** ([#9](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/9)) — two
  figures in the IC memo differ from what the code computes (a mislabelled cash-flow
  measure, and $7M vs $6.5M for the related-party sensitivity). The memo is the document
  a committee would actually read, so it goes in Now. Numbered last because it was found
  in a later review pass.

## Next

- **One source of truth for adjustment values** ([#4](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/4)) — two
  adjustments are defined in more than one place, and the finance-function range never
  reaches the bridge. Depends on #3 so the refactor can be shown not to change the
  numbers.
- **Size every unbooked exposure** ([#5](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/5)) — only related-party
  pricing is sized in the model today. The other unbooked issues are described in prose
  only. Depends on #4, because new exposure lines should go into the consolidated
  adjustment definitions rather than add another copy.
- **Quarterly NWC peg schedule** ([#6](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/6)) — the IC memo argues for
  a revenue-linked peg, and the quarterly data to show it is already committed but unused.
  Depends on #2 (ordering quarters correctly) and #3.

## Later

- **Run the diagnostics on a second issuer** ([#7](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/7)) — turns
  "built for reuse" into "reused". Largest change, and it depends on #2, #3, and #4. It
  also needs a new SEC data pull, which is a separately authorized step.
- **Quantify SBC and convertible dilution** ([#8](https://github.com/pragyan-varma/smci-qoe-earnings-diagnostics/issues/8)) — strengthens
  the SBC-as-cost argument. It needs share and convertible data hand-read from the filings
  first. Depends on #4.

## Assumptions

These shape the ordering above and none have been validated.

- **The users are assumed, not researched.** The personas in the README's Scope section
  and in the backlog stories (an investment committee member deciding whether to proceed
  past LOI, and an analyst who would review or reuse the model) describe who the project
  was designed for. Nobody has been interviewed, and nobody outside the project has
  reviewed the work.
- **Trust in the numbers matters more than new analysis.** This is why the control and
  test work (#1–#3) comes before new outputs. If a reader cares more about coverage than
  about reproducibility, #5 and #6 would move up.
- **A committee member reads the workbook, not just the memo.** #5 and #6 add workbook
  tabs. If the memo is the only thing read, the same content belongs in the memo instead.
- **Reuse on a second company is wanted.** #7 is the largest item. If nobody needs to run
  this on another issuer, it drops off the list, and #2 matters only as a correctness fix.

The next step for testing these is to give the memo and workbook to a few people in the
assumed roles, note which sections they use and which questions they still have, and
re-rank this list based on that.
