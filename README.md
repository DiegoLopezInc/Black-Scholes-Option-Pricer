# Black Scholes Option Pricer

## Overview
This project implements a Black Scholes Option Pricing model with an interactive GUI using Streamlit. It also includes data persistence using MySQL.

## Black Scholes Options Model
The model uses the following inputs:
- Current Asset Price
- Strike Price
- Time to Maturity
- Volatility
- Risk-Free Interest Rate

## GUI Layer (Streamlit)
The GUI allows users to:
1. Enter values for the model inputs
2. View an interactive heatmap of call and put option prices
3. Adjust volatility and stock prices using sliding bars
4. Enter purchase prices for call and put options
5. View Profit/Loss (P/L) based on input and purchase prices

Heatmap features:
- Updates dynamically with user input
- Color-coded: green for higher values, red for lower values
- Displays option prices (not P/L)

## Data Management
- Inputs and outputs are saved to a MySQL relational database
- Database structure:
  - Table with 6 rows and 5 columns
  - Columns:
    1. Base inputs (Black Scholes model parameters)
    2. Volatility and future shocks against base inputs
    3. P/L associated with shock and input
    4. Calculation ID (links outputs to distinct inputs)
    5. Unique identifier for each shock/volatility combination

## Development Steps
1. Implement Black Scholes model calculation
2. Create Streamlit GUI with input fields and heatmap visualization
3. Add interactivity to GUI (sliding bars, dynamic updates)
4. Implement P/L calculation
5. Set up MySQL database and connection
6. Implement data saving and retrieval functions
7. Integrate all components and test thoroughly

## Future Enhancements
- Connect to a data lake or repository for testing ideas
- Optimize data usage and efficiency