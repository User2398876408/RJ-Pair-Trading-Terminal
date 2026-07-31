from data_loader import StockLoader
from Config import DATA_FOLDER
from Indicators import add_indicators

loader = StockLoader(DATA_FOLDER)

df = loader.load("AAPL")

df = add_indicators(df)

print(df.tail())
print(df.columns)
