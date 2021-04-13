import cryptocompare
from datetime import datetime, timedelta
import datetime
import pandas as pd
from statistics import mean
from os import path
import matplotlib.pyplot as plt

application_path = path.dirname(__file__)

def get_current_dates():
    #Function that gets dates for the last 10 days and stores them in a list in ascending order.
    date_list = []
    todaydate = datetime.datetime.now()
    for i in range(10):
        date_list.append(todaydate - datetime.timedelta(days=i))
        date_list[i]=date_list[i].strftime('%d %b')
    date_list.reverse()
    return date_list

def get_crypto_prices(crypto_name):
    #Function that gets cryptocurrency prices for last 10 days and appends them to a list in ascending order.
    price_list = []
    for i in range(10):
        price_list.append(cryptocompare.get_historical_price(crypto_name, 'SGD', timestamp=datetime.datetime.now() - datetime.timedelta(days=i), exchange='CCCAGG'))
        price_list[i] = price_list[i][crypto_name]['SGD']
    price_list.reverse()
    return price_list

def compiler_transformer():
    #Gets all crypto prices and puts them in a dataframe.
    btc_prices = get_crypto_prices('BTC')
    eth_prices = get_crypto_prices('ETH')
    bnb_prices = get_crypto_prices('BNB')
    ltc_prices = get_crypto_prices('LTC')
    bch_prices = get_crypto_prices('BCH')
    last10days = get_current_dates()
    df = pd.DataFrame(btc_prices,index=last10days,columns=['Bitcoin'])
    df['Ethereum'] = eth_prices
    df['Binance Coin'] = bnb_prices
    df['LiteCoin'] = ltc_prices
    df['Bitcoin Cash'] = bch_prices
    return df

def aggregator():
    #Creates a dataframe with average, min, max prices of each type of crypto.
    btc_prices = get_crypto_prices('BTC')
    eth_prices = get_crypto_prices('ETH')
    bnb_prices = get_crypto_prices('BNB')
    ltc_prices = get_crypto_prices('LTC')
    bch_prices = get_crypto_prices('BCH')
    aggregate_terms = ['Average', 'Minimum', 'Maximum']
    btc_aggs = [mean(btc_prices), min(btc_prices), max(btc_prices)]
    eth_aggs = [mean(eth_prices), min(eth_prices), max(eth_prices)]
    bnb_aggs = [mean(bnb_prices), min(bnb_prices), max(bnb_prices)]
    ltc_aggs = [mean(ltc_prices), min(ltc_prices), max(ltc_prices)]
    bch_aggs = [mean(bch_prices), min(bch_prices), max(bch_prices)]
    df = pd.DataFrame(btc_aggs, index=aggregate_terms, columns=['Bitcoin'])
    df['Ethereum'] = eth_aggs
    df['Binance Coin'] = bnb_aggs
    df['LiteCoin'] = ltc_aggs
    df['Bitcoin Cash'] = bch_aggs
    return df

def concat_export():
    #Joins dataframe with prices and dataframe with summarized data together and exports as a .csv file.
    prices = compiler_transformer()
    aggregated_prices = aggregator()
    frames = [prices, aggregated_prices]
    result = pd.concat(frames)
    result.to_csv(path.join(application_path)+'.csv')

def plot_btc():
    #Plots a trend curve for bitcoin prices for the last 10 days and exports as .png file.
    btc_prices = get_crypto_prices('BTC')
    last10dates = get_current_dates()
    data = {'Date': last10dates, 'Prices': btc_prices}
    df = pd.DataFrame(data, columns=['Date', 'Prices'])
    plt.plot(df['Date'], df['Prices'], color='red', marker='o')
    plt.title('Bitcoin Prices', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Prices', fontsize=14)
    plt.grid(True)
    figure = plt.gcf()
    figure.set_size_inches(10,10)
    plt.savefig(path.join(application_path)+'bitcoin.png', bbox_inches = 'tight')
    plt.clf()

def plot_others():
    #Plots trend curves for other cryptocurrencies on the same graph for comparison, then exports as .png.
    eth_prices = get_crypto_prices('ETH')
    bnb_prices = get_crypto_prices('BNB')
    ltc_prices = get_crypto_prices('LTC')
    bch_prices = get_crypto_prices('BCH')
    last10dates = get_current_dates()
    df = pd.DataFrame({'Date': last10dates, 'eth': eth_prices, 'bnb': bnb_prices, 'ltc': ltc_prices, 'bch': bch_prices})
    plt.plot('Date', 'eth',data=df,marker='o',color='blue')
    plt.plot('Date', 'bnb', data=df, marker='o', color='red')
    plt.plot('Date', 'ltc', data=df, marker='o', color='yellow')
    plt.plot('Date', 'bch', data=df, marker='o', color='green')
    plt.title('Other Cryptocurrency Prices', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Prices', fontsize=14)
    plt.legend()
    plt.grid(True)
    figure = plt.gcf()
    figure.set_size_inches(10, 10)
    plt.savefig(path.join(application_path) + 'others.png', bbox_inches='tight')

get_prices_excel = concat_export()
btc_graph = plot_btc()
other_cryptos_graph = plot_others()

