import yfinance as yf
from pathlib import Path

Path("data").mkdir(exist_ok=True)

stocks = [
    "AAPL",
    "MSFT",
    "NVDA",
    "^GSPC"
]

for ticker in stocks:

    print("Downloading", ticker)

    data = yf.download(
        ticker,
        start="2000-01-01",
        auto_adjust=False,
        progress=False
    )

    # Fix yfinance multi-index columns
    data.columns = data.columns.droplevel(1)

    filename = ticker.replace("^", "") + ".csv"

    data.to_csv(
        "data/" + filename
    )

print("Done!")
