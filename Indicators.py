from ta.trend import SMAIndicator
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

def add_indicators(df):

    close = df["Close"]

    df["SMA20"] = SMAIndicator(close,20).sma_indicator()
    df["SMA50"] = SMAIndicator(close,50).sma_indicator()
    df["SMA200"] = SMAIndicator(close,200).sma_indicator()

    df["EMA20"] = EMAIndicator(close,20).ema_indicator()

    rsi = RSIIndicator(close)

    df["RSI"] = rsi.rsi()

    macd = MACD(close)

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    bb = BollingerBands(close)

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df
