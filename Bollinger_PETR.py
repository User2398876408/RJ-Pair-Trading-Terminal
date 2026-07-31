import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Download Petrobras stocks

petr3 = yf.download(
    "PETR3.SA",
    period="1y",
    interval="1d"
)

petr4 = yf.download(
    "PETR4.SA",
    period="1y",
    interval="1d"
)


# Fix yfinance columns

petr3.columns = petr3.columns.get_level_values(0)

petr4.columns = petr4.columns.get_level_values(0)


# Create PETR3/PETR4 ratio

ratio = petr3["Close"] / petr4["Close"]


# Calculate Bollinger Bands

period = 20

middle = ratio.rolling(period).mean()

std = ratio.rolling(period).std()


upper = middle + (2 * std)

lower = middle - (2 * std)


# Current ratio

current_ratio = ratio.iloc[-1]


print("==============================")
print("PETR3/PETR4 Ratio Analysis")
print("==============================")

print("Current ratio:", round(current_ratio,4))
print("Upper band:", round(upper.iloc[-1],4))
print("Lower band:", round(lower.iloc[-1],4))


# Trading signal

if current_ratio <= lower.iloc[-1]:

    print("SIGNAL: LONG PETR3 / SHORT PETR4")

elif current_ratio >= upper.iloc[-1]:

    print("SIGNAL: SHORT PETR3 / LONG PETR4")

else:

    print("SIGNAL: WAIT")


# Plot

plt.figure(figsize=(12,6))

plt.plot(
    ratio,
    label="PETR3/PETR4 Ratio"
)

plt.plot(
    upper,
    label="Upper Bollinger Band"
)

plt.plot(
    middle,
    label="Middle Band"
)

plt.plot(
    lower,
    label="Lower Bollinger Band"
)


plt.title("PETR3/PETR4 Ratio with Bollinger Bands")

plt.legend()

plt.grid()

plt.show()
