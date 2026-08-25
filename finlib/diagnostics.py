"""
finlib.diagnostics — earnings-quality and working-capital math.

PURE FUNCTIONS ONLY. Each takes plain numbers and returns a number. No I/O, no FactSet, no
company-specific labels. That is what makes this module reusable by the anomaly screener
(project 2): it wires its own data in; the math is identical.

Conventions:
- Balances can be period-end or average; the caller decides and stays consistent. Helpers that
  need an average take it explicitly (avg_*), so the choice is visible at the call site.
- Days basis defaults to 365; override for 360 if a house convention requires it.
"""
from __future__ import annotations


def avg(a: float, b: float) -> float:
    return (a + b) / 2.0


# ---- Cash conversion cycle ----------------------------------------------------
def dso(accounts_receivable: float, revenue: float, days: int = 365) -> float:
    """Days Sales Outstanding. Rising DSO on flat terms is a collection / revenue-timing signal."""
    return accounts_receivable / revenue * days


def dio(inventory: float, cogs: float, days: int = 365) -> float:
    """Days Inventory Outstanding. Rising DIO against growth = cash tied up in stock."""
    return inventory / cogs * days


def dpo(accounts_payable: float, cogs: float, days: int = 365) -> float:
    """Days Payable Outstanding. Watch for period-end spikes that flatter working capital."""
    return accounts_payable / cogs * days


def ccc(dso_days: float, dio_days: float, dpo_days: float) -> float:
    """Cash Conversion Cycle = DIO + DSO - DPO. Days of cash tied up per operating cycle."""
    return dio_days + dso_days - dpo_days


# ---- Earnings quality ---------------------------------------------------------
def accruals_ratio_cf(net_income: float, cfo: float, avg_total_assets: float) -> float:
    """
    Sloan (1996) cash-flow accruals ratio = (Net income - Operating cash flow) / avg total assets.
    High positive value = earnings driven by accruals not cash. Devastating when NI>0 but CFO<0.
    """
    return (net_income - cfo) / avg_total_assets


def accruals_ratio_bs(noa_end: float, noa_beg: float, avg_total_assets: float) -> float:
    """Balance-sheet accruals = change in net operating assets / avg total assets. Cross-check to CF."""
    return (noa_end - noa_beg) / avg_total_assets


# ---- Beneish M-score components (Beneish 1999) --------------------------------
# Each index compares the current year (t) to the prior year (t-1). >1 generally = deterioration.
def dsri(ar_t, sales_t, ar_p, sales_p):
    """Days Sales in Receivables Index. >1 => receivables growing faster than sales (revenue-quality flag)."""
    return (ar_t / sales_t) / (ar_p / sales_p)


def gmi(gross_margin_p, gross_margin_t):
    """Gross Margin Index. >1 => margins deteriorating (motive to manipulate)."""
    return gross_margin_p / gross_margin_t


def aqi(current_assets_t, ppe_t, total_assets_t, current_assets_p, ppe_p, total_assets_p):
    """Asset Quality Index. >1 => more soft/intangible assets (capitalizing costs)."""
    q_t = 1 - (current_assets_t + ppe_t) / total_assets_t
    q_p = 1 - (current_assets_p + ppe_p) / total_assets_p
    return q_t / q_p


def sgi(sales_t, sales_p):
    """Sales Growth Index. High growth isn't manipulation, but raises pressure/opportunity."""
    return sales_t / sales_p


def depi(dep_p, ppe_gross_p, dep_t, ppe_gross_t):
    """Depreciation Index. >1 => slowing depreciation (income-inflating)."""
    rate_p = dep_p / (dep_p + ppe_gross_p)
    rate_t = dep_t / (dep_t + ppe_gross_t)
    return rate_p / rate_t


def sgai(sga_t, sales_t, sga_p, sales_p):
    """SG&A Index. >1 => SG&A growing faster than sales (loss of efficiency)."""
    return (sga_t / sales_t) / (sga_p / sales_p)


def lvgi(liab_t, assets_t, liab_p, assets_p):
    """Leverage Index. >1 => leverage rising (debt-covenant pressure)."""
    return (liab_t / assets_t) / (liab_p / assets_p)


def tata(net_income_t, cfo_t, total_assets_t):
    """Total Accruals to Total Assets. Higher => more accrual-based earnings."""
    return (net_income_t - cfo_t) / total_assets_t


def m_score(dsri_, gmi_, aqi_, sgi_, depi_, sgai_, tata_, lvgi_) -> float:
    """
    Beneish 8-variable M-score. Threshold ~ -1.78: above it flags elevated manipulation likelihood.
    NOTE: built for manufacturers; a hyper-growth hardware co. will score high on SGI/TATA for
    benign reasons. Use as a screen and a talking point, not a verdict. Interpret component-by-
    component, which is why every component is exposed separately above.
    """
    return (-4.84
            + 0.920 * dsri_
            + 0.528 * gmi_
            + 0.404 * aqi_
            + 0.892 * sgi_
            + 0.115 * depi_
            - 0.172 * sgai_
            + 4.679 * tata_
            - 0.327 * lvgi_)


M_SCORE_THRESHOLD = -1.78
