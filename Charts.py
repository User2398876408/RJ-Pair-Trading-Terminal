import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ta.momentum import RSIIndicator
from ta.trend import MACD


RJ_GREEN = "#3ddc84"
RJ_BACKGROUND = "#2e3a26"
RJ_PANEL = "#36452d"



def candlestick(df):


    df = df.copy()


    # =========================
    # INDICATORS
    # =========================


    if "RSI" not in df.columns:

        df["RSI"] = RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()



    if "MACD" not in df.columns:

        macd = MACD(
            close=df["Close"]
        )

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = (
            macd.macd_signal()
        )

        df["MACD_HIST"] = (
            macd.macd_diff()
        )



    # =========================
    # CHART STRUCTURE
    # =========================


    fig = make_subplots(

        rows=3,

        cols=1,

        shared_xaxes=True,

        vertical_spacing=0.03,

        row_heights=[

            0.65,
            0.20,
            0.15

        ]

    )



    # =========================
    # PRICE
    # =========================


    fig.add_trace(

        go.Candlestick(

            x=df["Date"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],


            increasing=dict(

                line=dict(
                    color=RJ_GREEN
                ),

                fillcolor=RJ_GREEN

            ),


            decreasing=dict(

                line=dict(
                    color="#ff5b5b"
                ),

                fillcolor="#ff5b5b"

            ),


            name="Price"

        ),

        row=1,

        col=1

    )




    # =========================
    # MOVING AVERAGES
    # =========================


    averages = [

        ("SMA20","#f5e642"),

        ("SMA50","#ff9f43"),

        ("SMA200","#ff5b5b")

    ]


    for column, color in averages:


        if column in df.columns:


            fig.add_trace(

                go.Scatter(

                    x=df["Date"],

                    y=df[column],

                    name=column,

                    line=dict(

                        color=color,

                        width=2

                    )

                ),

                row=1,

                col=1

            )



    # =========================
    # BOLLINGER BANDS
    # =========================

    bands = [

        ("BB_UPPER_1.5", "BB +1.5σ", "#00ff99"),
        ("BB_LOWER_1.5", "BB -1.5σ", "#00ff99"),

        ("BB_UPPER_2", "BB +2σ", "#888888"),
        ("BB_LOWER_2", "BB -2σ", "#888888"),

        ("BB_UPPER_3", "BB +3σ", "#ff5555"),
        ("BB_LOWER_3", "BB -3σ", "#ff5555")

    ]


    for column, name, color in bands:

        if column in df.columns:

            fig.add_trace(

                go.Scatter(

                    x=df["Date"],

                    y=df[column],

                    name=name,

                    line=dict(

                        color=color,

                        width=1

                    )

                ),

                row=1,

                col=1

            )




    # =========================
    # RSI
    # =========================


    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["RSI"],

            name="RSI",

            line=dict(

                color=RJ_GREEN,

                width=2

            )

        ),

        row=2,

        col=1

    )



    fig.add_hline(

        y=70,

        line_dash="dash",

        line_color="red",

        row=2,

        col=1

    )


    fig.add_hline(

        y=30,

        line_dash="dash",

        line_color="green",

        row=2,

        col=1

    )




    # =========================
    # MACD
    # =========================


    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["MACD"],

            name="MACD",

            line=dict(

                color="#00bfff"

            )

        ),

        row=3,

        col=1

    )



    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["MACD_SIGNAL"],

            name="Signal",

            line=dict(

                color="#ff9800"

            )

        ),

        row=3,

        col=1

    )



    fig.add_trace(

        go.Bar(

            x=df["Date"],

            y=df["MACD_HIST"],

            name="Histogram",

            marker_color=RJ_GREEN

        ),

        row=3,

        col=1

    )





    # =========================
    # PROFESSIONAL VIEW
    # =========================


    if len(df) > 250:

        start = df["Date"].iloc[-250]

    else:

        start = df["Date"].iloc[0]



    # Add empty future space
    # lets candles breathe like TradingView


    if len(df) > 20:

        future_space = (

            df["Date"].iloc[-1]

            -

            df["Date"].iloc[-20]

        )


        fig.update_xaxes(

            range=[

                start,

                df["Date"].iloc[-1] + future_space * 0.5

            ]

        )


    else:

        fig.update_xaxes(

            range=[

                start,

                df["Date"].iloc[-1]

            ]

        )




    # =========================
    # LAYOUT
    # =========================


    fig.update_layout(

        template="plotly_dark",

        height=1000,

        paper_bgcolor=RJ_BACKGROUND,

        plot_bgcolor=RJ_PANEL,


        hovermode="x unified",


        xaxis_rangeslider_visible=False,


        dragmode="pan",


        legend=dict(

            orientation="h",

            y=1.02,

            x=0

        ),


        margin=dict(

            l=50,

            r=50,

            t=50,

            b=50

        ),


        font=dict(

            color="white"

        )

    )




    # =========================
    # MOUSE CONTROLS
    # =========================


    fig.update_layout(

        xaxis=dict(

            fixedrange=False

        ),

        yaxis=dict(

            fixedrange=False

        )

    )



    fig.update_xaxes(

        gridcolor="rgba(255,255,255,0.05)"

    )


    fig.update_yaxes(

        gridcolor="rgba(255,255,255,0.05)"

    )



    return fig
