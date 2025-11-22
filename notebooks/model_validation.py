import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import os
    from together import Together
    import json
    from datetime import datetime
    return Together, datetime, go, json, make_subplots, mo, np, os, pd


@app.cell
def __(mo):
    mo.md(
        """
        # Black-Scholes Model Validation with LLM Analysis

        This notebook validates the Black-Scholes option pricing model using Monte Carlo simulation
        and leverages the Together AI API for intelligent model analysis and interpretation.

        **Cost Limit: $2.00 maximum**
        """
    )
    return


@app.cell
def __(os):
    # Cost tracking configuration
    MAX_COST_USD = 2.00
    COST_PER_1M_INPUT_TOKENS = 0.20  # Together AI Llama-3.1-8B pricing
    COST_PER_1M_OUTPUT_TOKENS = 0.20

    # Initialize cost tracker
    cost_tracker = {
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_cost': 0.0,
        'api_calls': 0,
        'calls_history': []
    }

    # Get API key from environment
    TINKER_KEY = os.environ.get('TINKER_KEY', '')
    if not TINKER_KEY:
        raise ValueError("TINKER_KEY not found in environment variables")

    return (
        COST_PER_1M_INPUT_TOKENS,
        COST_PER_1M_OUTPUT_TOKENS,
        MAX_COST_USD,
        TINKER_KEY,
        cost_tracker,
    )


@app.cell
def __(mo):
    # Import our Black-Scholes functions
    import sys
    sys.path.append('/home/user/Black-Scholes-Option-Pricer')

    from src.models.black_scholes import black_scholes, monte_carlo_option_price

    mo.md("### Model Functions Imported Successfully")
    return black_scholes, monte_carlo_option_price, sys


@app.cell
def __(
    COST_PER_1M_INPUT_TOKENS,
    COST_PER_1M_OUTPUT_TOKENS,
    MAX_COST_USD,
    TINKER_KEY,
    Together,
    cost_tracker,
    datetime,
    json,
):
    def call_llm_with_cost_limit(prompt, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"):
        """Call Together AI LLM with cost tracking and limits"""

        # Check if we've exceeded cost limit
        if cost_tracker['total_cost'] >= MAX_COST_USD:
            return {
                'error': f"Cost limit of ${MAX_COST_USD} exceeded. Current cost: ${cost_tracker['total_cost']:.4f}",
                'exceeded_limit': True
            }

        try:
            client = Together(api_key=TINKER_KEY)

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7,
            )

            # Extract token usage
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens

            # Calculate cost
            input_cost = (input_tokens / 1_000_000) * COST_PER_1M_INPUT_TOKENS
            output_cost = (output_tokens / 1_000_000) * COST_PER_1M_OUTPUT_TOKENS
            call_cost = input_cost + output_cost

            # Update tracker
            cost_tracker['total_input_tokens'] += input_tokens
            cost_tracker['total_output_tokens'] += output_tokens
            cost_tracker['total_cost'] += call_cost
            cost_tracker['api_calls'] += 1
            cost_tracker['calls_history'].append({
                'timestamp': datetime.now().isoformat(),
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': call_cost,
                'model': model
            })

            return {
                'response': response.choices[0].message.content,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': call_cost,
                'total_cost': cost_tracker['total_cost'],
                'exceeded_limit': False
            }

        except Exception as e:
            return {
                'error': str(e),
                'exceeded_limit': False
            }

    return (call_llm_with_cost_limit,)


@app.cell
def __(mo):
    mo.md(
        """
        ## Test Parameters

        Define option parameters for validation:
        """
    )
    return


@app.cell
def __():
    # Option parameters
    S = 100.0  # Current asset price
    K = 100.0  # Strike price
    T = 1.0    # Time to maturity (1 year)
    r = 0.05   # Risk-free rate (5%)
    sigma = 0.2  # Volatility (20%)
    option_type = 'call'
    num_simulations = 100000

    return K, S, T, num_simulations, option_type, r, sigma


@app.cell
def __(
    K,
    S,
    T,
    black_scholes,
    monte_carlo_option_price,
    num_simulations,
    option_type,
    r,
    sigma,
):
    # Run simulations
    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    mc_price, convergence_data = monte_carlo_option_price(
        S, K, T, r, sigma, option_type, num_simulations, track_convergence=True
    )

    return bs_price, convergence_data, mc_price


@app.cell
def __(bs_price, mc_price, mo, pd):
    # Display results
    results_df = pd.DataFrame({
        'Method': ['Black-Scholes', 'Monte Carlo'],
        'Price': [f'${bs_price:.6f}', f'${mc_price:.6f}'],
        'Difference': ['-', f'${abs(mc_price - bs_price):.6f}'],
        'Relative Error': ['-', f'{abs(mc_price - bs_price)/bs_price * 100:.4f}%']
    })

    mo.md(f"""
    ### Pricing Results

    {mo.ui.table(results_df)}
    """)
    return (results_df,)


@app.cell
def __(convergence_data, go, make_subplots):
    # Create convergence plots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Price Convergence', 'Standard Error Reduction')
    )

    fig.add_trace(
        go.Scatter(
            x=convergence_data['iterations'],
            y=convergence_data['prices'],
            mode='lines+markers',
            name='MC Price',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=convergence_data['iterations'],
            y=convergence_data['std_errors'],
            mode='lines+markers',
            name='Std Error',
            line=dict(color='green', width=2)
        ),
        row=1, col=2
    )

    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=1)
    fig.update_xaxes(type="log", title_text="Iterations", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Std Error ($)", row=1, col=2)

    fig.update_layout(height=400, showlegend=True, title_text="Monte Carlo Convergence Analysis")

    convergence_plot = fig
    return (convergence_plot,)


@app.cell
def __(convergence_plot, mo):
    mo.ui.plotly(convergence_plot)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## LLM-Powered Model Analysis

        Use Together AI to analyze the convergence behavior and validate the model:
        """
    )
    return


@app.cell
def __(
    K,
    S,
    T,
    bs_price,
    call_llm_with_cost_limit,
    convergence_data,
    json,
    mc_price,
    num_simulations,
    option_type,
    r,
    sigma,
):
    # Prepare analysis prompt
    analysis_prompt = f"""
    You are a quantitative finance expert. Analyze the following Black-Scholes option pricing validation results:

    Parameters:
    - Asset Price (S): ${S}
    - Strike Price (K): ${K}
    - Time to Maturity (T): {T} years
    - Risk-Free Rate (r): {r*100}%
    - Volatility (σ): {sigma*100}%
    - Option Type: {option_type}

    Results:
    - Black-Scholes Price: ${bs_price:.6f}
    - Monte Carlo Price ({num_simulations:,} simulations): ${mc_price:.6f}
    - Absolute Difference: ${abs(mc_price - bs_price):.6f}
    - Relative Error: {abs(mc_price - bs_price)/bs_price * 100:.4f}%

    Convergence Data (last 3 checkpoints):
    {json.dumps({
        'iterations': convergence_data['iterations'][-3:],
        'prices': [f'${p:.6f}' for p in convergence_data['prices'][-3:]],
        'std_errors': [f'${se:.6f}' for se in convergence_data['std_errors'][-3:]]
    }, indent=2)}

    Please provide:
    1. Assessment of convergence quality
    2. Whether the Monte Carlo results validate the Black-Scholes price
    3. Recommendations for improving accuracy (if needed)
    4. Any concerns or observations about the results

    Keep your response concise (under 300 words).
    """

    llm_result = call_llm_with_cost_limit(analysis_prompt)
    return analysis_prompt, llm_result


@app.cell
def __(llm_result, mo):
    # Display LLM analysis
    if 'error' in llm_result:
        mo.md(f"**Error:** {llm_result['error']}")
    else:
        mo.md(f"""
        ### AI Analysis Results

        {llm_result['response']}

        ---

        **Token Usage:**
        - Input Tokens: {llm_result['input_tokens']:,}
        - Output Tokens: {llm_result['output_tokens']:,}
        - Call Cost: ${llm_result['cost']:.6f}
        - Total Cost So Far: ${llm_result['total_cost']:.6f}
        """)
    return


@app.cell
def __(
    K,
    S,
    T,
    call_llm_with_cost_limit,
    option_type,
    r,
    sigma,
):
    # Additional analysis: Greeks explanation
    greeks_prompt = f"""
    For a {option_type} option with the following parameters:
    - S = ${S}, K = ${K}, T = {T} years, r = {r*100}%, σ = {sigma*100}%

    Explain in 2-3 sentences:
    1. What is Delta and why is it important for this option?
    2. How would Vega affect this option's price if volatility increased?

    Be concise and practical.
    """

    greeks_result = call_llm_with_cost_limit(greeks_prompt)
    return greeks_prompt, greeks_result


@app.cell
def __(greeks_result, mo):
    if 'error' in greeks_result and not greeks_result['exceeded_limit']:
        mo.md(f"**Error:** {greeks_result['error']}")
    elif greeks_result.get('exceeded_limit'):
        mo.md(f"**Cost Limit Reached:** {greeks_result['error']}")
    else:
        mo.md(f"""
        ### Greeks Explanation

        {greeks_result['response']}

        **Cost:** ${greeks_result['cost']:.6f} | **Total:** ${greeks_result['total_cost']:.6f}
        """)
    return


@app.cell
def __(cost_tracker, mo, pd):
    # Final cost summary
    summary_df = pd.DataFrame({
        'Metric': [
            'Total API Calls',
            'Total Input Tokens',
            'Total Output Tokens',
            'Total Cost',
            'Remaining Budget'
        ],
        'Value': [
            cost_tracker['api_calls'],
            f"{cost_tracker['total_input_tokens']:,}",
            f"{cost_tracker['total_output_tokens']:,}",
            f"${cost_tracker['total_cost']:.6f}",
            f"${2.00 - cost_tracker['total_cost']:.6f}"
        ]
    })

    mo.md(f"""
    ## Cost Tracking Summary

    {mo.ui.table(summary_df)}

    ### Budget Status: {'✅ Within Budget' if cost_tracker['total_cost'] < 2.00 else '❌ Budget Exceeded'}
    """)
    return (summary_df,)


@app.cell
def __(cost_tracker, json, mo, pd):
    # Detailed call history
    if cost_tracker['calls_history']:
        calls_df = pd.DataFrame(cost_tracker['calls_history'])
        calls_df['cost'] = calls_df['cost'].apply(lambda x: f"${x:.6f}")

        mo.md(f"""
        ### API Call History

        {mo.ui.table(calls_df)}
        """)
    return (calls_df,)


if __name__ == "__main__":
    app.run()
