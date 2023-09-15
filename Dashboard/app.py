import matplotlib.pyplot as plt
from pandas_datareader import DataReader
import yfinance as yf
from keras.models import load_model
import streamlit as st

st.title('Analysing stocks')

# Create a Streamlit layout with two columns
col1, col2 = st.columns(2)

# In the first column, place the "Start" text input
start = col1.text_input('Start Date', '2023-06-15')

# In the second column, place the "End" text input
end = col2.text_input('End Date', '2023-09-08')

user_input = st.text_input('Enter a Stock Ticker','TSLA')
df = yf.download(user_input, start=start, end=end)
df

st.subheader('Open price values')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(df['Open'])
plt.xlabel('Date')
plt.ylabel('Open price')
st.pyplot(fig2)

st.subheader('Close price values')
fig1 = plt.figure(figsize=(12, 6))
plt.plot(df['Close'])
plt.xlabel('Date')
plt.ylabel('Close price')
st.pyplot(fig1)


st.title('Comparing closing prices of stocks')


col3, col4 = st.columns(2)

user_input1 = col3.text_input('Enter a Stock Ticker','AMZN')
df1 = yf.download(user_input1, start=start, end=end)

user_input2 = col4.text_input('Enter a Stock Ticker','APPL')
df2 = yf.download(user_input2, start=start, end=end)


st.subheader('Close price values')
fig3 = plt.figure(figsize=(12, 6))
plt.plot(df1['Close'])
plt.plot(df2['Close'])
plt.legend([user_input1,user_input2])
plt.xlabel('Date')
plt.ylabel('Close price')

st.pyplot(fig3)
