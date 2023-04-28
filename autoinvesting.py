import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("S&P500-365.csv")
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
df['Close'] = df['Close'].str.replace(',', '').astype(float)

def SMA(data, period=30, column='Close'):
    """
    generates the mean values over a 30 day period

    Args:
        data (dataframe): dataframe containing the close prices
        period (int, optional): period in which to evaluate the mean. Defaults to 30.
        column (str, optional): Column to evaluate against. Defaults to 'Close'.

    Returns:
        dataframe: column data
    """
    return data[column].rolling(window=period).mean()

df['SMA30'] = SMA(df)

def strat(df):
    """
    evaluates if the 30 day rolling average is above or below market value

    Args:
        df (dataframe): dataframe for s&p500 data

    Returns:
        tuple: contains buy and sell lists
    """
    buy = []
    sell = []
    flag = 0
    buy_price = 0
    
    for i in range(0, len(df)):
        if df['SMA30'][i] < df['Close'][i] and flag == 0:
            buy.append(df['Close'][i])
            sell.append(np.nan)
            buy_price = df['Close'][i]
            flag = 1
        elif df['SMA30'][i] > df['Close'][i] and flag == 1 and buy_price < df['Close'][i]:
            sell.append(df['Close'][i])
            buy.append(np.nan)
            buy_price = 0
            flag = 0
        else: 
            sell.append(np.nan)
            buy.append(np.nan)
    return (buy, sell)

stratdata = strat(df)
df['Buy'] = stratdata[0]
df['Sell'] = stratdata[1]

print(df)
plt.title('close with buy and sell')
plt.plot(df['Close'], alpha = 0.5, color='blue', label = 'Close')
plt.plot(df['SMA30'], alpha = 0.5,color='black', label = 'SMA30')
plt.scatter(df.index, df['Buy'], color='green', label='BuySignal', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', label='SellSignal', marker='v', alpha=1)
plt.show()
            
    



