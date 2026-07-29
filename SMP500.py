from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_FOLDER = BASE_DIR / "data"

SP500_FILE = DATA_FOLDER / "SP500.csv"

DEFAULT_THEME = "plotly_dark"

REFRESH_SECONDS = 30
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

        df = pd.read_csv(file)

        df.columns = [c.strip() for c in df.columns]

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])

        df.sort_values("Date", inplace=True)

        return df

    def load_sp500(self):

        df = pd.read_csv(self.folder / "SP500.csv")

        df["Date"] = pd.to_datetime(df["Date"])

        return df
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
import plotly.graph_objects as go

def candlestick(df):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA20"],
            name="SMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA50"],
            name="SMA50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA200"],
            name="SMA200"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=800,
        xaxis_rangeslider_visible=False
    )

    return fig
from dash import Dash
from dash import html
from dash import dcc
from dash import Input
from dash import Output

from config import *
from data_loader import StockLoader
from indicators import add_indicators
from charts import candlestick

loader = StockLoader(DATA_FOLDER)

app = Dash(__name__)

app.title = "Professional Stock Dashboard"

app.layout = html.Div([

    html.H1("Professional Stock Dashboard"),

    dcc.Dropdown(
        id="ticker",
        options=[
            {"label":t,"value":t}
            for t in loader.list_tickers()
        ],
        value=loader.list_tickers()[0]
    ),

    dcc.Graph(id="chart")

])

@app.callback(

    Output("chart","figure"),

    Input("ticker","value")

)

def update_chart(ticker):

    df = loader.load(ticker)

    df = add_indicators(df)

    return candlestick(df)

if __name__ == "__main__":

    app.run(debug=True)
