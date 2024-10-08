# Black Scholes Option Pricer

## Overview
This project implements an interactive Black-Scholes Option Pricing calculator with a Streamlit GUI, featuring dynamic heatmaps and MySQL data persistence. The project structure is designed to host different parts of the system as microservices for modularity and reliability.

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

## Security Improvements and Setup Instructions

To enhance security and make the project safe for public repositories, the following improvements have been implemented:

1. Environment variables: Sensitive information such as database credentials are now managed using environment variables.
2. Non-root user: The Dockerfile now creates and uses a non-root user for running the application.
3. MySQL healthcheck: A healthcheck has been added to ensure the MySQL service is ready before the application attempts to connect.
4. Secure database initialization: The MySQL service now creates a specific user for the application instead of using the root user.

### Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/black-scholes-option-pricer.git
   cd black-scholes-option-pricer
   ```

2. Create a `.env` file in the project root with the following content:
   ```
   MYSQL_HOST=mysql
   MYSQL_USER=options_user
   MYSQL_PASSWORD=your_secure_password
   MYSQL_DATABASE=options_db
   MYSQL_ROOT_PASSWORD=your_secure_root_password
   ```
   Replace `your_secure_password` and `your_secure_root_password` with strong, unique passwords.

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. Access the application at `http://localhost:8501`

Note: The `.env` file contains sensitive information and should not be committed to version control. It has been added to `.gitignore` for this purpose.

## Future Enhancements
- Connect to a data lake or repository for testing ideas
- Optimize data usage and efficiency