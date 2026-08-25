"""
qoe.labels — SMCI-specific wiring between the source data's labels and canonical concepts.

finlib stays company-agnostic; this file is where SMCI's particular line-item names live.
`pick` tries each alias in order and returns the first sourced value, so a relabel in the CSV
doesn't break the model. If none match, it RAISES (via FactSet.value) — never a silent zero.
"""
from __future__ import annotations
from finlib.facts import FactSet


def pick(fs: FactSet, period: str, *aliases: str) -> float:
    """First sourced alias wins; raise if none exist."""
    for a in aliases:
        if fs.has(a, period):
            return fs.value(a, period)
    # Force a clear error naming the first alias.
    return fs.value(aliases[0], period)


# Canonical accessors -----------------------------------------------------------
def revenue(fs, p):      return pick(fs, p, "Revenue", "Net sales")
def cogs(fs, p):         return pick(fs, p, "Cost of revenue (alt tag)", "Cost of revenue", "Cost of sales")
def gross_profit(fs, p): return pick(fs, p, "Gross profit")
def operating_income(fs, p): return pick(fs, p, "Operating income", "Income from operations")
def net_income(fs, p):   return pick(fs, p, "Net income")
def pretax_income(fs, p): return pick(fs, p, "Pre-tax income", "Income before income tax provision")
def tax(fs, p):          return pick(fs, p, "Income tax expense", "Income tax provision")
def rnd(fs, p):          return pick(fs, p, "R&D expense", "Research and development")


def sga(fs, p):
    """SMCI splits opex into Sales & marketing and General & administrative; sum them."""
    return pick(fs, p, "Sales and marketing") + pick(fs, p, "General and administrative")


def ga(fs, p):           return pick(fs, p, "General and administrative")

# Cash flow
def cfo(fs, p):          return pick(fs, p, "Operating cash flow")
def dna(fs, p):          return pick(fs, p, "D&A (cash flow)")
def capex(fs, p):        return pick(fs, p, "Capital expenditures")
def sbc(fs, p):          return pick(fs, p, "Stock-based compensation")

# Balance sheet
def cash(fs, p):         return pick(fs, p, "Cash & equivalents")
def ar(fs, p):           return pick(fs, p, "Accounts receivable, net")
def inventory(fs, p):    return pick(fs, p, "Inventories, net")
def ap(fs, p):           return pick(fs, p, "Accounts payable")
def prepaid(fs, p):      return pick(fs, p, "Prepaid & other current assets")
def accrued(fs, p):      return pick(fs, p, "Accrued liabilities")
def deferred_rev(fs, p): return pick(fs, p, "Deferred revenue, current")
def cur_assets(fs, p):   return pick(fs, p, "Total current assets")
def cur_liabs(fs, p):    return pick(fs, p, "Total current liabilities")
def total_assets(fs, p): return pick(fs, p, "Total assets")
def total_liabs(fs, p):  return pick(fs, p, "Total liabilities")
def total_equity(fs, p): return pick(fs, p, "Total equity incl. NCI", "Total stockholders' equity")

# Capital structure (debt = cash-free/debt-free bridge inputs)
def convertible_notes(fs, p): return pick(fs, p, "Convertible notes")
def term_loans_nc(fs, p):     return fs.opt("Term loans non-current", p, 0.0) or 0.0
def loc_and_current_debt(fs, p): return fs.opt("Lines of credit and current portion of term loans", p, 0.0) or 0.0


def total_debt(fs, p) -> float:
    """Convertibles + non-current term loans + lines of credit/current term-loan portion."""
    return convertible_notes(fs, p) + term_loans_nc(fs, p) + loc_and_current_debt(fs, p)


def net_debt(fs, p) -> float:
    """Total debt less cash. Negative => net cash position."""
    return total_debt(fs, p) - cash(fs, p)


# Related party (from the RP note)
def rp_cogs(fs, p):      return pick(fs, p, "Related party COGS - total")
def rp_sales(fs, p):     return pick(fs, p, "Related party net sales - total")
