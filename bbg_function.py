import urllib.parse
import requests
import pandas as pd

def last_price(ticker, timeframe = '1_MONTH', period ='daily'):
    possible_timeframe = ['1_MONTH', '6_MONTH', '1_YEAR', '5_YEAR']
    possible_period = ['daily', 'weekly', 'monthly']
    if timeframe not in possible_timeframe or period not in possible_period:
        return "Error: seleccionar un timeframe o period valido"
    else:
        query = urllib.parse.quote(ticker)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        params = {
            'timeframe':timeframe,
            'period':period,
            'volumePeriod': 'daily',
        }
        response = requests.get(f'https://www.bloomberg.com/markets2/api/history/{query}/PX_LAST', params=params, headers=headers)
        if not response.json():
            return "ticker invalido"
        else:
            volume = pd.DataFrame(response.json()[0]['volume']).set_index('dateTime').rename(columns={'value':f'VOL_{ticker}'})
            price = pd.DataFrame(response.json()[0]['price']).set_index('dateTime').rename(columns={'value':ticker})
            return pd.merge(price, volume, left_index=True, right_index=True)

def ohlc_price(ticker, timeframe = '1_MONTH', period ='daily'):
    possible_timeframe = ['1_MONTH', '6_MONTH', '1_YEAR', '5_YEAR']
    possible_period = ['daily', 'weekly', 'monthly']
    if timeframe not in possible_timeframe or period not in possible_period:
        return "Error: seleccionar un timeframe o period valido"
    else:
        query = urllib.parse.quote(ticker)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        params = {
            'timeframe':timeframe,
            'period':period,
            'volumePeriod': 'daily',
        }
        ticker_info = ['OPEN', 'HIGH','LOW','PX_LAST']
        df_data = []
        for info in ticker_info:
            response = requests.get(f'https://www.bloomberg.com/markets2/api/history/{query}/{info}', params=params, headers=headers)
            df_data.append(pd.DataFrame(response.json()[0]['price']).set_index('dateTime').rename(columns={'value':info}))
        df_data.append(pd.DataFrame(response.json()[0]['volume']).set_index('dateTime').rename(columns={'value':'VOLUME'}))
        return pd.concat(df_data, axis=1)
            