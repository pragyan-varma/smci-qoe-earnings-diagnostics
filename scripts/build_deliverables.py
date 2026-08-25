"""Generate the QoE deliverables into outputs/. Run: ./.venv/bin/python scripts/build_deliverables.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finlib.facts import load_facts
from qoe import excel, charts

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
PERIODS = ("FY2023", "FY2024", "FY2025")


def main():
    fs = load_facts()
    xlsx = excel.build_workbook(fs, os.path.join(OUT, "SMCI_QoE_model.xlsx"))
    wf = charts.waterfall(fs, "FY2025", os.path.join(OUT, "ebitda_waterfall_FY2025.png"))
    cc = charts.ccc_trend(fs, PERIODS, os.path.join(OUT, "ccc_trend.png"))
    print("Wrote:")
    for p in (xlsx, wf, cc):
        print(f"  {p}  ({os.path.getsize(p):,} bytes)")


if __name__ == "__main__":
    main()
