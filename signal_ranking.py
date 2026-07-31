import pandas as pd



def generate_stock_ranking(pair_signals):

    stock_scores = {}



    for _, row in pair_signals.iterrows():

        try:

            stock1, stock2 = row["Pair"].split("/", 1)

            z = abs(float(row["Z-Score"]))

            signal = row["Signal"]



            if signal == "LONG FIRST / SHORT SECOND":


                # stock1 is bullish

                stock_scores[stock1] = (
                    stock_scores.get(stock1, 0)
                    + z
                )


                # stock2 is bearish

                stock_scores[stock2] = (
                    stock_scores.get(stock2, 0)
                    - z
                )



            elif signal == "SHORT FIRST / LONG SECOND":


                # stock1 is bearish

                stock_scores[stock1] = (
                    stock_scores.get(stock1, 0)
                    - z
                )


                # stock2 is bullish

                stock_scores[stock2] = (
                    stock_scores.get(stock2, 0)
                    + z
                )



        except Exception:

            continue



    ranking = pd.DataFrame(

        list(stock_scores.items()),

        columns=[

            "Stock",

            "Score"

        ]

    )



    ranking["Signal"] = ranking["Score"].apply(

        lambda x:

        "Strong Buy" if x >= 5

        else "Buy" if x >= 2

        else "Strong Sell" if x <= -5

        else "Sell" if x <= -2

        else "Neutral"

    )



    return ranking.sort_values(

        "Score",

        ascending=False

    ).reset_index(drop=True)
