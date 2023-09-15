import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import DataReader
import yfinance as yf
from keras.models import load_model
import streamlit as st
import datetime

# Define CSS styles
st.markdown(
    """
    <style>
    .title {
        font-size: 24px;
        text-align: center;
    }
    .subheader {
        font-size: 20px;
        text-align: center;
    }
    table {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Finding the outliers')

model = load_model('my_model.keras')

colx, coly = st.columns(2)
start = colx.text_input('Start Date')
end = coly.text_input('End Date')

st.subheader('Stocks')
tickers = []

col1, col2, col3, col4, col5 = st.columns(5)

ticker_symbol_1 = col1.text_input('Stock :','AMZN')
tickers.append(ticker_symbol_1)
ticker_symbol_2 = col2.text_input('Stock :','META')
tickers.append(ticker_symbol_2)
ticker_symbol_3 = col3.text_input('Stock :','MSFT')
tickers.append(ticker_symbol_3)
ticker_symbol_4 = col4.text_input('Stock :','TSLA')
tickers.append(ticker_symbol_4)
ticker_symbol_5 = col5.text_input('Stock :','GOOG')
tickers.append(ticker_symbol_5)

# Calculate the previous 3 days
# start = '2023-01-01'
# end = '2023-01-10'

data_list = []
dates_list = []
predicted_prices = []
previous_prices = []
percentages = []
close_data = []
abs_percentages = []

for ticker in tickers:
    st.subheader(ticker)
    data = yf.download(ticker, start=start, end=end)
    data
    close_values = data['Close'].values
    close_data.append(close_values)

    # Extract the 'Close' values as a NumPy array
    dates = data.index
    date = dates[3]
    close_vals = data['Close'][-3:].to_numpy()
    close_vals
    close_vals_c = np.reshape(close_vals, (1, 3, 1))
    test_predictions_close_vals = model.predict(close_vals_c)
    
    predicted_price = round(test_predictions_close_vals[0][0], 2)
    predicted_prices.append(predicted_price)
    previous_price = round(data['Close'][-1], 2)
    previous_prices.append(previous_price)

    # st.write(f"The predicted price for {date} is {predicted_price}")
    # st.write(f"The actual price for {date} is {actual_price}")


    percentage = round(((predicted_price - data['Close'][-1]) / data['Close'][-1]) * 100, 2)
    percentages.append(percentage)
    abs_percentages.append(abs(percentage))

    # st.write(f"The percentage of close value change is {percentage}%")

    data_list.append(data)
    
# Create a DataFrame to display results
results_data = {
    'Ticker': tickers,
    'Previous day Value': previous_prices,
    'Predicted Value': predicted_prices,
    'Percentage of change': percentages
}

results_df = pd.DataFrame(results_data)

# Display the results table
st.subheader('Results')
st.table(results_df)

max_value = max(abs_percentages)
max_index = abs_percentages.index(max_value)

st.subheader('Outlier Stock')
st.write(f"The outlier stock : {tickers[max_index]} ")

st.subheader('Close price values')
fig = plt.figure(figsize=(12, 6))
plt.plot(close_data[0])
plt.plot(close_data[1])
plt.plot(close_data[2])
plt.plot(close_data[3])
plt.plot(close_data[4])
plt.legend([tickers[0],tickers[1],tickers[2],tickers[3],tickers[4]])
plt.xlabel('Date')
plt.ylabel('Close price')
st.pyplot(fig)

