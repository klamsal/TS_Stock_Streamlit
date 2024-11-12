import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Stock Price Forecasting App")

# Step 1: User Inputs Ticker
st.sidebar.header("Input")
user_ticker = st.sidebar.text_input("Enter the Stock Ticker:", "AAPL")

if user_ticker:
    try:
        # Step 2: Download Last 10 Years Data from yfinance
        stock_data = yf.download(user_ticker, period="10y")  # Changed from "20y" to "10y"
        if stock_data.empty:
            st.write("No data available for the provided ticker. Please enter a valid ticker symbol.")
        else:
            # Step 3: Data Cleanup
            stock_data = stock_data.loc[:, ~stock_data.columns.duplicated()]  # Remove duplicate columns if any
            stock_data.reset_index(inplace=True)
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Convert Date to datetime
            stock_data.set_index('Date', inplace=True)
            stock_data = stock_data[['Adj Close']]  # Use 'Adj Close' for plotting
            stock_data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
            stock_data.dropna(inplace=True)  # Remove any rows with missing values
            stock_data = stock_data[~stock_data.index.duplicated(keep='first')]  # Remove duplicate indices
            
            st.write(f"Showing data for {user_ticker}")
            st.write(stock_data.tail())

            # Plotting the Adjusted Close Price
            st.line_chart(stock_data['Adj_Close'])

            # Plotting the Chart using Matplotlib
            fig, ax = plt.subplots()
            ax.plot(stock_data.index, stock_data['Adj_Close'], label='Adjusted Close Price', color='blue')
            ax.set_title(f"{user_ticker} Stock Price - Adjusted Close")
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()
            st.pyplot(fig)
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please enter a valid ticker symbol to proceed.")
