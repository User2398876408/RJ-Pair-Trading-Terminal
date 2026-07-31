import pandas as pd

from dash import Dash, html, dcc, Input, Output
from datetime import datetime

from data_loader import StockLoader
from Config import DATA_FOLDER
from Charts import candlestick
from top50_pairs import get_valid_stocks
from signals_panel import register_signals_panel
from signal_ranking import generate_stock_ranking

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


stock_ranking = generate_stock_ranking(
    results
)


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
        "padding": "24px",
        "fontFamily": "Arial",
        "color": "white"
    },

    children=[

        # =========================
        # HEADER
        # =========================

        html.Div(

            [

                html.Div(

                    [

                        html.Img(

                            src="/assets/RJ_BRANCO.png",

                            style={
                                "height": "65px",
                                "marginRight": "18px"
                            }

                        ),

                        html.Div(

                            [

                                html.H1(

                                    "Pair Trading Terminal",

                                    style={
                                        "fontSize": "32px",
                                        "margin": "0"
                                    }

                                ),

                                html.P(

                                    "IBOVESPA statistical trading dashboard",

                                    style={
                                        "margin": "4px 0 0 0",
                                        "color": "#b8c4b8",
                                        "fontSize": "14px"
                                    }

                                )

                            ]

                        )

                    ],

                    style={
                        "display": "flex",
                        "alignItems": "center"
                    }

                ),

                html.Div(

                    id="last_update",

                    style={
                        "color": RJ_GREEN,
                        "fontSize": "13px",
                        "fontWeight": "bold"
                    }

                )

            ],

            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "backgroundColor": RJ_PANEL,
                "padding": "16px 20px",
                "borderRadius": "14px",
                "marginBottom": "18px"
            }

        ),


        # =========================
        # COLLAPSIBLE CONTROLS
        # =========================

        html.Details(

            open=True,

            style={
                "backgroundColor": RJ_PANEL,
                "padding": "16px 20px",
                "borderRadius": "14px",
                "marginBottom": "18px"
            },

            children=[

                html.Summary(

                    "Trading Controls",

                    style={
                        "cursor": "pointer",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "marginBottom": "15px"
                    }

                ),

                html.Div(

                    [

                        html.Div(

                            [

                                html.Label(

                                    "First Stock",

                                    style={
                                        "display": "block",
                                        "marginBottom": "7px",
                                        "fontWeight": "bold"
                                    }

                                ),

                                dcc.Dropdown(

                                    id="stock1",
                                    options=dropdown_options,
                                    value=default_stock1,
                                    clearable=False,

                                    style={
                                        "color": "black"
                                    }

                                )

                            ],

                            style={
                                "flex": "1",
                                "minWidth": "200px"
                            }

                        ),

                        html.Div(

                            [

                                html.Label(

                                    "Second Stock",

                                    style={
                                        "display": "block",
                                        "marginBottom": "7px",
                                        "fontWeight": "bold"
                                    }

                                ),

                                dcc.Dropdown(

                                    id="stock2",
                                    options=dropdown_options,
                                    value=default_stock2,
                                    clearable=False,

                                    style={
                                        "color": "black"
                                    }

                                )

                            ],

                            style={
                                "flex": "1",
                                "minWidth": "200px"
                            }

                        ),

                        html.Div(

                            [

                                html.Label(

                                    "Timeframe",

                                    style={
                                        "display": "block",
                                        "marginBottom": "7px",
                                        "fontWeight": "bold"
                                    }

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
                                    clearable=False,

                                    style={
                                        "color": "black"
                                    }

                                )

                            ],

                            style={
                                "flex": "1",
                                "minWidth": "200px"
                            }

                        )

                    ],

                    style={
                        "display": "flex",
                        "gap": "18px",
                        "flexWrap": "wrap",
                        "marginTop": "15px"
                    }

                )

            ]

        ),


        # =========================
        # CHART
        # =========================

        html.Div(

            [

                html.Div(

                    [

                        html.H2(

                            "Pair Ratio Analysis",

                            style={
                                "margin": "0"
                            }

                        ),

                        html.P(

                            "Candlestick ratio with Bollinger Bands, RSI and MACD",

                            style={
                                "margin": "5px 0 0 0",
                                "color": "#b8c4b8",
                                "fontSize": "14px"
                            }

                        )

                    ],

                    style={
                        "padding": "18px 20px 0 20px"
                    }

                ),

                dcc.Graph(

                    id="pair_graph",

                    config={
                        "displaylogo": False,
                        "scrollZoom": True,
                        "responsive": True
                    },

                    style={
                        "width": "100%"
                    }

                )

            ],

            style={
                "backgroundColor": RJ_PANEL,
                "borderRadius": "14px",
                "overflow": "hidden",
                "marginBottom": "18px"
            }

        ),


        # =========================
        # SIGNALS + RANKING
        # =========================

        html.Div(

            [

                # LEFT SIDE
                html.Div(

                    register_signals_panel(app),

                    style={
                        "flex": "3",
                        "minWidth": "650px"
                    }

                ),

                # RIGHT SIDE
                html.Div(

                    [

                        html.H3(

                            "IBOVESPA Stock Ranking",

                            style={
                                "marginTop": "0",
                                "marginBottom": "14px"
                            }

                        ),

                        html.Div(
                            id="stock-ranking"
                        )

                    ],

                    style={
                        "flex": "1",
                        "minWidth": "260px",
                        "backgroundColor": "#1f2b1f",
                        "padding": "15px",
                        "borderRadius": "12px",
                        "marginTop": "15px"
                    }

                )

            ],

            style={
                "display": "flex",
                "alignItems": "flex-start",
                "gap": "18px",
                "flexWrap": "wrap"
            }

        ),


        # =========================
        # REFRESH
        # =========================

        dcc.Interval(

            id="market_refresh",
            interval=60000,
            n_intervals=0

        )

    ]

)

# =========================
# CALLBACK
# =========================

@app.callback(

    Output("pair_graph", "figure"),

    Output("last_update", "children"),


    Input("stock1", "value"),

    Input("stock2", "value"),

    Input("timeframe", "value"),

    Input("market_refresh", "n_intervals")

)


def update(stock1, stock2, timeframe, n):



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


        graph,

        update_time

    )


@app.callback(
    Output("stock-ranking", "children"),
    Input("market_refresh", "n_intervals")
)
def update_stock_ranking(n):

    results = load_results()

    ranking = generate_stock_ranking(
        results
    )

    rows = []

    for index, row in ranking.head(15).iterrows():

        score = float(row["Score"])
        signal = row["Signal"]

        if score > 0:
            signal_color = RJ_GREEN

        elif score < 0:
            signal_color = "#ff5555"

        else:
            signal_color = "#cccccc"


        rows.append(

            html.Div(

                [

                    html.Div(

                        [

                            html.Span(

                                str(index + 1),

                                style={
                                    "color": "#91a091",
                                    "fontSize": "12px",
                                    "width": "22px"
                                }

                            ),

                            html.Span(

                                row["Stock"],

                                style={
                                    "fontWeight": "bold",
                                    "fontSize": "14px"
                                }

                            )

                        ],

                        style={
                            "display": "flex",
                            "alignItems": "center"
                        }

                    ),

                    html.Div(

                        [

                            html.Span(

                                f"{score:.2f}",

                                style={
                                    "fontWeight": "bold",
                                    "fontSize": "13px"
                                }

                            ),

                            html.Span(

                                signal,

                                style={
                                    "color": signal_color,
                                    "fontWeight": "bold",
                                    "fontSize": "11px",
                                    "marginLeft": "10px",
                                    "minWidth": "68px",
                                    "textAlign": "right"
                                }

                            )

                        ],

                        style={
                            "display": "flex",
                            "alignItems": "center"
                        }

                    )

                ],

                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "padding": "10px 8px",
                    "borderBottom": "1px solid rgba(255,255,255,0.08)"
                }

            )

        )

    return rows

# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
