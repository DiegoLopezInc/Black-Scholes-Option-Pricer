import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.services.option_pricing_service import OptionPricingService
from src.services.data_persistence_service import DataPersistenceService

# Initialize services
option_service = OptionPricingService()
data_service = DataPersistenceService()

st.title('Black-Scholes Option Pricer')

# Input fields
S = st.number_input('Current Asset Price', value=100.0)
K = st.number_input('Strike Price', value=100.0)
T = st.number_input('Time to Maturity (years)', value=1.0, min_value=0.0)
r = st.number_input('Risk-Free Interest Rate', value=0.05)
sigma = st.number_input('Volatility', value=0.2, min_value=0.0)
option_type = st.selectbox('Option Type', ['call', 'put'])

# Calculate option price
price = option_service.calculate_option_prices(S, K, T, r, sigma, option_type)
st.write(f'{option_type.capitalize()} Option Price: ${price:.2f}')

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
    yaxis_title='Volatility'
)

st.plotly_chart(fig)

# P/L calculation
purchase_price = st.number_input('Purchase Price', value=price)
pl = price - purchase_price
st.write(f'Profit/Loss: ${pl:.2f}')

# Save calculation
if st.button('Save Calculation'):
    base_inputs = f"S:{S},K:{K},T:{T},r:{r},sigma:{sigma},type:{option_type}"
    calculation_id = np.random.randint(1000000)
    data_service.save_calculation(base_inputs, sigma, S, pl, calculation_id)
    st.success('Calculation saved successfully!')

# Close database connection when the app is done
data_service.close_connection()