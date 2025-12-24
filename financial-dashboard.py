import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import date

# ======================================================
# Page Configuration
# ======================================================
st.set_page_config(
    page_title="Advanced Financial Dashboard",
    layout="wide"
)

st.title("Advanced Financial Data Dashboard")

# ======================================================
# Sidebar
# ======================================================
st.sidebar.header("Settings")

tickers = st.sidebar.text_input(
    "Tickers (comma-separated)",
    value="AAPL,MSFT,GOOGL"
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2023, 1, 1)
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today()
)

ma_windows = st.sidebar.multiselect(
    "Moving Averages",
    options=[10, 20, 50, 100, 200],
    default=[20, 50]
)

show_bollinger = st.sidebar.checkbox("Bollinger Bands", True)
show_volume = st.sidebar.checkbox("Volume", True)
show_rsi = st.sidebar.checkbox("RSI", True)
show_macd = st.sidebar.checkbox("MACD", True)
show_candles = st.sidebar.checkbox("Candlestick Chart", True)

# ======================================================
# Cached Data Loader
# ======================================================
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        group_by="column",
        auto_adjust=False,
        progress=False
    )

    # Handle MultiIndex columns defensively
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.dropna(inplace=True)

    return df

# ======================================================
# Indicators
# ======================================================
def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(period).mean() / loss.rolling(period).mean()
    return 100 - (100 / (1 + rs))

def macd(series):
    ema12 = series.ewm(span=12).mean()
    ema26 = series.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9).mean()
    return macd_line, signal

# ======================================================
# Data Processing
# ======================================================
ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
data = {}

for ticker in ticker_list:
    df = load_data(ticker, start_date, end_date)

    for w in ma_windows:
        df[f"MA_{w}"] = df["Close"].rolling(w).mean()

    if show_bollinger:
        df["BB_MID"] = df["Close"].rolling(20).mean()
        df["BB_UPPER"] = df["BB_MID"] + 2 * df["Close"].rolling(20).std()
        df["BB_LOWER"] = df["BB_MID"] - 2 * df["Close"].rolling(20).std()

    if show_rsi:
        df["RSI"] = rsi(df["Close"])

    if show_macd:
        df["MACD"], df["MACD_SIGNAL"] = macd(df["Close"])

    df["Returns"] = df["Close"].pct_change()

    data[ticker] = df

# ======================================================
# Price Chart
# ======================================================
price_fig = go.Figure()

for ticker, df in data.items():
    if show_candles:
        price_fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name=f"{ticker} Candles"
            )
        )
    else:
        price_fig.add_trace(
            go.Scatter(x=df.index, y=df["Close"], name=f"{ticker} Close")
        )

    for w in ma_windows:
        price_fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f"MA_{w}"],
                name=f"{ticker} MA {w}",
                line=dict(dash="dot")
            )
        )

    if show_bollinger:
        price_fig.add_trace(go.Scatter(x=df.index, y=df["BB_UPPER"], name=f"{ticker} BB Upper", line=dict(width=1)))
        price_fig.add_trace(go.Scatter(x=df.index, y=df["BB_LOWER"], name=f"{ticker} BB Lower", line=dict(width=1)))

price_fig.update_layout(title="Price Analysis")
st.plotly_chart(price_fig, use_container_width=True)

# ======================================================
# Volume
# ======================================================
if show_volume:
    vol_fig = go.Figure()
    for ticker, df in data.items():
        vol_fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name=ticker))
    vol_fig.update_layout(title="Volume")
    st.plotly_chart(vol_fig, use_container_width=True)

# ======================================================
# RSI
# ======================================================
if show_rsi:
    rsi_fig = go.Figure()
    for ticker, df in data.items():
        rsi_fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name=ticker))
    rsi_fig.update_layout(title="RSI", yaxis=dict(range=[0, 100]))
    st.plotly_chart(rsi_fig, use_container_width=True)

# ======================================================
# MACD
# ======================================================
if show_macd:
    macd_fig = go.Figure()
    for ticker, df in data.items():
        macd_fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name=f"{ticker} MACD"))
        macd_fig.add_trace(go.Scatter(x=df.index, y=df["MACD_SIGNAL"], name=f"{ticker} Signal"))
    macd_fig.update_layout(title="MACD")
    st.plotly_chart(macd_fig, use_container_width=True)

# ======================================================
# Portfolio Performance
# ======================================================
st.header("Portfolio Performance")

returns_df = pd.concat(
    {t: d["Returns"] for t, d in data.items()},
    axis=1
).dropna()

portfolio_returns = returns_df.mean(axis=1)
cumulative = (1 + portfolio_returns).cumprod()

port_fig = go.Figure()
port_fig.add_trace(go.Scatter(x=cumulative.index, y=cumulative, name="Portfolio"))
port_fig.update_layout(title="Cumulative Portfolio Return")
st.plotly_chart(port_fig, use_container_width=True)

# ======================================================
# Correlation Matrix
# ======================================================
st.header("Correlation Matrix")

corr = returns_df.corr()
corr_fig = px.imshow(corr, text_auto=True, title="Return Correlations")
st.plotly_chart(corr_fig, use_container_width=True)

# ======================================================
# Data Export
# ======================================================
st.header("Export Data")

selected = st.selectbox("Select Ticker", ticker_list)
csv = data[selected].to_csv().encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    f"{selected}_data.csv",
    "text/csv"
)

html = price_fig.to_html().encode("utf-8")
st.download_button(
    "Download Price Chart (HTML)",
    html,
    "price_chart.html",
    "text/html"
)
