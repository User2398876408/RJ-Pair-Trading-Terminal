import yfinance as yf
from pathlib import Path


# Create data folder if it does not exist
Path("data").mkdir(exist_ok=True)


# Brazilian stocks (B3)
stocks = [
    "PETR3.SA",
    "PETR4.SA",
    "VALE3.SA",
    "ITUB3.SA",
    "ITUB4.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "ABEV3.SA",
    "WEGE3.SA",
    "SUZB3.SA",
    "RENT3.SA",
    "RADL3.SA",
    "LREN3.SA",
    "PRIO3.SA",
    "GGBR4.SA",
    "CSNA3.SA",
    "USIM5.SA",
    "HAPV3.SA",
    "RAIL3.SA",
    "EQTL3.SA",
    "TAEE11.SA",
    "CMIG4.SA",
    "SBSP3.SA",
    "VIVT3.SA",
    "TIMS3.SA",
    "KLBN11.SA",
    "B3SA3.SA",
    "CYRE3.SA",
    "TOTS3.SA",
    "YDUQ3.SA",
    "MULT3.SA",
    "BPAC11.SA",
    "IGTI11.SA"
]


for ticker in stocks:

    print("Downloading:", ticker)

    data = yf.download(
        ticker,
        start="2025-01-01",
        auto_adjust=False,
        progress=False
    )

    # Fix newer yfinance column format
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.droplevel(1)

    # Save without .SA
    filename = ticker.replace(".SA", "")

    data.to_csv(
        f"data/{filename}.csv"
    )


print("Download finished!")
