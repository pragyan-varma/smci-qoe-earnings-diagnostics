"""
SMCI QoE — EDGAR ingestion (Phase 1).

Pulls SMCI's structured financial facts from SEC's XBRL companyfacts API in ONE request,
plus the filing index from the submissions API, and writes:

  data/source/facts.csv        one row per (concept, period), each stamped with the
                               filing accession number and a direct EDGAR URL
  data/source/filings.csv      the filing index (10-K / 10-Q / 8-K / DEF 14A) with URLs

No values are invented. Every row is a value SEC returned, tagged to the filing it came from.
Concepts SEC did not tag for SMCI are written with value=NOT_TAGGED so you know to read the
note by hand rather than assuming zero.
"""
import json, csv, os, urllib.request, time

CIK = "0001375365"
CIK_INT = "1375365"
UA = {"User-Agent": "SMCI QoE Research pragyanv07@gmail.com"}
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "data", "source")
os.makedirs(SRC, exist_ok=True)

# Fiscal years we care about (FYE June 30). Add more here to widen scope.
TARGET_FYE = {"2023-06-30", "2024-06-30", "2025-06-30"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


# Curated concept map: statement -> {us-gaap concept: friendly line item}.
# These are the standard tags. If a company uses a different tag, the concept comes back
# NOT_TAGGED and you go read the note — that gap is itself a finding, not an error.
CONCEPTS = {
    "IS": {
        "RevenueFromContractWithCustomerExcludingAssessedTax": "Revenue",
        "CostOfGoodsAndServicesSold": "Cost of revenue",
        "CostOfRevenue": "Cost of revenue (alt tag)",
        "GrossProfit": "Gross profit",
        "ResearchAndDevelopmentExpense": "R&D expense",
        "SellingGeneralAndAdministrativeExpense": "SG&A expense",
        "OperatingIncomeLoss": "Operating income",
        "InterestExpense": "Interest expense",
        "InterestExpenseNonoperating": "Interest expense (nonoperating)",
        "InvestmentIncomeInterest": "Interest income",
        "OtherNonoperatingIncomeExpense": "Other non-operating income/expense",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments": "Pre-tax income",
        "IncomeTaxExpenseBenefit": "Income tax expense",
        "NetIncomeLoss": "Net income",
    },
    "BS": {
        "CashAndCashEquivalentsAtCarryingValue": "Cash & equivalents",
        "ShortTermInvestments": "Short-term investments",
        "AccountsReceivableNetCurrent": "Accounts receivable, net",
        "InventoryNet": "Inventories, net",
        "InventoryGross": "Inventories, gross",
        "InventoryValuationReserves": "Inventory reserve (E&O)",
        "PrepaidExpenseAndOtherAssetsCurrent": "Prepaid & other current assets",
        "AssetsCurrent": "Total current assets",
        "Assets": "Total assets",
        "AccountsPayableCurrent": "Accounts payable",
        "AccruedLiabilitiesCurrent": "Accrued liabilities",
        "ContractWithCustomerLiabilityCurrent": "Deferred revenue, current",
        "LiabilitiesCurrent": "Total current liabilities",
        "Liabilities": "Total liabilities",
        "LongTermDebtNoncurrent": "Long-term debt, noncurrent",
        "StockholdersEquity": "Total stockholders' equity",
        "LiabilitiesAndStockholdersEquity": "Total liabilities & equity",
    },
    "CF": {
        "NetCashProvidedByUsedInOperatingActivities": "Operating cash flow",
        "DepreciationDepletionAndAmortization": "D&A (cash flow)",
        "DepreciationAmortizationAndAccretionNet": "D&A + accretion (cash flow, alt)",
        "ShareBasedCompensation": "Stock-based compensation",
        "PaymentsToAcquirePropertyPlantAndEquipment": "Capital expenditures",
        "IncreaseDecreaseInInventories": "Change in inventories",
        "IncreaseDecreaseInAccountsReceivable": "Change in receivables",
        "IncreaseDecreaseInAccountsPayable": "Change in payables",
    },
}


def classify_period(start, end):
    """Return a period label or None if it's not a clean FY or recent quarter."""
    from datetime import date
    y, m, d = (int(x) for x in end.split("-"))
    e = date(y, m, d)
    if start:  # duration concept
        ys, ms, ds = (int(x) for x in start.split("-"))
        days = (e - date(ys, ms, ds)).days
        if 350 <= days <= 380 and end in TARGET_FYE:
            return f"FY{y}"
        if 80 <= days <= 100 and e >= date(2024, 9, 1):  # recent quarters only
            return f"Q/E {end}"
        return None
    else:  # instant concept (balance sheet)
        if end in TARGET_FYE:
            return f"FY{y}"
        if e >= date(2024, 9, 1):
            return f"Q/E {end}"
        return None


def main():
    print("Fetching companyfacts (one request)...")
    facts = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json")
    with open(os.path.join(SRC, "companyfacts_raw.json"), "w") as f:
        json.dump(facts, f)

    time.sleep(0.3)
    print("Fetching submissions (filing index)...")
    subs = get(f"https://data.sec.gov/submissions/CIK{CIK}.json")

    # Build accession -> filing URL map
    recent = subs["filings"]["recent"]
    acc_url, acc_doc, acc_date = {}, {}, {}
    for accn, prim, fdate, form in zip(
        recent["accessionNumber"], recent["primaryDocument"],
        recent["filingDate"], recent["form"]
    ):
        nodash = accn.replace("-", "")
        acc_url[accn] = f"https://www.sec.gov/Archives/edgar/data/{CIK_INT}/{nodash}/{prim}"
        acc_doc[accn] = prim
        acc_date[accn] = fdate

    # Write filings index
    with open(os.path.join(SRC, "filings.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["form", "filing_date", "accession", "url"])
        for accn, form, fdate in sorted(
            zip(recent["accessionNumber"], recent["form"], recent["filingDate"]),
            key=lambda x: x[2], reverse=True
        ):
            if form in ("10-K", "10-Q", "8-K", "DEF 14A", "NT 10-K", "10-K/A"):
                w.writerow([form, fdate, accn, acc_url.get(accn, "")])

    # Extract target facts
    usgaap = facts["facts"].get("us-gaap", {})
    rows = []
    for statement, concept_map in CONCEPTS.items():
        for concept, label in concept_map.items():
            node = usgaap.get(concept)
            if not node:
                rows.append([statement, label, concept, "", "", "NOT_TAGGED",
                             "", "", "", "FILED?"])
                continue
            unit = next(iter(node["units"]))
            seen = set()
            for r in node["units"][unit]:
                if r.get("form") not in ("10-K", "10-Q"):
                    continue
                period = classify_period(r.get("start"), r["end"])
                if not period:
                    continue
                key = (period, concept)
                if key in seen:
                    continue  # first (as-originally/most-authoritative) wins
                seen.add(key)
                accn = r.get("accn", "")
                rows.append([
                    statement, label, concept, period, r["val"], unit,
                    r.get("form", ""), accn, acc_url.get(accn, ""), "FILED",
                ])

    order = {"FY2023": 0, "FY2024": 1, "FY2025": 2}
    rows.sort(key=lambda x: (x[0], x[2], order.get(x[3], 9), x[3]))

    with open(os.path.join(SRC, "facts.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["statement", "line_item", "concept", "period", "value",
                    "units", "form", "accession", "source_url", "provenance"])
        w.writerows(rows)

    filed = [r for r in rows if r[9] == "FILED"]
    missing = [r for r in rows if r[5] == "NOT_TAGGED"]
    print(f"\nWrote {len(filed)} sourced facts to data/source/facts.csv")
    print(f"{len(missing)} concepts NOT tagged by SMCI (read the note by hand):")
    for r in missing:
        print(f"   - {r[1]} ({r[2]})")


if __name__ == "__main__":
    main()
