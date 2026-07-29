import pandas as pd

from dash import Dash, html, dcc, Input, Output
from datetime import datetime

from data_loader import StockLoader
from Config import DATA_FOLDER
from Charts import candlestick
from top50_pairs import get_valid_stocks

# =========================
# APP CONFIG
# =========================

app = Dash(__name__)

loader = StockLoader(DATA_FOLDER)


RJ_GREEN = "#3ddc84"
RJ_BACKGROUND = "#2e3a26"
RJ_PANEL = "#36452d"



# =========================
# LOAD RESULTS
# =========================

def load_results():

    return pd.read_csv(
        "results/latest_scan.csv"
    )



# =========================
# TIMEFRAME
# =========================

def apply_timeframe(df, timeframe):

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    df = df.set_index(
        "Date"
    )


    rules = {

        "1d": "1D",
        "1wk": "1W",
        "1mo": "1ME"

    }


    if timeframe in rules:

        df = df.resample(
            rules[timeframe]
        ).agg({

            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last"

        })


    df.dropna(inplace=True)

    df.reset_index(inplace=True)


    return df



# =========================
# INDICATORS
# =========================

def add_indicators(df):

    df = df.copy()


    df["SMA20"] = (
        df["Close"]
        .rolling(20)
        .mean()
    )


    df["SMA50"] = (
        df["Close"]
        .rolling(50)
        .mean()
    )


    if len(df) >= 200:

        df["SMA200"] = (
            df["Close"]
            .rolling(200)
            .mean()
        )

    else:

        df["SMA200"] = None



    middle = (
        df["Close"]
        .rolling(20)
        .mean()
    )


    std = (
        df["Close"]
        .rolling(20)
        .std()
    )


    df["BB_MIDDLE"] = middle


    df["BB_UPPER_1.5"] = (
        middle + (1.5 * std)
    )


    df["BB_LOWER_1.5"] = (
        middle - (1.5 * std)
    )


    df["BB_UPPER_2"] = (
        middle + (2 * std)
    )


    df["BB_LOWER_2"] = (
        middle - (2 * std)
    )


    df["BB_UPPER_3"] = (
        middle + (3 * std)
    )


    df["BB_LOWER_3"] = (
        middle - (3 * std)
    )


    return df



# =========================
# BUILD RATIO CHART
# =========================

def build_ratio(stock1, stock2):

    a = loader.load(stock1)

    b = loader.load(stock2)


    df = a.merge(

        b,

        on="Date",

        suffixes=("_1", "_2")

    )


    ratio = pd.DataFrame()


    ratio["Date"] = df["Date"]


    ratio["Open"] = (
        df["Open_1"]
        /
        df["Open_2"]
    )


    ratio["High"] = (
        df["High_1"]
        /
        df["High_2"]
    )


    ratio["Low"] = (
        df["Low_1"]
        /
        df["Low_2"]
    )


    ratio["Close"] = (
        df["Close_1"]
        /
        df["Close_2"]
    )


    return ratio

# =========================
# CREATE GRAPH
# =========================

def create_graph(stock1, stock2, timeframe):


    df = build_ratio(
        stock1,
        stock2
    )


    df = apply_timeframe(
        df,
        timeframe
    )


    df = add_indicators(
        df
    )


    return candlestick(
        df
    )



# =========================
# DATA
# =========================

results = load_results()


signal_order = {

    "LONG FIRST / SHORT SECOND": 0,

    "SHORT FIRST / LONG SECOND": 1,

    "WATCH LONG": 2,

    "WATCH SHORT": 3,

    "NO SIGNAL": 4

}


results = results.sort_values(

    by="Signal",

    key=lambda x: x.map(signal_order).fillna(99)

)



tickers = get_valid_stocks()


dropdown_options = [

    {
        "label": ticker,
        "value": ticker
    }

    for ticker in tickers

]


default_stock1 = tickers[0]

default_stock2 = tickers[1]



# =========================
# LAYOUT
# =========================

app.layout = html.Div(

    style={

        "backgroundColor": RJ_BACKGROUND,

        "minHeight": "100vh",

        "padding": "30px",

        "fontFamily": "Arial",

        "color": "white"

    },


    children=[


        html.Div(

            [

                html.Img(

                    src="/assets/RJ+_PRETO.png",

                    style={

                        "height": "80px",

                        "marginRight": "20px"

                    }

                ),


                html.H1(

                    "RJ+ Pair Trading Terminal",

                    style={

                        "fontSize": "40px",

                        "margin": "0"

                    }

                )

            ],


            style={

                "display": "flex",

                "alignItems": "center"

            }

        ),



        html.Hr(),



        html.H3(
            "First Stock"
        ),


        dcc.Dropdown(

            id="stock1",

            options=dropdown_options,

            value=default_stock1,

            style={

                "color": "black"

            }

        ),



        html.Br(),



        html.H3(
            "Second Stock"
        ),


        dcc.Dropdown(

            id="stock2",

            options=dropdown_options,

            value=default_stock2,

            style={

                "color": "black"

            }

        ),



        html.Br(),



        html.H3(
            "Timeframe"
        ),



        dcc.Dropdown(

            id="timeframe",

            options=[

                {
                    "label": "1 Day",
                    "value": "1d"
                },

                {
                    "label": "1 Week",
                    "value": "1wk"
                },

                {
                    "label": "1 Month",
                    "value": "1mo"
                }

            ],

            value="1d",

            style={

                "color": "black"

            }

        ),



        html.Br(),



        html.Div(

            id="stats",

            style={

                "backgroundColor": RJ_PANEL,

                "padding": "20px",

                "borderRadius": "15px"

            }

        ),



        html.Br(),



        dcc.Graph(

            id="pair_graph"

        ),



        dcc.Interval(

            id="market_refresh",

            interval=60000,

            n_intervals=0

        ),



        html.Div(

            id="last_update",

            style={

                "color": RJ_GREEN

            }

        )

    ]

)

# =========================
# CALLBACK
# =========================

@app.callback(

    Output("stats", "children"),

    Output("pair_graph", "figure"),

    Output("last_update", "children"),


    Input("stock1", "value"),

    Input("stock2", "value"),

    Input("timeframe", "value"),

    Input("market_refresh", "n_intervals")

)


def update(stock1, stock2, timeframe, n):


    pair = f"{stock1}/{stock2}"


    results = load_results()


    match = results[

        results["Pair"] == pair

    ]



    # If the pair exists in scanner results

    if len(match) > 0:


        row = match.iloc[0]


        stats = [

            html.H2(pair),


            html.P(
                f"Signal: {row['Signal']}"
            ),


            html.P(
                f"Ratio: {row['Ratio']}"
            ),


            html.P(
                f"Z-Score: {row['Z-Score']}"
            ),


            html.P(
                f"RSI: {row['RSI']}"
            ),


            html.P(
                f"MACD: {row['MACD']}"
            ),


            html.H2(

                row["Signal"],

                style={

                    "color": RJ_GREEN

                }

            )

        ]


    else:


        stats = [

            html.H2(pair),


            html.P(
                "Pair not found in scanner results"
            ),


            html.P(
                "Chart is showing live ratio"
            )

        ]



    graph = create_graph(

        stock1,

        stock2,

        timeframe

    )



    update_time = (

        "LIVE UPDATE: "

        +

        datetime.now()

        .strftime("%H:%M:%S")

    )



    return (

        stats,

        graph,

        update_time

    )



# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
