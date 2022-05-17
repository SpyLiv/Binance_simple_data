#config
apikey = 'Your API KEY'
secret = 'Your Secret API'


from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import mplfinance as mpf

#Auth
client = Client(apikey, secret)

#ticket data
tickers = client.get_all_tickers()
##print(tickers)

#dataframe
ticker_df = pd.DataFrame(tickers)
print(ticker_df.head())
print(ticker_df.tail())

#easy search
ticker_df.set_index('symbol', inplace=True)
print (float(ticker_df.loc['BNBBTC']['price']))

#market depth
depth = client.get_order_book(symbol='BTCUSDT')
##print (depth)
depth_df = pd.DataFrame(depth['asks'])
depth_df.columns = ['Price', 'Volume']
print(depth_df.head())
print(depth_df.dtypes)

#historical data for a pair
historical = client.get_historical_klines('ETHBTC', Client.KLINE_INTERVAL_1DAY, '14 Jan 2021')
##print (historical)
#  [
#   [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore.
#   ]
# ]

#historical dataframe
hist_df = pd.DataFrame(historical)
print (hist_df.head())
hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
print (hist_df.tail())
print (hist_df.dtypes)


#data proccess
hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')
print (hist_df.head())
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
print(hist_df.tail())
print(hist_df.describe())
print(hist_df.info())

#visualization
hist_df.set_index('Close Time').tail(100)
mpf.plot(hist_df.set_index('Close Time').tail(240), 
        type='candle', style='charles', 
        volume=True, 
        title='ETHBTC Last 240 Days', 
        mav=(10,20,30))