
# Optimization Techniques for Faster Convergence

This document provides a comprehensive guide to variance reduction and optimization techniques implemented in the Black-Scholes Option Pricer, inspired by classical Monte Carlo methods and modern approaches from Terence Tao's mathematical discovery research.

## Table of Contents

1. [Variance Reduction Techniques](#variance-reduction-techniques)
2. [Mathematical Greeks Reference](#mathematical-greeks-reference)
3. [Options Greeks Reference](#options-greeks-reference)
4. [Terence Tao's Optimization Research](#terence-taos-optimization-research)
5. [Implementation Guide](#implementation-guide)
6. [Performance Comparison](#performance-comparison)

---

## Variance Reduction Techniques

### 1. Antithetic Variates

**Concept:** Use paired simulations with negatively correlated random variables to reduce variance.

**Mathematical Foundation:**
For random variable Z ~ N(0,1), generate both Z and -Z. For a function f:

```
Var[(f(Z) + f(-Z))/2] ≤ Var[f(Z)]
```

For monotonic functions, this typically achieves **~50% variance reduction**.

**Implementation:**
```python
from src.models.black_scholes import monte_carlo_antithetic

price, conv_data, var_reduction = monte_carlo_antithetic(
    S=100, K=100, T=1, r=0.05, sigma=0.2,
    option_type='call',
    num_simulations=50000,
    track_convergence=True
)

print(f"Variance reduction: {var_reduction:.1f}%")
```

**When to Use:**
- Option payoffs are monotonic or convex/concave
- Minimal computational overhead required
- Works best for symmetric problems

**Reference:** Hammersley & Morton (1956), "A new Monte Carlo technique: antithetic variates"

### 2. Control Variates

**Concept:** Leverage correlation with a related variable that has a known analytical solution.

**Mathematical Foundation:**
For target Y with control X (known mean μₓ):

```
Y* = Y - β(X - μₓ)
```

where optimal β = Cov(Y,X) / Var(X)

**Variance Reduction:**
```
Var(Y*) = Var(Y)[1 - ρ²(Y,X)]
```

Can achieve **>90% variance reduction** for highly correlated controls.

**Implementation:**
```python
from src.models.black_scholes import monte_carlo_control_variate

price, conv_data, var_reduction = monte_carlo_control_variate(
    S=100, K=100, T=1, r=0.05, sigma=0.2,
    option_type='call',
    num_simulations=100000,
    track_convergence=True
)

print(f"Variance reduction: {var_reduction:.1f}%")
```

**When to Use:**
- An analytically solvable related problem exists
- Strong correlation between target and control
- Computational cost of control is minimal

**Reference:** Lavenberg & Welch (1981), "A perspective on the use of control variates"

### 3. Importance Sampling

**Concept:** Sample from a distribution that concentrates samples where they matter most.

**Mathematical Foundation:**
Change measure from P to Q:

```
E_P[f(X)] = E_Q[f(X) · dP/dQ]
```

**Best For:**
- Rare event simulation
- Tail probability estimation
- Problems with known important regions

### 4. Stratified Sampling

**Concept:** Partition sample space and sample proportionally from each stratum.

**Mathematical Foundation:**
For K strata with weights w_k:

```
Var(θ̂_strat) ≤ Var(θ̂_standard)
```

Equality only if no variation within strata.

**Best For:**
- Natural stratification exists
- Can estimate stratum probabilities
- Want guaranteed variance reduction

---

## Mathematical Greeks Reference

### Greek Symbols in Mathematics and Their Uses

| Symbol | Name | Primary Uses | Fields |
|--------|------|-------------|---------|
| α | alpha | Significance level (statistics), learning rate (ML), angles | Statistics, ML, Geometry |
| β | beta | Type II error, regression coefficients, angles | Statistics, Regression |
| γ, Γ | gamma | Euler constant (≈0.5772), Gamma function Γ(n) = (n-1)!, discount factor | Analysis, RL, Finance |
| δ, Δ | delta | Dirac delta, finite difference, variational derivative | Functional Analysis, Numerics |
| ε | epsilon | Small positive quantity in limits, error term, machine epsilon | Analysis, Numerical Methods |
| ζ | zeta | Riemann zeta function ζ(s) = Σ 1/nˢ | Number Theory |
| η | eta | Efficiency, viscosity, learning rate | Optimization, Physics |
| θ, Θ | theta | Angles, parameter vectors, asymptotic notation Θ(n) | Geometry, Statistics, CS |
| λ, Λ | lambda | Eigenvalues, Lagrange multipliers, wavelength, Poisson rate | Linear Algebra, Optimization |
| μ | mu | Mean (expected value), friction coefficient, Möbius function | Statistics, Physics |
| ν | nu | Degrees of freedom, frequency, kinematic viscosity | Statistics, Physics |
| ξ | xi | Random variables, Riemann xi function | Probability, Analysis |
| π, Π | pi | Circle constant (≈3.14159), product notation, prime counting | Geometry, Number Theory |
| ρ | rho | Correlation coefficient, density, spectral radius | Statistics, Physics |
| σ, Σ | sigma | Standard deviation, summation Σ, sigma algebra | Statistics, Measure Theory |
| τ | tau | Circle constant (2π), Kendall's tau, torque | Geometry, Statistics |
| φ, Φ | phi | Golden ratio (≈1.618), Euler totient, normal CDF | Number Theory, Statistics |
| χ | chi | Chi-squared distribution, Euler characteristic | Statistics, Topology |
| ψ, Ψ | psi | Wave function, digamma function ψ(x) = Γ'(x)/Γ(x) | Quantum Mechanics, Analysis |
| ω, Ω | omega | Angular frequency, sample space, complexity Ω(n) | Physics, Probability, CS |

### Important Mathematical Constants

| Constant | Symbol | Value | Definition |
|----------|--------|-------|------------|
| Pi | π | 3.14159... | Ratio of circumference to diameter |
| Tau | τ | 6.28318... | τ = 2π |
| Euler's number | e | 2.71828... | lim(1 + 1/n)ⁿ as n→∞ |
| Golden ratio | φ | 1.61803... | (1 + √5)/2 |
| Euler-Mascheroni | γ | 0.57721... | lim(Σ1/k - ln(n)) |

---

## Options Greeks Reference

### First-Order Greeks

#### Delta (Δ)
- **Formula:** ∂V/∂S
- **Meaning:** Rate of change of option value with respect to underlying asset price
- **Range:** [0, 1] for calls, [-1, 0] for puts
- **Interpretation:** Hedge ratio - number of shares to hold for delta-neutral hedge
- **At-the-Money:** ~0.5 for calls, ~-0.5 for puts

#### Vega (ν)
- **Formula:** ∂V/∂σ
- **Meaning:** Sensitivity to volatility (per 1% change)
- **Properties:** Always positive for long positions
- **Interpretation:** P&L change for 1% increase in implied volatility
- **Note:** Not actually a Greek letter; sometimes called kappa (κ)

#### Theta (Θ)
- **Formula:** ∂V/∂t (or -∂V/∂τ where τ = T - t)
- **Meaning:** Time decay of option value (per day)
- **Properties:** Typically negative for long positions
- **Interpretation:** Daily P&L from passage of time
- **Units:** Usually expressed per calendar day (/365)

#### Rho (ρ)
- **Formula:** ∂V/∂r
- **Meaning:** Sensitivity to interest rate (per 1% change)
- **Properties:** Positive for calls, negative for puts
- **Interpretation:** P&L change for 1% increase in interest rate
- **Note:** Often least important for equity options

### Second-Order Greeks

#### Gamma (Γ)
- **Formula:** ∂²V/∂S² = ∂Δ/∂S
- **Meaning:** Rate of change of delta with respect to underlying price
- **Properties:** Always positive, highest at-the-money
- **Interpretation:** Convexity of option value, frequency of hedge rebalancing
- **Units:** Change in delta per $1 move in underlying

#### Vomma (∂²V/∂σ²)
- **Alternative names:** Volga, vega convexity, DvegaDvol
- **Formula:** ∂Vega/∂σ = ∂²V/∂σ²
- **Meaning:** Second derivative with respect to volatility
- **Interpretation:** How vega changes as volatility changes
- **Application:** Important for volatility smile/skew trading

### Cross Greeks

#### Vanna (∂²V/∂S∂σ)
- **Formula:** ∂Delta/∂σ = ∂Vega/∂S
- **Meaning:** Cross derivative - sensitivity of delta to volatility
- **Interpretation:** How delta changes with volatility OR how vega changes with spot
- **Application:** Crucial for understanding volatility skew effects on delta hedging

#### Charm (∂²V/∂S∂t)
- **Alternative names:** Delta bleed, DdeltaDtime
- **Formula:** ∂Delta/∂t
- **Meaning:** Delta decay over time
- **Interpretation:** How delta changes as time passes
- **Application:** Predicting how hedges need adjustment over time

### Greeks Summary Table

| Greek | Symbol | Type | Formula | Measures Sensitivity To |
|-------|--------|------|---------|------------------------|
| Delta | Δ | First-order | ∂V/∂S | Underlying price |
| Gamma | Γ | Second-order | ∂²V/∂S² | Delta change |
| Vega | ν | First-order | ∂V/∂σ | Volatility |
| Theta | Θ | First-order | -∂V/∂t | Time decay |
| Rho | ρ | First-order | ∂V/∂r | Interest rate |
| Vomma | - | Second-order | ∂²V/∂σ² | Vega change |
| Vanna | - | Cross | ∂²V/∂S∂σ | Spot-vol interaction |
| Charm | - | Cross | ∂²V/∂S∂t | Delta decay |

---

## Terence Tao's Optimization Research

### AlphaEvolve: Mathematical Discovery at Scale

**Paper:** "Mathematical exploration and discovery at scale" (2024-2025)
**Authors:** Terence Tao, Bogdan Georgiev, Javier Gomez-Serrano, Adam Zsolt Wagner

**GitHub Repository:** [https://github.com/google-deepmind/alphaevolve_repository_of_problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)

### Key Contributions

1. **Problem Formulation**
   - Translated 67 diverse mathematical problems into optimization form
   - Bridged gap between pure mathematics and computational optimization

2. **AI-Powered Discovery**
   - Used AlphaEvolve (LLM-powered optimization tool) to attack problems
   - Iterative refinement using AI-generated candidate solutions
   - Mathematical verification of results

3. **Notable Achievement**
   - Improved asymptotic construction of finite field Nikodym sets
   - Published separate paper (November 2025) on this result
   - Demonstrates practical value of AI in mathematical research

### Methodology

```
1. Translate problem → Optimization formulation
2. Use LLM → Generate candidate solutions
3. Evaluate → Test mathematical validity
4. Refine → Iterate based on feedback
5. Verify → Prove results rigorously
```

### Connections to Options Pricing

The AlphaEvolve approach parallels variance reduction techniques:

| AlphaEvolve | Variance Reduction |
|-------------|-------------------|
| Problem reformulation | Transform to antithetic/control form |
| Iterative refinement | Optimize β in control variates |
| Mathematical verification | Prove variance reduction bounds |
| Scale across problems | Apply to different option types |

### Applications

- **Combinatorics:** Finite field problems
- **Number Theory:** Prime distributions
- **Analysis:** Convergence problems
- **Discrete Optimization:** Graph theory

---

## Implementation Guide

### Basic Usage

```python
from src.models.black_scholes import (
    black_scholes,
    monte_carlo_option_price,
    monte_carlo_antithetic,
    monte_carlo_control_variate,
    calculate_greeks
)

# Parameters
S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

# Analytical solution
bs_price = black_scholes(S, K, T, r, sigma, 'call')

# Standard Monte Carlo
mc_price, conv_data = monte_carlo_option_price(
    S, K, T, r, sigma, 'call', 100000, track_convergence=True
)

# Antithetic variates
anti_price, anti_conv, var_red = monte_carlo_antithetic(
    S, K, T, r, sigma, 'call', 50000, track_convergence=True
)

# Control variates
cv_price, cv_conv, cv_var_red = monte_carlo_control_variate(
    S, K, T, r, sigma, 'call', 100000, track_convergence=True
)

# Calculate all Greeks
greeks = calculate_greeks(S, K, T, r, sigma, 'call')
print(f"Delta: {greeks['delta']:.6f}")
print(f"Gamma: {greeks['gamma']:.6f}")
print(f"Vega: {greeks['vega']:.6f}")
```

### Visualizations

Run the interactive Marimo notebook:

```bash
marimo edit notebooks/optimization_comparison.py
```

This provides:
- Side-by-side convergence comparison
- Variance reduction metrics
- Interactive parameter exploration
- Export functionality for further research

### Mathematical Search Interface

Launch the search interface:

```bash
streamlit run src/gui/math_search.py
```

Features:
- Search 20+ mathematical Greek symbols
- Browse all options Greeks
- Explore optimization techniques
- NLP-powered semantic search (with TINKER_KEY)
- Export concepts to Sonnet 4.5 for deeper learning

---

## Performance Comparison

### Convergence Rates

| Method | Convergence Rate | Variance | Paths for ε Accuracy |
|--------|------------------|----------|----------------------|
| Standard MC | O(1/√n) | σ²/n | O(1/ε²) |
| Antithetic | O(1/√n) | ~σ²/(2n) | O(1/(2ε²)) |
| Control Variate | O(1/√n) | σ²(1-ρ²)/n | O((1-ρ²)/ε²) |

### Typical Variance Reductions

Based on empirical tests with at-the-money options:

| Technique | Typical Variance Reduction | Best Case | Overhead |
|-----------|----------------------------|-----------|----------|
| Antithetic Variates | 40-60% | ~70% (very smooth payoffs) | Minimal (~5%) |
| Control Variates | 60-90% | >95% (ρ ≈ 1) | Low (~10%) |
| Importance Sampling | Problem-dependent | >99% (tail events) | Moderate (20-50%) |
| Stratified Sampling | 30-70% | Guaranteed positive | Moderate (varies) |

### When to Use Each Method

**Antithetic Variates:**
- ✅ Always try first (minimal overhead)
- ✅ Convex/concave payoffs
- ✅ Symmetric problems
- ❌ Discontinuous payoffs

**Control Variates:**
- ✅ Related analytical solution available
- ✅ High correlation achievable
- ✅ Complex European options
- ❌ When no good control exists

**Importance Sampling:**
- ✅ Rare event simulation
- ✅ Deep out-of-the-money options
- ✅ Tail risk measurement
- ❌ Need to design good importance distribution

**Stratified Sampling:**
- ✅ Natural stratification
- ✅ Need guaranteed improvement
- ✅ When can estimate stratum probabilities
- ❌ High-dimensional problems (curse of dimensionality)

---

## References

### Variance Reduction
- Hammersley, J. M., & Morton, K. W. (1956). "A new Monte Carlo technique: antithetic variates"
- Lavenberg, S. S., & Welch, P. D. (1981). "A perspective on the use of control variates"
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.

### Options and Greeks
- Black, F., & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities"
- Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.)
- Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance*

### Terence Tao's Work
- Tao, T., et al. (2024-2025). "Mathematical exploration and discovery at scale"
- [What's New Blog](https://terrytao.wordpress.com/)
- [AlphaEvolve Repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems)

### Online Resources
- [Wikipedia: Variance Reduction](https://en.wikipedia.org/wiki/Variance_reduction)
- [Wikipedia: Antithetic Variates](https://en.wikipedia.org/wiki/Antithetic_variates)
- [arXiv.org](https://arxiv.org/) - Mathematics and Statistics preprints

---

*For questions or contributions, see the main README or open an issue on GitHub.*
