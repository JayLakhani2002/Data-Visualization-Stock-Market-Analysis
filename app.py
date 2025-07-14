import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout="wide")
st.title("📈 Stock Market Analysis Dashboard – 2023")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/2023_Global_Markets_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by=["Ticker", "Date"], inplace=True)
    df["Year"] = df["Date"].dt.year
    df["Return"] = df.groupby("Ticker")["Adj Close"].pct_change() * 100
    df.dropna(subset=["Return"], inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
tickers = sorted(df["Ticker"].unique())
selected_tickers = st.sidebar.multiselect("Select Tickers", tickers, default=tickers[:5])

df_filtered = df[df["Ticker"].isin(selected_tickers)]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Adjusted Price Trend", 
    "📈 Daily Return Distribution", 
    "📉 Annual Return", 
    "⚡ Volatility"
])

# Adjusted Price Trend
with tab1:
    st.subheader("Adjusted Close Price Over Time")
    for ticker in selected_tickers:
        st.line_chart(df_filtered[df_filtered["Ticker"] == ticker][["Date", "Adj Close"]].set_index("Date"))

# Daily Return Distribution
with tab2:
    st.subheader("Daily Return Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df_filtered["Return"], bins=50, kde=True, ax=ax)
    ax.set_title("Distribution of Daily Returns (All Selected Tickers)")
    ax.set_xlabel("Return (%)")
    st.pyplot(fig)

# Annual Return
with tab3:
    st.subheader("Annual Return by Ticker")
    annual_return = df_filtered.groupby("Ticker").apply(
        lambda x: (x["Adj Close"].iloc[-1] - x["Adj Close"].iloc[0]) / x["Adj Close"].iloc[0] * 100
    ).reset_index(name="Annual Return (%)")

    fig2, ax2 = plt.subplots()
    sns.barplot(data=annual_return, x="Ticker", y="Annual Return (%)", ax=ax2)
    ax2.set_title("Annual Return (2023)")
    st.pyplot(fig2)

# Volatility
with tab4:
    st.subheader("Volatility by Ticker")
    volatility = df_filtered.groupby("Ticker")["Return"].std().reset_index(name="Volatility")

    fig3, ax3 = plt.subplots()
    sns.barplot(data=volatility, x="Ticker", y="Volatility", ax=ax3)
    ax3.set_title("Volatility (Standard Deviation of Daily Return)")
    st.pyplot(fig3)
