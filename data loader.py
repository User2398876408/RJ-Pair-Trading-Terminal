import pandas as pd
from pathlib import Path


class StockLoader:

    def __init__(self, folder):
        self.folder = Path(folder)

    def list_tickers(self):

        return sorted([
            f.stem
            for f in self.folder.glob("*.csv")
            if f.stem.upper() != "SP500"
        ])

    def load(self, ticker):

        file = self.folder / f"{ticker}.csv"

        df = pd.read_csv(file, skiprows=[1])

        df.columns = [
            "Date",
            "Adj Close",
            "Close",
            "High",
            "Low",
            "Open",
            "Volume"
        ]

        df["Date"] = pd.to_datetime(df["Date"])

        for col in [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df = df.dropna()

        return df


    def load_sp500(self):

        file = self.folder / "SP500.csv"

        df = pd.read_csv(file, skiprows=[1])

        df.columns = [
            "Date",
            "Adj Close",
            "Close",
            "High",
            "Low",
            "Open",
            "Volume"
        ]

        df["Date"] = pd.to_datetime(df["Date"])

        return df
