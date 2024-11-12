import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def download_and_clean_data(ticker, years=10):
    """
    Downloads stock data from yfinance for the specified number of years,
    cleans it, and converts it to a DataFrame.

    Args:
        ticker (str): The stock ticker symbol.
        years (int, optional): Number of years of data to download. Defaults to 10.

    Returns:
        pd.DataFrame: Cleaned DataFrame containing stock data with Date as index.
    """

    try:
        # Download data for the specified number of years
        data = yf.download(ticker, period=f"{years}y")

        # Only keep the 'Adj Close' column
        data = data[['Adj Close']]

        # Rename 'Adj Close' to 'Price'
        data = data.rename(columns={"Adj Close": "Price"})

        # Keep 'Date' as the index and convert it to datetime
        data.index = pd.to_datetime(data.index)

        return data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
st.title("Stock Price Viewer")

# User input for the ticker symbol
ticker_name = st.text_input("Enter the stock ticker symbol:")
years = st.slider("Select number of years of data to download:", 1, 20, 10)

if ticker_name:
    df = download_and_clean_data(ticker_name, years)

    # Plot the cleaned DataFrame
    if df is not None:
        st.line_chart(df['Price'], use_container_width=True)
        st.write(df)
    else:
        st.write("No data available for the given ticker symbol.")
