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
   cd .\docker\
   docker-compose up --build
   ```

4. Access the application at `http://localhost:8501`

Note: The `.env` file contains sensitive information and should not be committed to version control. It has been added to `.gitignore` for this purpose.

## New Features

### Monte Carlo Convergence Analysis
- Monte Carlo simulation with convergence tracking at logarithmic intervals
- Real-time visualization of price convergence, standard error reduction, and confidence intervals
- Comparison against analytical Black-Scholes pricing
- Interactive convergence plots with 4 different metrics:
  - Price convergence to Black-Scholes
  - Standard error reduction (shows √n convergence)
  - 95% confidence intervals
  - Relative error percentage

### REST API Endpoints
FastAPI-based REST API for programmatic access:
- `POST /price` - Calculate option price using Black-Scholes formula
- `POST /monte-carlo` - Run Monte Carlo simulation with convergence data
- `POST /heatmap` - Generate heatmap data for visualization
- `GET /` - API information and version

**Run API Server**:
```bash
python -m src.api.routes
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Model Validation Notebook
Interactive Marimo notebook (`notebooks/model_validation.py`) with:
- Automated model validation using Monte Carlo vs Black-Scholes
- **LLM-powered analysis** using Together AI for intelligent insights
- **Strict $2 cost limit** with real-time tracking
- Interactive convergence visualization
- Greeks explanation and interpretation
- Detailed API call history and budget monitoring

**Run Notebook**:
```bash
export TINKER_KEY="your_together_ai_key"
marimo edit notebooks/model_validation.py
```

### Enhanced Streamlit GUI
Updated Streamlit interface with three tabs:
1. **Basic Pricing** - Traditional Black-Scholes calculator with P/L
2. **Convergence Analysis** - Run Monte Carlo with live convergence plots
3. **Price Heatmap** - Interactive volatility/price sensitivity analysis

## Free Data Pipeline Options

See [`docs/FREE_DATA_PIPELINES.md`](docs/FREE_DATA_PIPELINES.md) for comprehensive guide on:
- Free backend hosting (Render, Railway, Fly.io, Streamlit Cloud)
- Free frontend deployment (Vercel, Netlify, Cloudflare Pages)
- Real-time data streaming options (WebSocket, SSE, Supabase)
- Recommended architecture and quick deployment guide

**Recommended Free Stack**:
- **Backend API**: Render.com (FastAPI)
- **GUI**: Streamlit Community Cloud
- **Frontend** (optional): Vercel (React)
- **Database**: Supabase (PostgreSQL) or local MySQL

## API Usage Examples

### Calculate Black-Scholes Price
```bash
curl -X POST "http://localhost:8000/price" \
  -H "Content-Type: application/json" \
  -d '{
    "S": 100,
    "K": 100,
    "T": 1,
    "r": 0.05,
    "sigma": 0.2,
    "option_type": "call"
  }'
```

### Run Monte Carlo with Convergence
```bash
curl -X POST "http://localhost:8000/monte-carlo" \
  -H "Content-Type: application/json" \
  -d '{
    "S": 100,
    "K": 100,
    "T": 1,
    "r": 0.05,
    "sigma": 0.2,
    "option_type": "call",
    "num_simulations": 100000
  }'
```

Response includes:
- `monte_carlo_price`: Simulated option price
- `black_scholes_price`: Analytical price
- `difference`: Absolute difference
- `convergence_data`: Arrays of iterations, prices, std_errors, confidence_intervals

## Project Structure

```
Black-Scholes-Option-Pricer/
├── src/
│   ├── models/
│   │   └── black_scholes.py          # Core pricing logic + Monte Carlo
│   ├── services/
│   │   ├── option_pricing_service.py # Pricing service layer
│   │   └── data_persistence_service.py
│   ├── gui/
│   │   ├── streamlit_app.py          # Enhanced Streamlit interface
│   │   └── convergence_plots.py      # Convergence visualization
│   ├── api/
│   │   └── routes.py                 # FastAPI REST endpoints
│   └── data/
│       └── database.py
├── notebooks/
│   ├── model_validation.py           # Marimo notebook with LLM analysis
│   └── README.md                     # Notebook documentation
├── docs/
│   └── FREE_DATA_PIPELINES.md        # Deployment and pipeline guide
├── docker/
│   └── docker-compose.yml
└── requirements.txt
```

## Advanced Optimization Features

### Variance Reduction Techniques

Faster convergence through mathematical optimization:

**Antithetic Variates** - Achieve ~50% variance reduction:
```python
from src.models.black_scholes import monte_carlo_antithetic

price, conv_data, var_reduction = monte_carlo_antithetic(
    S=100, K=100, T=1, r=0.05, sigma=0.2,
    option_type='call', num_simulations=50000
)
print(f"Variance reduced by {var_reduction:.1f}%")
```

**Control Variates** - Achieve up to 90% variance reduction:
```python
from src.models.black_scholes import monte_carlo_control_variate

price, conv_data, var_reduction = monte_carlo_control_variate(
    S=100, K=100, T=1, r=0.05, sigma=0.2,
    option_type='call', num_simulations=100000
)
print(f"Variance reduced by {var_reduction:.1f}%")
```

**Benefits:**
- Same accuracy with fewer simulations
- Faster computation time
- Lower memory requirements
- Mathematically proven variance reduction

See [`docs/OPTIMIZATION_TECHNIQUES.md`](docs/OPTIMIZATION_TECHNIQUES.md) for complete guide.

### Greeks Calculator

Calculate all option Greeks (first-order, second-order, and cross derivatives):

```python
from src.models.black_scholes import calculate_greeks

greeks = calculate_greeks(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')

print(f"Delta (Δ): {greeks['delta']:.6f}")
print(f"Gamma (Γ): {greeks['gamma']:.6f}")
print(f"Vega (ν): {greeks['vega']:.6f}")
print(f"Theta (Θ): {greeks['theta']:.6f}")
print(f"Rho (ρ): {greeks['rho']:.6f}")
print(f"Vomma: {greeks['vomma']:.6f}")
print(f"Vanna: {greeks['vanna']:.6f}")
print(f"Charm: {greeks['charm']:.6f}")
```

### Mathematical Concept Search

**searchthearXiv-style interface** for discovering mathematical concepts:

```bash
streamlit run src/gui/math_search.py
```

**Features:**
- 🔍 Search 20+ mathematical Greek symbols
- 📊 Browse 8 options Greeks with formulas
- ⚡ Explore optimization techniques
- 🤖 NLP-powered semantic search (with TINKER_KEY)
- 📤 Export concepts to Sonnet 4.5 for deeper learning
- 📈 Query analytics and fine-tuning

**Search Modes:**
1. **Quick Search** - Keyword-based search across all concepts
2. **NLP-Powered Search** - Natural language queries with AI
3. **Browse Categories** - Organized browsing by topic
4. **Query Analytics** - Track search patterns and success rates

### Interactive Visualizations

**Optimization Comparison Notebook** - Marimo notebook with:

```bash
marimo edit notebooks/optimization_comparison.py
```

- Side-by-side convergence comparison
- Variance reduction metrics visualization
- Mathematical foundations explained
- Interactive parameter exploration
- Export prompts for Sonnet 4.5 research

Inspired by **Terence Tao's AlphaEvolve** research on mathematical discovery at scale:
- [GitHub Repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
- Paper: "Mathematical exploration and discovery at scale" (2024-2025)

### Knowledge Base

Comprehensive mathematical reference system:

**Mathematical Greeks** (20+ symbols):
- Alpha (α) - Significance level, learning rate
- Beta (β) - Regression coefficients, Type II error
- Gamma (Γ) - Gamma function, Euler constant
- Delta (δ,Δ) - Dirac delta, finite differences
- Epsilon (ε) - Small quantities, error terms
- Zeta (ζ) - Riemann zeta function
- Lambda (λ) - Eigenvalues, Lagrange multipliers
- Mu (μ) - Mean, expected value
- Sigma (σ,Σ) - Standard deviation, summation
- And 11 more...

**Options Greeks** (8 derivatives):
- Delta (Δ) - ∂V/∂S - Price sensitivity
- Gamma (Γ) - ∂²V/∂S² - Delta sensitivity
- Vega (ν) - ∂V/∂σ - Volatility sensitivity
- Theta (Θ) - ∂V/∂t - Time decay
- Rho (ρ) - ∂V/∂r - Interest rate sensitivity
- Vomma - ∂²V/∂σ² - Vega convexity
- Vanna - ∂²V/∂S∂σ - Spot-vol cross derivative
- Charm - ∂²V/∂S∂t - Delta decay

**Optimization Techniques**:
- Variance reduction (antithetic, control variates)
- Gradient methods (SGD, momentum, Adam)
- Terence Tao's AlphaEvolve methodology
- Connections to options pricing

## Usage Examples

### Running All Interfaces

```bash
# 1. API Server (FastAPI with convergence endpoints)
python -m src.api.routes
# Visit http://localhost:8000/docs

# 2. Main Streamlit GUI (Basic pricing, convergence, heatmaps)
streamlit run src/gui/streamlit_app.py
# Visit http://localhost:8501

# 3. Mathematical Search Interface
streamlit run src/gui/math_search.py
# Visit http://localhost:8502

# 4. Model Validation Notebook (LLM analysis with cost tracking)
export TINKER_KEY="your_together_ai_key"
marimo edit notebooks/model_validation.py
# Visit http://localhost:2718

# 5. Optimization Comparison Notebook (Variance reduction)
marimo edit notebooks/optimization_comparison.py
# Visit http://localhost:2718

# 6. Run Tests
python test_api.py
```

### Comparing Optimization Methods

```python
from src.models.black_scholes import (
    black_scholes,
    monte_carlo_option_price,
    monte_carlo_antithetic,
    monte_carlo_control_variate
)

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

# Analytical benchmark
bs_price = black_scholes(S, K, T, r, sigma, 'call')
print(f"Black-Scholes: ${bs_price:.6f}")

# Standard Monte Carlo
mc_price, mc_conv = monte_carlo_option_price(
    S, K, T, r, sigma, 'call', 100000
)
print(f"Standard MC: ${mc_price:.6f}")

# Antithetic variates
anti_price, anti_conv, anti_var_red = monte_carlo_antithetic(
    S, K, T, r, sigma, 'call', 50000
)
print(f"Antithetic: ${anti_price:.6f} ({anti_var_red:.1f}% variance reduction)")

# Control variates
cv_price, cv_conv, cv_var_red = monte_carlo_control_variate(
    S, K, T, r, sigma, 'call', 100000
)
print(f"Control Variate: ${cv_price:.6f} ({cv_var_red:.1f}% variance reduction)")
```

## Performance

### Typical Variance Reductions

| Method | Variance Reduction | Convergence Rate | Best For |
|--------|-------------------|------------------|----------|
| Standard MC | Baseline | O(1/√n) | General purpose |
| Antithetic Variates | 40-60% | O(1/√n) | Smooth payoffs |
| Control Variates | 60-90% | O(1/√n) | When correlated control available |

### Speed Comparison

For same accuracy:
- **Antithetic variates**: ~2x faster (50% variance reduction)
- **Control variates**: ~5-10x faster (80-90% variance reduction)

## Future Enhancements
- WebSocket streaming for real-time convergence updates
- Additional exotic option types (Asian, Barrier, etc.)
- Portfolio optimization tools
- Historical data integration
- Multi-asset correlation models
- Machine learning price prediction
- Integration with live market data
- Advanced importance sampling techniques