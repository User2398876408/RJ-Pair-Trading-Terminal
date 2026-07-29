from data_loader import StockLoader
from Config import DATA_FOLDER


loader = StockLoader(DATA_FOLDER)


for ticker in loader.list_tickers():

    try:

        df = loader.load(ticker)

        print(
            ticker,
            "OK",
            list(df.columns)
        )

    except Exception as e:

        print(
            ticker,
            "ERROR:",
            e
        )
