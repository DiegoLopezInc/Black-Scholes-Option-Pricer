import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from src.models.black_scholes import black_scholes, monte_carlo_option_price

def display_convergence_analysis(S, K, T, r, sigma, option_type, num_simulations=100000):
    """
    Display convergence analysis for Monte Carlo simulation

    Args:
        S: Current asset price
        K: Strike price
        T: Time to maturity
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        num_simulations: Number of Monte Carlo paths
    """
    st.subheader("Monte Carlo Convergence Analysis")

    with st.spinner('Running Monte Carlo simulation...'):
        # Run Monte Carlo with convergence tracking
        mc_price, convergence_data = monte_carlo_option_price(
            S, K, T, r, sigma, option_type, num_simulations, track_convergence=True
        )

        # Calculate Black-Scholes price for comparison
        bs_price = black_scholes(S, K, T, r, sigma, option_type)

    # Display prices
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Black-Scholes Price", f"${bs_price:.4f}")
    with col2:
        st.metric("Monte Carlo Price", f"${mc_price:.4f}")
    with col3:
        difference = abs(mc_price - bs_price)
        st.metric("Difference", f"${difference:.4f}",
                  delta=f"{(difference/bs_price)*100:.2f}%")

    # Create subplots for convergence visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Price Convergence to Black-Scholes',
            'Standard Error Reduction',
            '95% Confidence Interval',
            'Relative Error (%)'
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    iterations = convergence_data['iterations']
    prices = convergence_data['prices']
    std_errors = convergence_data['std_errors']
    ci_95 = convergence_data['confidence_intervals']

    # Plot 1: Price convergence
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=prices,
            mode='lines+markers',
            name='Monte Carlo Price',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=[bs_price] * len(iterations),
            mode='lines',
            name='Black-Scholes Price',
            line=dict(color='red', dash='dash', width=2)
        ),
        row=1, col=1
    )

    # Plot 2: Standard error
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=std_errors,
            mode='lines+markers',
            name='Std Error',
            line=dict(color='green', width=2),
            marker=dict(size=6),
            showlegend=False
        ),
        row=1, col=2
    )

    # Plot 3: Confidence interval
    upper_bound = [p + ci for p, ci in zip(prices, ci_95)]
    lower_bound = [p - ci for p, ci in zip(prices, ci_95)]

    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=upper_bound,
            mode='lines',
            name='Upper 95% CI',
            line=dict(color='lightblue', width=0),
            showlegend=False
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=lower_bound,
            mode='lines',
            name='Lower 95% CI',
            line=dict(color='lightblue', width=0),
            fill='tonexty',
            fillcolor='rgba(173, 216, 230, 0.3)',
            showlegend=False
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=prices,
            mode='lines+markers',
            name='Price',
            line=dict(color='blue', width=2),
            marker=dict(size=6),
            showlegend=False
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=[bs_price] * len(iterations),
            mode='lines',
            name='BS Price',
            line=dict(color='red', dash='dash', width=2),
            showlegend=False
        ),
        row=2, col=1
    )

    # Plot 4: Relative error
    relative_errors = [abs((p - bs_price) / bs_price) * 100 for p in prices]
    fig.add_trace(
        go.Scatter(
            x=iterations,
            y=relative_errors,
            mode='lines+markers',
            name='Relative Error',
            line=dict(color='orange', width=2),
            marker=dict(size=6),
            showlegend=False
        ),
        row=2, col=2
    )

    # Update x-axes to log scale for better visualization
    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=1)
    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=2)
    fig.update_xaxes(type="log", title_text="Iterations", row=2, col=1)
    fig.update_xaxes(type="log", title_text="Iterations", row=2, col=2)

    # Update y-axes
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Std Error ($)", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=2, col=1)
    fig.update_yaxes(title_text="Error (%)", row=2, col=2)

    # Update layout
    fig.update_layout(
        height=700,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title_text="Monte Carlo Convergence Analysis",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display convergence table
    with st.expander("View Detailed Convergence Data"):
        import pandas as pd

        df = pd.DataFrame({
            'Iterations': iterations,
            'MC Price': [f"${p:.6f}" for p in prices],
            'Std Error': [f"${se:.6f}" for se in std_errors],
            '95% CI': [f"±${ci:.6f}" for ci in ci_95],
            'Rel Error (%)': [f"{re:.4f}%" for re in relative_errors]
        })
        st.dataframe(df, use_container_width=True)

    return mc_price, bs_price, convergence_data
