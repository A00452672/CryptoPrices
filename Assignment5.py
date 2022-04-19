import requests
from pandas import DataFrame, to_datetime
import streamlit as st

#to run this app we need the above three libraries pip installed 
def fetchCoinPrices(currencyType: str, requiredDays: int, coin: str) -> DataFrame:
    outputFromApiCall = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={currencyType}'
                            f'&days={requiredDays}&interval=daily')
   # print(outputFromApiCall.json())
   # print(outputFromApiCall.json()['prices'])
    outputFromApiCall = outputFromApiCall.json()['prices'] #of the three values we got from response using only the prices field
    myDataFrame = DataFrame(outputFromApiCall, columns=['Date', currencyType]) #creating the fetched data as a dataframe for return value
    myDataFrame['Date'] = to_datetime(myDataFrame['Date'], unit='ms') #the date field is being created using to_datetime() and currently i/p is in milli seconds
    myDataFrame.set_index(myDataFrame.Date, inplace=True) #making the date field as index field
    myDataFrame.drop('Date', axis=1, inplace=True) #since additionally date is present unwantedly, we'll remove date column
    return myDataFrame


requiredDays = st.slider('Days', min_value=1, max_value=730, value=180)
coin = st.radio('Coins', ('cardano','bitcoin', 'ftx-token','theta-token'))
currencyType = st.radio('Currency', ('inr', 'usd', 'cad','aud'))
finaldata = fetchCoinPrices(currencyType, requiredDays, coin)
st.title(f"Crypto Coins and Prices in {currencyType}")
st.line_chart(finaldata[currencyType])
st.write(f'The Average price for {requiredDays}days is ', sum(finaldata[currencyType]) / requiredDays, f'{currencyType}')
