"""
Quant Trading Strategy: Feature Engineering, Backtesting & Visualization
Author: Hir Shah

Pipeline: Raw OHLCV Data → Feature Engineering → Signal Model → Backtest → Visualization

Dependencies: pip install yfinance pandas numpy matplotlib
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")


TICKER     = "SPY"        
START_DATE = "2018-01-01"
END_DATE   = "2024-12-31"
INITIAL_CAPITAL = 10_000  


def fetch_data(ticker, start, end):
    """Download OHLCV data from Yahoo Finance."""
    print(f"Fetching data for {ticker}...")
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.dropna(inplace=True)
    print(f"  Loaded {len(df)} trading days ({start} to {end})\n")
    return df


def add_features(df):
    """
    Build technical indicators used as signals:
    - SMA (trend)
    - RSI (momentum / mean reversion)
    - MACD (trend + momentum)
    - Volatility (risk filter)
    """
    close = df["Close"]

    df["SMA_20"]  = close.rolling(20).mean()
    df["SMA_50"]  = close.rolling(50).mean()
    df["SMA_200"] = close.rolling(200).mean()

    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    ema_12        = close.ewm(span=12, adjust=False).mean()
    ema_26        = close.ewm(span=26, adjust=False).mean()
    df["MACD"]        = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"]   = df["MACD"] - df["MACD_Signal"]

    df["Returns"]    = close.pct_change()
    df["Volatility"] = df["Returns"].rolling(20).std()

    df.dropna(inplace=True)
    print(f"Features engineered. Shape: {df.shape}\n")
    return df


def generate_signals(df):
    """
    Blend three sub-signals into one composite score.
    Each component is normalized to [-1, +1]:

    Trend Signal    → SMA cross (price vs SMA_50)
    Momentum Signal → RSI (overbought/oversold)
    MACD Signal     → MACD histogram direction

    Weights sum to 1.0. Adjust to test different strategies.
    """
    WEIGHT_TREND    = 0.50
    WEIGHT_MOMENTUM = 0.30
    WEIGHT_MACD     = 0.20

    trend_signal = np.where(df["Close"] > df["SMA_50"], 1, -1)

    rsi = df["RSI"]
    momentum_signal = np.where(rsi < 30, 1,
                      np.where(rsi > 70, -1, 0))

    macd_signal = np.sign(df["MACD_Hist"])

    df["Signal_Score"] = (
        WEIGHT_TREND    * trend_signal +
        WEIGHT_MOMENTUM * momentum_signal +
        WEIGHT_MACD     * macd_signal
    )

    df["Position"] = np.where(df["Signal_Score"] > 0.2, 1, 0)

    print("Signals generated.")
    print(f"  Days in market : {df['Position'].sum()} / {len(df)}")
    print(f"  Market exposure: {df['Position'].mean():.1%}\n")
    return df


def backtest(df, initial_capital=INITIAL_CAPITAL):
    """
    Simulate strategy returns.
    Position is shifted by 1 day to avoid look-ahead bias
    (we can only trade on tomorrow's open using today's signal).
    """
    # Shift position by 1: today's signal → tomorrow's trade
    df["Strategy_Returns"] = df["Returns"] * df["Position"].shift(1)
    df["Buy_Hold_Returns"]  = df["Returns"]

    df["Strategy_Equity"]  = initial_capital * (1 + df["Strategy_Returns"]).cumprod()
    df["Buy_Hold_Equity"]  = initial_capital * (1 + df["Buy_Hold_Returns"]).cumprod()

    df.dropna(inplace=True)
    return df


def compute_metrics(df, label="Strategy"):
    """Calculate Sharpe, CAGR, Max Drawdown."""
    eq_col  = "Strategy_Equity" if label == "Strategy" else "Buy_Hold_Equity"
    ret_col = "Strategy_Returns" if label == "Strategy" else "Buy_Hold_Returns"

    equity  = df[eq_col]
    returns = df[ret_col].dropna()

    n_years = len(df) / 252
    cagr    = (equity.iloc[-1] / INITIAL_CAPITAL) ** (1 / n_years) - 1

    sharpe  = (returns.mean() / returns.std()) * np.sqrt(252)

    rolling_max = equity.cummax()
    drawdown    = (equity - rolling_max) / rolling_max
    max_dd      = drawdown.min()

    total_return = (equity.iloc[-1] - INITIAL_CAPITAL) / INITIAL_CAPITAL

    return {
        "Label"        : label,
        "Final Value"  : f"${equity.iloc[-1]:,.0f}",
        "Total Return" : f"{total_return:.1%}",
        "CAGR"         : f"{cagr:.1%}",
        "Sharpe Ratio" : f"{sharpe:.2f}",
        "Max Drawdown" : f"{max_dd:.1%}",
    }


def print_metrics(strategy_metrics, benchmark_metrics):
    print("=" * 45)
    print(f"{'PERFORMANCE SUMMARY':^45}")
    print("=" * 45)
    keys = list(strategy_metrics.keys())[1:]  # skip "Label"
    header = f"{'Metric':<18} {'Strategy':>12} {'Buy & Hold':>12}"
    print(header)
    print("-" * 45)
    for k in keys:
        print(f"{k:<18} {strategy_metrics[k]:>12} {benchmark_metrics[k]:>12}")
    print("=" * 45)


def plot_results(df, ticker):
    """4-panel dashboard: price + signals, RSI, MACD, equity curve."""
    fig = plt.figure(figsize=(14, 12))
    fig.suptitle(f"Quant Trading Strategy — {ticker}", fontsize=15, fontweight="bold", y=0.98)
    gs  = gridspec.GridSpec(4, 1, height_ratios=[2.5, 1, 1, 2], hspace=0.4)

    C_BUY    = "#26a69a"
    C_SELL   = "#ef5350"
    C_STRAT  = "#1565C0"
    C_BH     = "#9E9E9E"
    C_PRICE  = "#212121"

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df.index, df["Close"],   color=C_PRICE, lw=1.2, label="Price")
    ax1.plot(df.index, df["SMA_20"],  color="#FB8C00", lw=0.9, linestyle="--", label="SMA 20")
    ax1.plot(df.index, df["SMA_50"],  color="#8E24AA", lw=0.9, linestyle="--", label="SMA 50")
    ax1.plot(df.index, df["SMA_200"], color="#E53935", lw=0.9, linestyle="--", label="SMA 200")

    entries = df[df["Position"].diff() == 1]
    exits   = df[df["Position"].diff() == -1]
    ax1.scatter(entries.index, entries["Close"], marker="^", color=C_BUY,  s=60, zorder=5, label="Entry")
    ax1.scatter(exits.index,   exits["Close"],   marker="v", color=C_SELL, s=60, zorder=5, label="Exit")

    ax1.set_ylabel("Price ($)")
    ax1.legend(loc="upper left", fontsize=7, ncol=3)
    ax1.set_title("Price Action with Moving Averages & Trade Signals", fontsize=10)
    ax1.grid(alpha=0.3)

    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(df.index, df["RSI"], color="#7B1FA2", lw=1)
    ax2.axhline(70, color=C_SELL, linestyle="--", lw=0.8, alpha=0.7)
    ax2.axhline(30, color=C_BUY,  linestyle="--", lw=0.8, alpha=0.7)
    ax2.fill_between(df.index, 30, 70, alpha=0.05, color="gray")
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.set_title("RSI (14)", fontsize=9)
    ax2.grid(alpha=0.3)

    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(df.index, df["MACD"],        color="#1565C0", lw=1,   label="MACD")
    ax3.plot(df.index, df["MACD_Signal"], color="#E53935", lw=0.8, label="Signal")
    colors = [C_BUY if v >= 0 else C_SELL for v in df["MACD_Hist"]]
    ax3.bar(df.index, df["MACD_Hist"], color=colors, alpha=0.6, width=1, label="Histogram")
    ax3.axhline(0, color="black", lw=0.5)
    ax3.set_ylabel("MACD")
    ax3.legend(loc="upper left", fontsize=7)
    ax3.set_title("MACD (12, 26, 9)", fontsize=9)
    ax3.grid(alpha=0.3)

    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    ax4.plot(df.index, df["Strategy_Equity"], color=C_STRAT, lw=1.5, label="Strategy")
    ax4.plot(df.index, df["Buy_Hold_Equity"], color=C_BH,    lw=1.2, linestyle="--", label="Buy & Hold")
    ax4.fill_between(df.index, df["Strategy_Equity"], df["Buy_Hold_Equity"],
                     where=df["Strategy_Equity"] >= df["Buy_Hold_Equity"],
                     alpha=0.1, color=C_BUY,  interpolate=True)
    ax4.fill_between(df.index, df["Strategy_Equity"], df["Buy_Hold_Equity"],
                     where=df["Strategy_Equity"] <  df["Buy_Hold_Equity"],
                     alpha=0.1, color=C_SELL, interpolate=True)
    ax4.set_ylabel("Portfolio Value ($)")
    ax4.set_xlabel("Date")
    ax4.legend(loc="upper left", fontsize=8)
    ax4.set_title("Equity Curve: Strategy vs Buy & Hold", fontsize=9)
    ax4.grid(alpha=0.3)

    plt.savefig("quant_strategy_results.png", dpi=150, bbox_inches="tight")
    print("\nChart saved: quant_strategy_results.png")
    plt.show()


if __name__ == "__main__":
    df = fetch_data(TICKER, START_DATE, END_DATE)

    df = add_features(df)

    df = generate_signals(df)

    df = backtest(df)

    strat_metrics = compute_metrics(df, label="Strategy")
    bh_metrics    = compute_metrics(df, label="Buy & Hold")
    print_metrics(strat_metrics, bh_metrics)

    plot_results(df, TICKER)