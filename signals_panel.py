from pathlib import Path

import pandas as pd

from dash import html, dcc, Input, Output, State, ctx
import dash

from Config import REFRESH_SECONDS


RESULTS_FILE = Path(__file__).parent / "results" / "latest_scan.csv"


RJ_GREEN = "#3ddc84"
RJ_RED = "#ff5555"


# =========================
# LOAD RESULTS
# =========================

def _load_results():

    try:
        df = pd.read_csv(RESULTS_FILE)
        df.columns = [c.strip() for c in df.columns]

        return df

    except Exception:

        return pd.DataFrame(
            columns=[
                "Pair",
                "Ratio",
                "Z-Score",
                "RSI",
                "MACD",
                "Signal"
            ]
        )



# =========================
# TRADE STRUCTURE
# =========================

def get_trade_structure(pair, signal):

    if "/" not in str(pair):

        return html.Div("NO ACTIVE SIGNAL")


    stock1, stock2 = pair.split("/", 1)


    if signal == "LONG FIRST / SHORT SECOND":

        long_stock = stock1
        short_stock = stock2


    elif signal == "SHORT FIRST / LONG SECOND":

        long_stock = stock2
        short_stock = stock1


    else:

        return html.Div("NO ACTIVE SIGNAL")


    return html.Div(
        [

            html.Div(
                f"LONG: {long_stock}",
                style={
                    "color": RJ_GREEN,
                    "fontWeight": "bold"
                }
            ),


            html.Div(
                f"SHORT: {short_stock}",
                style={
                    "color": RJ_RED,
                    "fontWeight": "bold"
                }
            )

        ]
    )



# =========================
# DISPLAY SIGNAL NAME
# =========================

def display_signal(signal):

    names = {

        "LONG FIRST / SHORT SECOND":
            "PAIR TRADING OPPORTUNITY",

        "SHORT FIRST / LONG SECOND":
            "PAIR TRADING OPPORTUNITY",

        "WATCH LONG":
            "LONG OPPORTUNITY DEVELOPING",

        "WATCH SHORT":
            "SHORT OPPORTUNITY DEVELOPING",

        "NO SIGNAL":
            "NO TRADING OPPORTUNITY"

    }

    return names.get(signal, signal)



# =========================
# REGISTER PANEL
# =========================

def register_signals_panel(app: dash.Dash):


    panel = html.Div(

        id="signals-panel",

        style={

            "backgroundColor": "#1f2b1f",

            "padding": "15px",

            "borderRadius": "12px",

            "marginTop": "15px"

        },


        children=[


            html.H3(
                "Pair Trading Signals",
                style={
                    "color":"white"
                }
            ),



            dcc.Dropdown(

                id="signal_filter",

                options=[

                    {
                        "label":"ALL PAIRS",
                        "value":"ALL"
                    },

                    {
                        "label":"PAIR TRADING OPPORTUNITIES",
                        "value":"ACTIVE"
                    },

                    {
                        "label":"LONG OPPORTUNITY DEVELOPING",
                        "value":"WATCH LONG"
                    },

                    {
                        "label":"SHORT OPPORTUNITY DEVELOPING",
                        "value":"WATCH SHORT"
                    },

                    {
                        "label":"NO TRADING OPPORTUNITY",
                        "value":"NO SIGNAL"
                    }

                ],

                value="ALL",

                clearable=False,

                style={
                    "color":"black"
                }

            ),



            html.Br(),



            dcc.Dropdown(

                id="pair_selector",

                options=[],

                placeholder="Select pair",

                clearable=True,

                style={
                    "color":"black"
                }

            ),



            dcc.Store(

                id="signals_display_limit",

                data=15

            ),



            html.Br(),



            html.Div(
                id="signals_table_container"
            ),



            html.Div(

                [

                    html.Button(
                        "SHOW MORE",
                        id="show_more_signals",
                        n_clicks=0,
                        style={
                            "marginRight":"10px"
                        }
                    ),


                    html.Button(
                        "SHOW LESS",
                        id="show_less_signals",
                        n_clicks=0
                    )

                ],

                style={
                    "marginTop":"15px"
                }

            ),



            dcc.Interval(

                id="signals_refresh",

                interval=max(1, REFRESH_SECONDS) * 1000
                if REFRESH_SECONDS
                else 30000,

                n_intervals=0

            )

        ]

    )



    # =========================
    # UPDATE TABLE
    # =========================

    @app.callback(

        Output("pair_selector","options"),

        Output("pair_selector","value"),

        Output("signals_table_container","children"),

        Output("signals_display_limit","data"),


        Input("signal_filter","value"),

        Input("signals_refresh","n_intervals"),

        Input("show_more_signals","n_clicks"),

        Input("show_less_signals","n_clicks"),


        State("pair_selector","value"),

        State("signals_display_limit","data")

    )


    def update_signals(
        signal_filter,
        refresh,
        more_clicks,
        less_clicks,
        selected_pair,
        current_limit
    ):


        limit = current_limit or 15


        trigger = ctx.triggered_id


        if trigger == "show_more_signals":

            limit += 15


        elif trigger == "show_less_signals":

            limit = 15



        df = _load_results()



        if df.empty:

            return [], None, html.P(
                "No results found",
                style={
                    "color":"white"
                }
            ), 15



        if signal_filter == "ACTIVE":

            df = df[
                df["Signal"].isin(
                    [
                        "LONG FIRST / SHORT SECOND",
                        "SHORT FIRST / LONG SECOND"
                    ]
                )
            ]


        elif signal_filter == "WATCH LONG":

            df = df[
                df["Signal"] == "WATCH LONG"
            ]


        elif signal_filter == "WATCH SHORT":

            df = df[
                df["Signal"] == "WATCH SHORT"
            ]


        elif signal_filter == "NO SIGNAL":

            df = df[
                df["Signal"] == "NO SIGNAL"
            ]



        options = [

            {
                "label": pair,
                "value": pair
            }

            for pair in df["Pair"].unique()

        ]



        if selected_pair:

            df = df[
                df["Pair"] == selected_pair
            ]



        try:

            df["abs_z"] = (
                df["Z-Score"]
                .astype(float)
                .abs()
            )

            df = df.sort_values(
                "abs_z",
                ascending=False
            )

        except Exception:

            pass



        visible = df.head(limit)



        rows = []



        for _, row in visible.iterrows():

            rows.append(

                html.Tr(

                    [

                        html.Td(row["Pair"]),


                        html.Td(
                            display_signal(
                                row["Signal"]
                            )
                        ),


                        html.Td(
                            get_trade_structure(
                                row["Pair"],
                                row["Signal"]
                            )
                        ),


                        html.Td(
                            f"{float(row['Z-Score']):.2f}"
                        ),


                        html.Td(
                            f"{float(row['RSI']):.2f}"
                        ),


                        html.Td(
                            f"{float(row['MACD']):.4f}"
                        ),


                        html.Td(
                            f"{float(row['Ratio']):.4f}"
                        )

                    ],

                    style={
                        "color":"white"
                    }

                )

            )



        table = html.Table(

            [

                html.Tr(

                    [

                        html.Th("PAIR"),

                        html.Th("SIGNAL"),

                        html.Th("TRADE"),

                        html.Th("Z-SCORE"),

                        html.Th("RSI"),

                        html.Th("MACD"),

                        html.Th("RATIO")

                    ],

                    style={
                        "color":"white"
                    }

                )

            ] + rows,


            style={

                "width":"100%",

                "borderCollapse":"collapse"

            }

        )



        return (

            options,

            selected_pair,

            table,

            limit

        )



    # =========================
    # JUMP TO PAIR
    # =========================

    @app.callback(

        Output("stock1","value"),

        Output("stock2","value"),

        Input("pair_selector","value"),

        prevent_initial_call=True

    )


    def jump_pair(pair):

        if not pair or "/" not in pair:

            return (
                dash.no_update,
                dash.no_update
            )


        a, b = pair.split("/", 1)


        return a, b



    return panel
