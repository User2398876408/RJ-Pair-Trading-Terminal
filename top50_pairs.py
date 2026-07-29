from itertools import combinations

from data_loader import StockLoader
from Config import DATA_FOLDER


loader = StockLoader(DATA_FOLDER)



# =========================
# IBOVESPA TOP 50 UNIVERSE
# =========================

TOP50_IBOV = [

    "PETR4",
    "VALE3",
    "ITUB4",
    "BBDC4",
    "BBAS3",
    "PETR3",
    "ABEV3",
    "ELET3",
    "BPAC11",
    "RENT3",

    "WEGE3",
    "SUZB3",
    "PRIO3",
    "B3SA3",
    "EQTL3",
    "RADL3",
    "RAIL3",
    "GGBR4",
    "LREN3",
    "JBSS3",

    "HAPV3",
    "CSNA3",
    "VIVT3",
    "TIMS3",
    "CMIG4",
    "SBSP3",
    "CPLE6",
    "TAEE11",
    "EMBR3",
    "KLBN11",

    "MULT3",
    "CYRE3",
    "TOTS3",
    "YDUQ3",
    "MRFG3",
    "BRFS3",
    "USIM5",
    "GOAU4",
    "CSAN3",
    "VAMO3",

    "ALPA4",
    "ASAI3",
    "AZUL4",
    "CCRO3",
    "CRFB3",
    "MGLU3",
    "PCAR3",
    "UGPA3",
    "NTCO3",
    "SOMA3"

]



# =========================
# VALIDATE DATA
# =========================

def get_valid_stocks():

    valid = []


    available_files = loader.list_tickers()


    for ticker in TOP50_IBOV:


        # File does not exist

        if ticker not in available_files:

            print(
                "Missing:",
                ticker
            )

            continue



        try:

            df = loader.load(
                ticker
            )


            # Needs enough history

            if len(df) < 50:

                print(
                    "Not enough data:",
                    ticker
                )

                continue



            valid.append(
                ticker
            )


        except Exception as e:


            print(
                "Bad file:",
                ticker,
                e
            )



    return valid



# =========================
# GENERATE PAIRS
# =========================

def generate_pairs():


    valid_stocks = get_valid_stocks()


    pairs = list(

        combinations(

            valid_stocks,

            2

        )

    )


    return pairs



# =========================
# TEST
# =========================

if __name__ == "__main__":


    valid = get_valid_stocks()


    pairs = generate_pairs()



    print()

    print(
        "Valid stocks:",
        len(valid)
    )


    print(
        "Generated pairs:",
        len(pairs)
    )


    print()


    print(
        pairs[:10]
    )
