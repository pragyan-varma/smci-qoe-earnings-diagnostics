"""
SMCI QoE — run the validation controls and print the diagnostics summary.

    python3 main.py

Everything printed is DERIVED from FILED facts in data/source/. If a required fact is missing,
this RAISES rather than guessing.
"""
from finlib.facts import load_facts
from qoe import validate, metrics, bridge, mscore
from qoe import labels as L

PERIODS = ("FY2023", "FY2024", "FY2025")


def money(x):
    return f"${x/1e9:,.2f}B" if abs(x) >= 1e9 else f"${x/1e6:,.1f}M"


def main():
    fs = load_facts()
    print(f"Loaded {len(fs)} sourced facts. Periods: {', '.join(fs.periods())}\n")

    # 1) Controls -----------------------------------------------------------
    print("=" * 78)
    print("VALIDATION CONTROLS (tie-outs)")
    print("=" * 78)
    checks = validate.run_all(fs, PERIODS, tolerate=True)
    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name:44s} {detail}")

    # 2) Cash conversion & earnings quality --------------------------------
    print("\n" + "=" * 78)
    print("WORKING CAPITAL / CASH CONVERSION  (avg balances where prior period exists)")
    print("=" * 78)
    print(f"  {'':10s}{'DIO':>8}{'DSO':>8}{'DPO':>8}{'CCC':>8}"
          f"{'NWC':>12}{'NWC/Rev':>9}{'Accruals':>10}")
    for m in metrics.compute(fs, PERIODS):
        acc = f"{m.accruals_ratio*100:>8.1f}%" if m.accruals_ratio is not None else "     n/a"
        print(f"  {m.period:10s}{m.dio:>8.0f}{m.dso:>8.0f}{m.dpo:>8.0f}{m.ccc:>8.0f}"
              f"{money(m.nwc):>12}{m.nwc_pct_revenue*100:>8.1f}%{acc:>10}")

    # 3) Profit vs cash — the punchline ------------------------------------
    print("\n" + "=" * 78)
    print("REPORTED PROFIT vs CASH  (the core finding)")
    print("=" * 78)
    for p in PERIODS:
        ni, cf = L.net_income(fs, p), L.cfo(fs, p)
        print(f"  {p}:  Net income {money(ni):>10}   Operating cash flow {money(cf):>11}   "
              f"gap {money(ni - cf):>10}")

    # 4) Capital structure --------------------------------------------------
    print("\n" + "=" * 78)
    print("CAPITAL STRUCTURE (cash-free/debt-free inputs)")
    print("=" * 78)
    for p in ("FY2024", "FY2025"):
        print(f"  {p}:  Total debt {money(L.total_debt(fs, p)):>10}   "
              f"Cash {money(L.cash(fs, p)):>10}   Net debt {money(L.net_debt(fs, p)):>11}")

    # 5) Related-party exposure --------------------------------------------
    print("\n" + "=" * 78)
    print("RELATED-PARTY PURCHASE EXPOSURE")
    print("=" * 78)
    for r in metrics.related_party_exposure(fs, PERIODS):
        print(f"  {r['period']}:  RP COGS {money(r['rp_cogs']):>9} = {r['pct_of_cogs']*100:>4.2f}% of COGS   "
              f"| 100bps pricing swing = {money(r['ebitda_per_100bps'])} EBITDA")

    # 6) EBITDA bridge ------------------------------------------------------
    print("\n" + "=" * 78)
    print("EBITDA BRIDGE — three-tier walk")
    print("=" * 78)
    adjs = bridge.load_adjustments()
    for p in ("FY2025",):
        br = bridge.build_bridge(fs, p, adjs)
        print(f"\n  [{p}]  GAAP EBITDA (Operating income + D&A) = {money(br.gaap_ebitda)}")
        for l in br.lines:
            val = money(l.value) if l.value is not None else "  n/q  "
            mark = "booked " if l.booked else "shown  "
            print(f"    {l.id}  {mark} {l.name[:46]:46s} {val:>10}   [{l.treatment}]")
            if l.note:
                print(f"           └ {l.note}")
        print(f"\n    => Management-basis EBITDA (SBC added back)          = {money(br.management_ebitda)}")
        print(f"    => Diligence Adjusted EBITDA — SBC added back        = {money(br.diligence_ebitda_pre_sbc)}")
        print(f"    => Diligence Adjusted EBITDA — SBC as real cost      = {money(br.diligence_ebitda_post_sbc)}")
        sbc_swing = br.diligence_ebitda_pre_sbc - br.diligence_ebitda_post_sbc
        print(f"       SBC decision is worth {money(sbc_swing)} of EBITDA; at 15x that is "
              f"{money(sbc_swing*15)} of enterprise value.")
        print("       (SENSITIVITY / REJECT items above are shown as exposures, not booked)")

    # 7) Beneish M-score ----------------------------------------------------
    print("\n" + "=" * 78)
    print("BENEISH M-SCORE  (screen, not verdict — read the components)")
    print("=" * 78)
    print(f"  {'':8}{'DSRI':>7}{'GMI':>7}{'AQI':>7}{'SGI':>7}{'DEPI':>7}"
          f"{'SGAI':>7}{'TATA':>7}{'LVGI':>7}{'M':>9}  flag")
    for ms in mscore.compute_all(fs):
        print(f"  {ms.period:8}{ms.DSRI:>7.2f}{ms.GMI:>7.2f}{ms.AQI:>7.2f}{ms.SGI:>7.2f}"
              f"{ms.DEPI:>7.2f}{ms.SGAI:>7.2f}{ms.TATA:>7.2f}{ms.LVGI:>7.2f}"
              f"{ms.m_score:>9.2f}  {'FLAG' if ms.flagged else 'ok'}")
    print(f"  threshold {mscore.dx.M_SCORE_THRESHOLD}: above => elevated manipulation likelihood")


if __name__ == "__main__":
    main()
