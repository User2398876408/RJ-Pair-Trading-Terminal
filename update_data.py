import yfinance as yf
from pathlib import Path

from Config import DATA_FOLDER
from top50_pairs import TOP50_IBOV


folder = Path(DATA_FOLDER)

folder.mkdir(
    exist_ok=True
)


# Yahoo ticker corrections
TICKER_MAP = {

    "ELET3": "ELET6.SA"

}



for ticker in TOP50_IBOV:


    yf_ticker = TICKER_MAP.get(

        ticker,

        ticker + ".SA"

    )


    print(
        "Updating",
        yf_ticker
    )


    try:

        df = yf.download(

            yf_ticker,

            period="5y",

            auto_adjust=False,

            progress=False

        )


        if df.empty:

            print(
                "SKIPPED:",
                yf_ticker,
                "No data found"
            )

            continue



        # Remove Yahoo multi-index
        if hasattr(df.columns, "levels"):

            df.columns = df.columns.get_level_values(0)



        # Move Date from index to column
        df.reset_index(
            inplace=True
        )



        required_columns = [

            "Date",
            "Adj Close",
            "Close",
            "High",
            "Low",
            "Open",
            "Volume"

        ]



        missing = [

            col for col in required_columns

            if col not in df.columns

        ]



        if missing:

            print(
                "SKIPPED:",
                yf_ticker,
                "Missing:",
                missing
            )

            continue



        df = df[

            required_columns

        ]



        df.to_csv(

            folder / f"{ticker}.csv",

            index=False

        )


        print(
            "Saved:",
            ticker
        )


    except Exception as e:


        print(

            "ERROR:",

            ticker,

            e

        )



print(
    "\nUpdate complete"
)
