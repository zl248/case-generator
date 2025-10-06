"""Financial data retrieval from Yahoo Finance via yfinance.

Provides helpers to extract tickers from company names and to
format financial statement data for prompt inclusion.
"""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd
import yfinance as yf


COMPANY_TICKER_MAP: Dict[str, str] = {
    "Netflix": "NFLX",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Alphabet": "GOOGL",
}


def extract_ticker(company_name: str) -> Optional[str]:
    """Extract a ticker from a company name using a simple lookup.

    Args:
        company_name: Free-form company string from user input.

    Returns:
        Optional ticker symbol if recognized.
    """

    for key, value in COMPANY_TICKER_MAP.items():
        if key.lower() in company_name.lower():
            return value
    return None


def get_financial_data_yf(ticker: str, years: int = 5) -> Dict[str, Dict[str, Optional[float]]]:
    """Fetch financial statement data for a ticker using yfinance.

    Returns a mapping of year -> metrics (Revenue, Net Income, ...).
    """

    try:
        ticker_obj = yf.Ticker(ticker)
        financials = ticker_obj.financials
        cashflow = ticker_obj.cashflow
        balance = ticker_obj.balance_sheet

        financials = financials.iloc[:, :years]
        cashflow = cashflow.iloc[:, :years]
        balance = balance.iloc[:, :years]

        result: Dict[str, Dict[str, Optional[float]]] = {}
        for col in financials.columns:
            year = str(col.year)
            result[year] = {
                "Revenue": financials.get("Total Revenue", pd.Series()).get(col, None),
                "Net Income": financials.get("Net Income", pd.Series()).get(col, None),
                "Operating Income": financials.get("Operating Income", pd.Series()).get(col, None),
                "Gross Profit": financials.get("Gross Profit", pd.Series()).get(col, None),
                "Cash Flow": cashflow.get("Total Cash From Operating Activities", pd.Series()).get(col, None),
                "Total Assets": balance.get("Total Assets", pd.Series()).get(col, None),
                "Total Liabilities": balance.get("Total Liab", pd.Series()).get(col, None),
                "Shareholder Equity": balance.get("Total Stockholder Equity", pd.Series()).get(col, None),
            }
        return result
    except Exception as exc:  # pragma: no cover - defensive
        return {"error": str(exc)}  # type: ignore[return-value]


def format_financials_table(financial_data: Dict[str, Dict[str, Optional[float]]]) -> str:
    """Format financial data into a simple pipe-separated table.

    Values are rounded to millions USD where available.
    """

    if not financial_data or "error" in financial_data:
        return "No financial data available."

    years = list(financial_data.keys())
    header = [
        "Year",
        "Revenue",
        "Net Income",
        "Operating Income",
        "Gross Profit",
        "Cash Flow",
        "Total Assets",
        "Total Liabilities",
        "Shareholder Equity",
    ]
    table = [header]
    for year in years:
        row = [year]
        for metric in header[1:]:
            value = financial_data[year].get(metric)
            row.append(str(round(value / 1e6, 2)) if value else "-")
        table.append(row)
    return "\n".join([" | ".join(row) for row in table])


