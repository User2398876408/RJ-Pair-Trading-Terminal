from data_loader import StockLoader
from Config import DATA_FOLDER
from Indicators import add_indicators
from Charts import candlestick

loader = StockLoader(DATA_FOLDER)

df = loader.load("AAPL")

df = add_indicators(df)

fig = candlestick(df)

fig.show()
