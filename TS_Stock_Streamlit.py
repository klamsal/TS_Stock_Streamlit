import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
            st.write(f"Showing data for {user_ticker}")
            st.write(stock_data.tail())

            # Step 3: Dropdown to Select Forecast Method
            forecast_method = st.selectbox("Select Forecast Method:", ["Simple Moving Average", "Exponential Moving Average"])
            window_size = st.slider("Choose Window Size for Moving Average:", min_value=5, max_value=100, value=20)

            if forecast_method == "Simple Moving Average":
                # Calculate Simple Moving Average (SMA)
                stock_data["SMA"] = stock_data["Close"].rolling(window=window_size).mean()
                st.write(f"Simple Moving Average with Window Size {window_size}")
                st.line_chart(stock_data[["Close", "SMA"]])

            elif forecast_method == "Exponential Moving Average":
                # Calculate Exponential Moving Average (EMA)
                stock_data["EMA"] = stock_data["Close"].ewm(span=window_size, adjust=False).mean()
                st.write(f"Exponential Moving Average with Span {window_size}")
                st.line_chart(stock_data[["Close", "EMA"]])

            # Plotting the Chart
            fig, ax = plt.subplots()
            ax.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
            if forecast_method == "Simple Moving Average":
                ax.plot(stock_data.index, stock_data['SMA'], label='Simple Moving Average', color='orange')
            elif forecast_method == "Exponential Moving Average":
                ax.plot(stock_data.index, stock_data['EMA'], label='Exponential Moving Average', color='green')
            ax.set_title(f"{user_ticker} Stock Price with {forecast_method}")
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()
            st.pyplot(fig)
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please enter a valid ticker symbol to proceed.")
