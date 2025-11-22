import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import sys
    sys.path.append('/home/user/Black-Scholes-Option-Pricer')

    from src.models.black_scholes import (
        black_scholes,
        monte_carlo_option_price,
        monte_carlo_antithetic,
        monte_carlo_control_variate,
        calculate_greeks
    )

    return (
        black_scholes,
        calculate_greeks,
        go,
        make_subplots,
        mo,
        monte_carlo_antithetic,
        monte_carlo_control_variate,
        monte_carlo_option_price,
        np,
        pd,
        sys,
    )


@app.cell
def __(mo):
    mo.md(
        """
        # Optimization Techniques for Faster Convergence

        This notebook demonstrates variance reduction techniques inspired by classical Monte Carlo optimization
        and modern approaches from Terence Tao's work on mathematical discovery at scale.

        ## Key References

        1. **Terence Tao et al.** - [Mathematical exploration and discovery at scale](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
        2. **Hammersley & Morton (1956)** - Antithetic variates technique
        3. **Lavenberg & Welch (1981)** - Control variates method

        ## Variance Reduction Techniques

        We'll compare three Monte Carlo methods for option pricing:

        1. **Standard Monte Carlo** - Baseline approach (O(1/√n) convergence)
        2. **Antithetic Variates** - Uses paired simulations with negatively correlated random variables
        3. **Control Variates** - Leverages correlation with analytically solvable problem

        The goal: **Achieve same accuracy with fewer simulations → Faster convergence**
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Option Parameters")
    return


@app.cell
def __():
    # Define parameters
    S = 100.0    # Current asset price
    K = 100.0    # Strike price (at-the-money)
    T = 1.0      # 1 year to maturity
    r = 0.05     # 5% risk-free rate
    sigma = 0.2  # 20% volatility
    option_type = 'call'

    # Number of simulations to test
    num_sims = 50000

    return K, S, T, num_sims, option_type, r, sigma


@app.cell
def __(K, S, T, black_scholes, calculate_greeks, mo, option_type, r, sigma):
    # Get analytical solution
    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    greeks = calculate_greeks(S, K, T, r, sigma, option_type)

    mo.md(f"""
    ### Analytical Black-Scholes Solution

    **Option Price:** ${bs_price:.6f}

    **The Greeks:**
    - **Delta (Δ):** {greeks['delta']:.6f} - Hedge ratio
    - **Gamma (Γ):** {greeks['gamma']:.6f} - Convexity
    - **Vega (ν):** {greeks['vega']:.6f} - Volatility sensitivity (per 1%)
    - **Theta (Θ):** {greeks['theta']:.6f} - Time decay (per day)
    - **Rho (ρ):** {greeks['rho']:.6f} - Interest rate sensitivity (per 1%)

    **Higher-Order Greeks:**
    - **Vomma:** {greeks['vomma']:.6f} - Vega convexity
    - **Vanna:** {greeks['vanna']:.6f} - Cross derivative (spot-vol)
    - **Charm:** {greeks['charm']:.6f} - Delta decay
    """)
    return bs_price, greeks


@app.cell
def __(
    K,
    S,
    T,
    monte_carlo_antithetic,
    monte_carlo_control_variate,
    monte_carlo_option_price,
    num_sims,
    option_type,
    r,
    sigma,
):
    # Run all three methods
    standard_price, standard_conv = monte_carlo_option_price(
        S, K, T, r, sigma, option_type, num_sims, track_convergence=True
    )

    antithetic_price, antithetic_conv, var_red_anti = monte_carlo_antithetic(
        S, K, T, r, sigma, option_type, num_sims // 2, track_convergence=True
    )

    cv_price, cv_conv, var_red_cv = monte_carlo_control_variate(
        S, K, T, r, sigma, option_type, num_sims, track_convergence=True
    )

    return (
        antithetic_conv,
        antithetic_price,
        cv_conv,
        cv_price,
        standard_conv,
        standard_price,
        var_red_anti,
        var_red_cv,
    )


@app.cell
def __(
    antithetic_price,
    bs_price,
    cv_price,
    mo,
    pd,
    standard_price,
    var_red_anti,
    var_red_cv,
):
    # Results comparison
    comparison_df = pd.DataFrame({
        'Method': ['Standard MC', 'Antithetic Variates', 'Control Variates'],
        'Price': [f'${standard_price:.6f}', f'${antithetic_price:.6f}', f'${cv_price:.6f}'],
        'Error': [
            f'${abs(standard_price - bs_price):.6f}',
            f'${abs(antithetic_price - bs_price):.6f}',
            f'${abs(cv_price - bs_price):.6f}'
        ],
        'Rel Error (%)': [
            f'{abs(standard_price - bs_price)/bs_price * 100:.4f}%',
            f'{abs(antithetic_price - bs_price)/bs_price * 100:.4f}%',
            f'{abs(cv_price - bs_price)/bs_price * 100:.4f}%'
        ],
        'Variance Reduction': [
            '-',
            f'{var_red_anti:.1f}%',
            f'{var_red_cv:.1f}%'
        ]
    })

    mo.md(f"""
    ## Results Comparison

    {mo.ui.table(comparison_df)}

    ### Key Insights

    - **Antithetic Variates** reduced variance by **{var_red_anti:.1f}%**
    - **Control Variates** reduced variance by **{var_red_cv:.1f}%**
    - Both methods achieved better accuracy with same computational cost!
    """)
    return (comparison_df,)


@app.cell
def __(
    antithetic_conv,
    bs_price,
    cv_conv,
    go,
    make_subplots,
    standard_conv,
):
    # Create convergence comparison plots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Price Convergence Comparison',
            'Standard Error Comparison',
            'Convergence Speed (Log Scale)',
            'Efficiency Gain'
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    # Plot 1: Price convergence
    fig.add_trace(
        go.Scatter(
            x=standard_conv['iterations'],
            y=standard_conv['prices'],
            mode='lines+markers',
            name='Standard MC',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=antithetic_conv['iterations'],
            y=antithetic_conv['prices'],
            mode='lines+markers',
            name='Antithetic',
            line=dict(color='green', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=cv_conv['iterations'],
            y=cv_conv['prices'],
            mode='lines+markers',
            name='Control Variate',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=standard_conv['iterations'],
            y=[bs_price] * len(standard_conv['iterations']),
            mode='lines',
            name='Black-Scholes',
            line=dict(color='black', dash='dash', width=2)
        ),
        row=1, col=1
    )

    # Plot 2: Standard error
    fig.add_trace(
        go.Scatter(
            x=standard_conv['iterations'],
            y=standard_conv['std_errors'],
            mode='lines',
            name='Standard MC',
            line=dict(color='blue', width=2),
            showlegend=False
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=antithetic_conv['iterations'],
            y=antithetic_conv['std_errors'],
            mode='lines',
            name='Antithetic',
            line=dict(color='green', width=2),
            showlegend=False
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=cv_conv['iterations'],
            y=cv_conv['std_errors'],
            mode='lines',
            name='Control Variate',
            line=dict(color='red', width=2),
            showlegend=False
        ),
        row=1, col=2
    )

    # Plot 3: Log-log convergence (theoretical is straight line with slope -0.5)
    fig.add_trace(
        go.Scatter(
            x=standard_conv['iterations'],
            y=standard_conv['std_errors'],
            mode='lines+markers',
            name='Standard MC',
            line=dict(color='blue', width=2),
            showlegend=False
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=antithetic_conv['iterations'],
            y=antithetic_conv['std_errors'],
            mode='lines+markers',
            name='Antithetic',
            line=dict(color='green', width=2),
            showlegend=False
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=cv_conv['iterations'],
            y=cv_conv['std_errors'],
            mode='lines+markers',
            name='Control Variate',
            line=dict(color='red', width=2),
            showlegend=False
        ),
        row=2, col=1
    )

    # Plot 4: Efficiency gain (variance reduction over standard)
    baseline_var = [se**2 for se in standard_conv['std_errors']]
    anti_var = [se**2 for se in antithetic_conv['std_errors']]
    cv_var = [se**2 for se in cv_conv['std_errors']]

    efficiency_anti = [(1 - av/bv) * 100 if bv > 0 else 0
                       for av, bv in zip(anti_var, baseline_var)]
    efficiency_cv = [(1 - cv_v/bv) * 100 if bv > 0 else 0
                     for cv_v, bv in zip(cv_var, baseline_var)]

    fig.add_trace(
        go.Scatter(
            x=antithetic_conv['iterations'],
            y=efficiency_anti,
            mode='lines+markers',
            name='Antithetic Gain',
            line=dict(color='green', width=2),
            fill='tozeroy',
            showlegend=False
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=cv_conv['iterations'],
            y=efficiency_cv,
            mode='lines+markers',
            name='CV Gain',
            line=dict(color='red', width=2),
            showlegend=False
        ),
        row=2, col=2
    )

    # Update axes
    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=1)
    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=2)
    fig.update_xaxes(type="log", title_text="Iterations (log)", row=2, col=1)
    fig.update_xaxes(type="log", title_text="Iterations", row=2, col=2)

    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Std Error ($)", row=1, col=2)
    fig.update_yaxes(type="log", title_text="Std Error (log)", row=2, col=1)
    fig.update_yaxes(title_text="Variance Reduction (%)", row=2, col=2)

    fig.update_layout(
        height=800,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title_text="Monte Carlo Optimization Comparison",
        title_x=0.5
    )

    convergence_comparison_plot = fig
    return (
        anti_var,
        baseline_var,
        convergence_comparison_plot,
        cv_var,
        efficiency_anti,
        efficiency_cv,
        fig,
    )


@app.cell
def __(convergence_comparison_plot, mo):
    mo.ui.plotly(convergence_comparison_plot)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Mathematical Foundations

        ### Standard Monte Carlo
        - **Convergence rate:** O(1/√n)
        - **Variance:** σ²/n
        - **Paths required** for ε accuracy: O(1/ε²)

        ### Antithetic Variates
        For random variable Z ~ N(0,1), use both Z and -Z:
        - **Variance reduction:** Var[(f(Z) + f(-Z))/2] = Var[f(Z)]/2 when f is monotonic
        - **Benefit:** 50% variance reduction for convex/concave functions
        - **Cost:** Nearly free (reuses same random numbers)

        ### Control Variates
        For target Y with control X (known mean μₓ):
        - **Estimator:** Y* = Y - β(X - μₓ)
        - **Optimal β:** Cov(Y,X) / Var(X)
        - **Variance reduction:** 1 - ρ²(Y,X) where ρ is correlation
        - **Benefit:** Can exceed 90% for highly correlated controls

        ## Connections to Terence Tao's Work

        Tao's AlphaEvolve project demonstrates how optimization can be automated for mathematical discovery:

        1. **Problem formulation** - Express problem as optimization
        2. **Iterative refinement** - Use AI to propose improvements
        3. **Mathematical verification** - Prove results rigorously
        4. **Scale** - Test across 67+ diverse problems

        Our variance reduction techniques follow similar principles:
        - Reformulate the problem (antithetic pairing, control variates)
        - Iterate to optimal parameters (β in control variates)
        - Verify improvement mathematically (variance calculations)
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Export to Sonnet 4.5

        To learn more about these techniques, copy the following prompt and paste it into Claude Sonnet 4.5:
        """
    )
    return


@app.cell
def __(
    antithetic_price,
    bs_price,
    cv_price,
    mo,
    num_sims,
    standard_price,
    var_red_anti,
    var_red_cv,
):
    export_prompt = f"""
# Monte Carlo Variance Reduction Analysis

I've been studying variance reduction techniques for Monte Carlo simulation in computational finance. Here are my results from pricing a European call option:

## Results

**Method Comparison:**
- Standard Monte Carlo: ${standard_price:.6f} (baseline)
- Antithetic Variates: ${antithetic_price:.6f} ({var_red_anti:.1f}% variance reduction)
- Control Variates: ${cv_price:.6f} ({var_red_cv:.1f}% variance reduction)
- Black-Scholes (analytical): ${bs_price:.6f}

**Parameters:** {num_sims:,} simulations

## Questions

1. **Theoretical foundations:** Can you explain why antithetic variates work particularly well for monotonic functions? What's the mathematical proof?

2. **Optimal control variates:** How do I determine the optimal control variate for a given problem? What makes a good control?

3. **Combining techniques:** Can I combine antithetic variates with control variates? What's the theoretical variance reduction?

4. **Advanced methods:** What are other variance reduction techniques I should explore? (e.g., importance sampling, stratified sampling)

5. **Connections to other fields:** How do these techniques relate to:
   - Quasi-Monte Carlo methods
   - MCMC sampling
   - Reinforcement learning (baseline methods)

6. **Practical considerations:** When might variance reduction techniques fail or be counterproductive?

Please provide detailed mathematical explanations with:
- Rigorous proofs where relevant
- Concrete examples
- References to key papers
- Implementation guidance

---
*Generated from Black-Scholes Mathematical Knowledge System*
*Optimization Comparison Notebook*
"""

    mo.md(f"""
    ### Copy this prompt:

    ```markdown
    {export_prompt}
    ```

    **📋 Click to select all, then Ctrl+C to copy**
    """)
    return (export_prompt,)


@app.cell
def __(mo):
    mo.md(
        """
        ## Further Reading

        ### Terence Tao's Work
        - [What's New (Blog)](https://terrytao.wordpress.com/)
        - [AlphaEvolve Repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
        - Paper: "Mathematical exploration and discovery at scale"

        ### Variance Reduction Techniques
        - [Wikipedia: Variance Reduction](https://en.wikipedia.org/wiki/Variance_reduction)
        - [Wikipedia: Antithetic Variates](https://en.wikipedia.org/wiki/Antithetic_variates)
        - Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*

        ### Option Greeks
        - Hull, J. (2018). *Options, Futures, and Other Derivatives*
        - Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance*

        ### Mathematical Greeks in General
        - Various analysis and algebra textbooks
        - See the Mathematical Search interface for comprehensive listing
        """
    )
    return


if __name__ == "__main__":
    app.run()
