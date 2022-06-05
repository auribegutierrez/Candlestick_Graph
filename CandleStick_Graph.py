"""
Name: Andrea Uribe
Course: ICT-4370 Python Programming
Date: 06/05/2022
Description: This program will create a candlestick graph using matplotlib fincance library. It will use the 
Open, Close, High and Low informaiton to determine gain and loss for the stock of each date. It also has the 
volume at the bottom showing also gain and loss through the different dates.
"""

import os
from symtable import Symbol
import pandas as pd
import io
import tkinter as tk
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mpl_dates
import mplfinance as mpf

try:
    # Read the json as a pandas data frame
    stocks_df = pd.read_json('/Users/andreauribe/Desktop/AllStocks.json')

    # Use the date column as index and convert to the type that Matplotlib wants
    stocks_df.index = pd.DatetimeIndex(stocks_df['Date'])

    # Remove all data points where one of the values is not known.
    stocks_df = stocks_df[(stocks_df["Open"] != "-") &
                        (stocks_df["Close"] != "-") &
                        (stocks_df["High"] != "-") &
                        (stocks_df["Low"] != "-")]

    # Convert values from string to float
    stocks_df = stocks_df.astype({'Open': 'float',
                                'Close': 'float',
                                'High': 'float',
                                'Low': 'float'})

    # Get a list of all distinct symbols
    stock_symbols = stocks_df["Symbol"].unique()


    # Class that helps to create graphs.
    class StockHistory:
        def __init__(self, symbol, df):
            self.symbol = symbol
            self.df = df

        def candlestick_graph(self, filename):
            # Use mplfinance to plot the stock data frame
            mpf.plot(self.df,
                    volume=True,
                    type='candle',
                    style="yahoo",
                    title=self.symbol,
                    savefig=filename)

except FileNotFoundError as error:
    print ("Error: inability to read from the input file")

except io.UnsupportedOperation as error:
    print ("Error: Unable to write on file")

except ValueError as error:
    print ("Error: Wront data types entered")
    

try:
    graphs_dir = "graphs"
    os.mkdir(graphs_dir)

    # For each symbol, create a class and generate the graph.
    for symbol in stock_symbols:
        stock_df = stocks_df[stocks_df["Symbol"] == symbol]
        stock_history = StockHistory(symbol=symbol, df=stock_df)
        graph_dir = graphs_dir + "/" + symbol + "_candlestick.png"
        stock_history.candlestick_graph(filename=graph_dir)

except FileExistsError as e:
    print("The graphs folder already exists, the graphs would be replaced.")
