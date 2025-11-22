import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.services.option_pricing_service import OptionPricingService
from src.services.data_persistence_service import DataPersistenceService
from src.gui.convergence_plots import display_convergence_analysis

# Initialize services
option_service = OptionPricingService()
data_service = DataPersistenceService()

st.title('Black-Scholes Option Pricer')

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Basic Pricing", "Convergence Analysis", "Price Heatmap"])

# Input fields in sidebar
st.sidebar.header("Option Parameters")
S = st.sidebar.number_input('Current Asset Price', value=100.0)
K = st.sidebar.number_input('Strike Price', value=100.0)
T = st.sidebar.number_input('Time to Maturity (years)', value=1.0, min_value=0.0)
r = st.sidebar.number_input('Risk-Free Interest Rate', value=0.05)
sigma = st.sidebar.number_input('Volatility', value=0.2, min_value=0.0)
option_type = st.sidebar.selectbox('Option Type', ['call', 'put'])

with tab1:
    st.header("Black-Scholes Pricing")

    # Calculate option price
    price = option_service.calculate_option_prices(S, K, T, r, sigma, option_type)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f'{option_type.capitalize()} Option Price', value=f'${price:.4f}')

    # P/L calculation
    with col2:
        purchase_price = st.number_input('Purchase Price', value=price)
        pl = price - purchase_price
        delta = f"{(pl/purchase_price)*100:.2f}%" if purchase_price != 0 else "N/A"
        st.metric(label='Profit/Loss', value=f'${pl:.4f}', delta=delta)

    # Save calculation
    if st.button('Save Calculation'):
        base_inputs = f"S:{S},K:{K},T:{T},r:{r},sigma:{sigma},type:{option_type}"
        calculation_id = np.random.randint(1000000)
        data_service.save_calculation(base_inputs, sigma, S, pl, calculation_id)
        st.success('Calculation saved successfully!')

with tab2:
    st.header("Monte Carlo Convergence Analysis")

    num_simulations = st.slider(
        'Number of Simulations',
        min_value=10000,
        max_value=500000,
        value=100000,
        step=10000
    )

    if st.button('Run Convergence Analysis', type='primary'):
        display_convergence_analysis(S, K, T, r, sigma, option_type, num_simulations)

with tab3:
    st.header("Option Price Heatmap")

    # Generate heatmap data
    prices, vols, heatmap_data = option_service.generate_heatmap_data(S, K, T, r, sigma, option_type)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=prices,
        y=vols,
        colorscale='RdYlGn',
        colorbar=dict(title='Option Price')
    ))

    fig.update_layout(
        title='Option Price Heatmap',
        xaxis_title='Stock Price',
        yaxis_title='Volatility',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

# Close database connection when the app is done
data_service.close_connection()