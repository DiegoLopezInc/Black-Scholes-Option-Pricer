# Model Validation Notebooks

This directory contains interactive notebooks for validating and analyzing the Black-Scholes option pricing model.

## Files

### `model_validation.py` - Marimo Notebook

An interactive Marimo notebook that:
- Validates Black-Scholes pricing using Monte Carlo simulation
- Visualizes convergence behavior with dynamic plots
- Uses Together AI (via TINKER_KEY) for intelligent model analysis
- **Implements strict $2 cost limit** with real-time tracking

## Running the Notebook

### Prerequisites
```bash
pip install marimo together pandas plotly
```

### Environment Setup
Make sure `TINKER_KEY` is set in your environment:
```bash
export TINKER_KEY="your_together_ai_key"
```

### Launch Marimo Notebook
```bash
# From project root
marimo edit notebooks/model_validation.py
```

The notebook will open in your browser at `http://localhost:2718`

## Features

### 1. Monte Carlo Validation
- Runs 100,000 simulations by default
- Compares against analytical Black-Scholes price
- Tracks convergence at logarithmic intervals

### 2. Convergence Visualization
- Price convergence plot
- Standard error reduction
- Interactive Plotly charts

### 3. LLM-Powered Analysis
- **Cost-Controlled**: Maximum $2 spend on API calls
- Real-time token and cost tracking
- Intelligent analysis of convergence behavior
- Greeks explanation using Together AI's Llama-3.1-8B model
- Detailed call history and budget status

### 4. Cost Tracking
The notebook includes comprehensive cost tracking:
- Input/output token counts
- Per-call cost calculation
- Running total with budget alerts
- Automatic shutoff at $2 limit
- Detailed API call history

## Cost Structure

**Together AI Pricing (Llama-3.1-8B-Instruct-Turbo)**:
- Input: $0.20 per 1M tokens
- Output: $0.20 per 1M tokens

**Estimated Usage**:
- ~2,000 input tokens per analysis
- ~400 output tokens per response
- **Cost per analysis**: ~$0.0005
- **Total analyses possible**: ~4,000 within $2 budget

## Safety Features

1. **Pre-call budget check**: Prevents calls if budget exceeded
2. **Real-time cost calculation**: After each API call
3. **Cost history**: Tracks all API calls with timestamps
4. **Clear warnings**: Visual feedback when approaching/exceeding limit

## Example Output

```
Pricing Results:
┌───────────────┬──────────────┬────────────┬───────────────┐
│ Method        │ Price        │ Difference │ Relative Error│
├───────────────┼──────────────┼────────────┼───────────────┤
│ Black-Scholes │ $10.450584   │ -          │ -             │
│ Monte Carlo   │ $10.451237   │ $0.000653  │ 0.0062%       │
└───────────────┴──────────────┴────────────┴───────────────┘

Cost Tracking Summary:
┌────────────────────┬──────────┐
│ Metric             │ Value    │
├────────────────────┼──────────┤
│ Total API Calls    │ 2        │
│ Total Input Tokens │ 3,847    │
│ Total Output Tokens│ 723      │
│ Total Cost         │ $0.00091 │
│ Remaining Budget   │ $1.99909 │
└────────────────────┴──────────┘

Budget Status: ✅ Within Budget
```

## Notebook Structure

1. **Setup**: Import libraries, configure cost tracking
2. **Model Import**: Load Black-Scholes functions
3. **Test Parameters**: Define option parameters
4. **Simulation**: Run Monte Carlo with convergence tracking
5. **Results**: Display pricing comparison
6. **Visualization**: Interactive convergence plots
7. **LLM Analysis**: AI-powered result interpretation
8. **Greeks Explanation**: Educational analysis of option sensitivities
9. **Cost Summary**: Final budget status and call history

## Customization

### Change Parameters
Modify the option parameters in the notebook:
```python
S = 100.0      # Current asset price
K = 100.0      # Strike price
T = 1.0        # Time to maturity
r = 0.05       # Risk-free rate
sigma = 0.2    # Volatility
option_type = 'call'  # or 'put'
num_simulations = 100000
```

### Adjust Budget
Change the cost limit:
```python
MAX_COST_USD = 2.00  # Increase/decrease as needed
```

### Use Different Model
Switch to a different Together AI model:
```python
model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"  # More capable, higher cost
```

## Troubleshooting

### "TINKER_KEY not found"
Set the environment variable:
```bash
export TINKER_KEY="your_api_key"
```

### "Cost limit exceeded"
The notebook has reached the $2 budget. To continue:
1. Restart the notebook (resets cost tracker)
2. Or increase `MAX_COST_USD`

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Interactive Features

Marimo notebooks are reactive, meaning:
- Changes to parameters automatically re-run dependent cells
- Plots update in real-time
- No need to manually re-execute cells
- Clean, reproducible results

## Next Steps

After validation:
1. Review convergence quality in plots
2. Read LLM analysis for insights
3. Adjust parameters if needed
4. Export results for documentation
5. Check cost summary to track budget usage
