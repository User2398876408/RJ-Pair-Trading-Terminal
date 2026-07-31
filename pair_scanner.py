import os
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

from data_loader import StockLoader
from Config import DATA_FOLDER
from top50_pairs import generate_pairs


loader = StockLoader(DATA_FOLDER)


def bollinger_analysis(df, window=20):

    df["MA"] = df["Ratio"].rolling(window).mean()
    df["STD"] = df["Ratio"].rolling(window).std()

    df["Upper"] = df["MA"] + (2 * df["STD"])
    df["Lower"] = df["MA"] - (2 * df["STD"])

    last = df.iloc[-1]
    previous = df.iloc[-2]

    ratio = last["Ratio"]

    z_score = (
        (ratio - last["MA"])
        /
        last["STD"]
    )

    signal = "NO SIGNAL"

    # Cross below lower band
    if (
        previous["Ratio"] > previous["Lower"]
        and ratio < last["Lower"]
    ):
        signal = "LONG FIRST / SHORT SECOND"

    # Cross above upper band
    elif (
        previous["Ratio"] < previous["Upper"]
        and ratio > last["Upper"]
    ):
        signal = "SHORT FIRST / LONG SECOND"

    # Approaching lower band
    elif z_score < -1.8:
        signal = "WATCH LONG"

    # Approaching upper band
    elif z_score > 1.8:
        signal = "WATCH SHORT"

    return signal, round(z_score, 2)


def analyze_pair(stock1, stock2):

    a = loader.load(stock1)
    b = loader.load(stock2)

    df = a[["Date", "Close"]].merge(
        b[["Date", "Close"]],
        on="Date",
        suffixes=("_1", "_2")
    )

    if len(df) < 50:
        raise Exception("Not enough data")

    # Ratio
    df["Ratio"] = (
        df["Close_1"]
        /
        df["Close_2"]
    )

    # RSI
    df["RSI"] = RSIIndicator(
        close=df["Ratio"],
        window=14
    ).rsi()

    # MACD
    macd = MACD(df["Ratio"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # Bollinger
    signal, z = bollinger_analysis(df)

    last = df.iloc[-1]

    return {
        "Pair": f"{stock1}/{stock2}",
        "Ratio": round(last["Ratio"], 4),
        "Z-Score": z,
        "RSI": round(last["RSI"], 1),
        "MACD": round(last["MACD"], 4),
        "Signal": signal
    }


# Automatically generate every pair
pairs = generate_pairs()


def run_scanner():

    results = []

    for stock1, stock2 in pairs:

        try:

            results.append(
                analyze_pair(stock1, stock2)
            )

        except Exception as e:

            print(
                "Skipped:",
                stock1,
                stock2,
                e
            )

    result = pd.DataFrame(results)

    result = result.sort_values(
        by="Z-Score"
    )

    return result


if __name__ == "__main__":

    result = run_scanner()

    print("\nBOLLINGER PAIR SCANNER\n")

    print(result.to_string(index=False))

os.makedirs("results", exist_ok=True)

result.to_csv(
    "results/latest_scan.csv",
    index=False
)
