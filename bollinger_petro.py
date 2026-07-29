import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# PETR3 and PETR4 Bollinger Bands Analyzer
# ==========================================


stocks = [
    "PETR3.SA",
    "PETR4.SA"
]


# Bollinger Band settings
period = 20
deviation = 2


def analyze_stock(stock):

    print("\n==============================")
    print("Analyzing:", stock)
    print("==============================")


    # Download 1 year of daily prices
    data = yf.download(
        stock,
        period="1y",
        interval="1d"
    )


    # Remove empty rows
    data = data.dropna()
    data.columns = data.columns.get_level_values(0)

    # Calculate Bollinger Bands

    data["Middle Band"] = (
        data["Close"]
        .rolling(period)
        .mean()
    )


    standard_deviation = (
        data["Close"]
        .rolling(period)
        .std()
    )


    data["Upper Band"] = (
        data["Middle Band"]
        +
        deviation * standard_deviation
    )


    data["Lower Band"] = (
        data["Middle Band"]
        -
        deviation * standard_deviation
    )


    # Latest values

    price = float(data["Close"].iloc[-1])

    upper = float(data["Upper Band"].iloc[-1])

    lower = float(data["Lower Band"].iloc[-1])


    print("Current price:", round(price, 2))
    print("Upper band:", round(upper, 2))
    print("Lower band:", round(lower, 2))


    # Trading signal

    if price <= lower:

        signal = "LONG"

        reason = (
            "Price is touching the lower Bollinger Band. "
            "Possible oversold condition."
        )


    elif price >= upper:

        signal = "SHORT"

        reason = (
            "Price is touching the upper Bollinger Band. "
            "Possible overbought condition."
        )


    else:

        signal = "WAIT"

        reason = (
            "Price is between the Bollinger Bands."
        )


    print("\n==============================")
    print("TRADING SIGNAL:", signal)
    print(reason)
    print("==============================\n")


    # Create chart

    plt.figure(figsize=(12,6))


    plt.plot(
        data.index,
        data["Close"],
        label="Price"
    )


    plt.plot(
        data.index,
        data["Upper Band"],
        label="Upper Bollinger Band"
    )


    plt.plot(
        data.index,
        data["Middle Band"],
        label="Middle Bollinger Band"
    )


    plt.plot(
        data.index,
        data["Lower Band"],
        label="Lower Bollinger Band"
    )


    plt.title(
        stock + " Bollinger Bands"
    )


    plt.legend()
    plt.grid()

    plt.show()



# Run analysis for both stocks

for stock in stocks:

    analyze_stock(stock)
    
