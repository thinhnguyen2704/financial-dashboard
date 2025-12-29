import numpy as np


def backtest(df, initial_capital=10000):
    df = df.copy()
    df["position"] = df["signal"].shift(1).fillna(0)
    df["strategy_returns"] = df["position"] * df["Returns"]
    df["equity"] = initial_capital * (1 + df["strategy_returns"]).cumprod()
    return df


def calculate_performance_metrics(df):
    total_return = df["equity"].iloc[-1] / df["equity"].iloc[0] - 1
    annualized_return = (1 + total_return) ** (252 / len(df)) - 1
    daily_returns = df["strategy_returns"]
    annualized_volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (
        annualized_return / annualized_volatility
        if annualized_volatility != 0
        else np.nan
    )
    drawdown = df["equity"] / df["equity"].cummax() - 1
    max_drawdown = drawdown.min()
    return {
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
    }


def run_backtest(df, initial_capital=10000):
    backtested_df = backtest(df, initial_capital)
    performance_metrics = calculate_performance_metrics(backtested_df)
    return backtested_df, performance_metrics
