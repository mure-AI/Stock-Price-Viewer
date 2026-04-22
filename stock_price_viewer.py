import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# ---------- TITLE ----------
st.title("📈 Stock Market Dashboard")

st.markdown("Analyze stock performance with interactive charts.")

# ---------- SIDEBAR (USER INPUTS) ----------
st.sidebar.header("User Input")

ticker_symbol = st.sidebar.text_input("Stock Ticker", "GOOGL")

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

if start_date > end_date:
    st.error(f"Start date must be before end date.")
else:
    tickerData = yf.Ticker("AAPL")
    tickerDf = tickerData.history(start=start_date, end=end_date)
    st.write(tickerDf)


# ---------- FETCH DATA ----------
def load_data(ticker, start, end):
    try:
        data = yf.Ticker(ticker)
        df = data.history(start=str(start), end=str(end))
        return df
    except:
        return None

df = load_data(ticker_symbol, start_date, end_date)

# ---------- ERROR HANDLING ----------
if df is None or df.empty:
    st.error("Invalid ticker or no data available. Try another symbol.")
else:
    # ---------- SHOW DATA ----------
    st.subheader(f"Data for {ticker_symbol.upper()}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Closing Price")
        st.line_chart(df["Close"])

    with col2:
        st.write("### Volume")
        st.line_chart(df["Volume"])

    # ---------- MOVING AVERAGE ----------
    st.write("### Moving Average (50-day)")
    df["MA50"] = df["Close"].rolling(window=50).mean()
    st.line_chart(df[["Close", "MA50"]])

    # ---------- RAW DATA ----------
    if st.checkbox("Show Raw Data"):
        st.write(df)