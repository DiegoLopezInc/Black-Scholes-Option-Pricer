import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return price

def monte_carlo_option_price(S, K, T, r, sigma, option_type='call', num_simulations=100000, track_convergence=True):
    """
    Price an option using Monte Carlo simulation with convergence tracking.

    Args:
        S: Current asset price
        K: Strike price
        T: Time to maturity
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        num_simulations: Number of Monte Carlo paths
        track_convergence: If True, returns convergence history

    Returns:
        If track_convergence=True: (price, convergence_data)
        If track_convergence=False: price
    """
    np.random.seed(42)

    # Generate random paths
    Z = np.random.standard_normal(num_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Calculate payoffs
    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    # Discount to present value
    discounted_payoffs = np.exp(-r * T) * payoffs

    if track_convergence:
        # Track convergence at logarithmic intervals
        convergence_data = {
            'iterations': [],
            'prices': [],
            'std_errors': [],
            'confidence_intervals': []
        }

        # Check points at powers of 2 and in between
        check_points = []
        for i in range(7, int(np.log2(num_simulations)) + 1):
            check_points.append(2**i)

        # Add final point
        if check_points[-1] != num_simulations:
            check_points.append(num_simulations)

        for n in check_points:
            subset = discounted_payoffs[:n]
            mean_price = np.mean(subset)
            std_error = np.std(subset) / np.sqrt(n)
            ci_95 = 1.96 * std_error

            convergence_data['iterations'].append(n)
            convergence_data['prices'].append(mean_price)
            convergence_data['std_errors'].append(std_error)
            convergence_data['confidence_intervals'].append(ci_95)

        final_price = np.mean(discounted_payoffs)
        return final_price, convergence_data

    return np.mean(discounted_payoffs)

def monte_carlo_antithetic(S, K, T, r, sigma, option_type='call', num_simulations=50000, track_convergence=True):
    """
    Monte Carlo with Antithetic Variates for variance reduction.

    Antithetic variates technique uses pairs of negatively correlated random variables
    to reduce variance. For each Z, we also use -Z, which often reduces variance by ~50%.

    Reference: Hammersley & Morton (1956), "A new Monte Carlo technique: antithetic variates"

    Args:
        S: Current asset price
        K: Strike price
        T: Time to maturity
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        num_simulations: Number of base simulations (total paths = 2 * num_simulations)
        track_convergence: If True, returns convergence history

    Returns:
        If track_convergence=True: (price, convergence_data, variance_reduction)
        If track_convergence=False: price
    """
    np.random.seed(42)

    # Generate random paths
    Z = np.random.standard_normal(num_simulations)

    # Standard paths
    ST_pos = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    # Antithetic paths (using -Z)
    ST_neg = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * (-Z))

    # Calculate payoffs for both
    if option_type == 'call':
        payoffs_pos = np.maximum(ST_pos - K, 0)
        payoffs_neg = np.maximum(ST_neg - K, 0)
    elif option_type == 'put':
        payoffs_pos = np.maximum(K - ST_pos, 0)
        payoffs_neg = np.maximum(K - ST_neg, 0)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    # Average antithetic pairs
    payoffs = (payoffs_pos + payoffs_neg) / 2
    discounted_payoffs = np.exp(-r * T) * payoffs

    # Calculate variance reduction
    var_standard = np.var(np.exp(-r * T) * payoffs_pos)
    var_antithetic = np.var(discounted_payoffs)
    variance_reduction = (1 - var_antithetic / var_standard) * 100 if var_standard > 0 else 0

    if track_convergence:
        convergence_data = {
            'iterations': [],
            'prices': [],
            'std_errors': [],
            'confidence_intervals': []
        }

        check_points = []
        for i in range(7, int(np.log2(num_simulations)) + 1):
            check_points.append(2**i)
        if check_points[-1] != num_simulations:
            check_points.append(num_simulations)

        for n in check_points:
            subset = discounted_payoffs[:n]
            mean_price = np.mean(subset)
            std_error = np.std(subset) / np.sqrt(n)
            ci_95 = 1.96 * std_error

            convergence_data['iterations'].append(n * 2)  # Total paths = 2n
            convergence_data['prices'].append(mean_price)
            convergence_data['std_errors'].append(std_error)
            convergence_data['confidence_intervals'].append(ci_95)

        final_price = np.mean(discounted_payoffs)
        return final_price, convergence_data, variance_reduction

    return np.mean(discounted_payoffs)

def monte_carlo_control_variate(S, K, T, r, sigma, option_type='call', num_simulations=100000, track_convergence=True):
    """
    Monte Carlo with Control Variate for variance reduction.

    Uses the geometric average Asian option as a control variate since it has a
    known analytical solution and is correlated with the European option.

    Reference: Lavenberg & Welch (1981), "A perspective on the use of control variates"

    Args:
        S: Current asset price
        K: Strike price
        T: Time to maturity
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        num_simulations: Number of Monte Carlo paths
        track_convergence: If True, returns convergence history

    Returns:
        If track_convergence=True: (price, convergence_data, variance_reduction)
        If track_convergence=False: price
    """
    np.random.seed(42)

    # Generate random paths
    Z = np.random.standard_normal(num_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Calculate European option payoffs (Y)
    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    discounted_payoffs = np.exp(-r * T) * payoffs

    # Control variate: Use the stock price itself
    # E[ST] = S * exp(r*T) is known analytically
    control_variate = ST
    expected_control = S * np.exp(r * T)

    # Optimal beta: cov(Y, X) / var(X)
    cov_yx = np.cov(discounted_payoffs, control_variate)[0, 1]
    var_x = np.var(control_variate)
    beta = cov_yx / var_x if var_x > 0 else 0

    # Control variate adjustment
    adjusted_payoffs = discounted_payoffs - beta * (control_variate - expected_control)

    # Calculate variance reduction
    var_standard = np.var(discounted_payoffs)
    var_cv = np.var(adjusted_payoffs)
    variance_reduction = (1 - var_cv / var_standard) * 100 if var_standard > 0 else 0

    if track_convergence:
        convergence_data = {
            'iterations': [],
            'prices': [],
            'std_errors': [],
            'confidence_intervals': []
        }

        check_points = []
        for i in range(7, int(np.log2(num_simulations)) + 1):
            check_points.append(2**i)
        if check_points[-1] != num_simulations:
            check_points.append(num_simulations)

        for n in check_points:
            subset = adjusted_payoffs[:n]
            mean_price = np.mean(subset)
            std_error = np.std(subset) / np.sqrt(n)
            ci_95 = 1.96 * std_error

            convergence_data['iterations'].append(n)
            convergence_data['prices'].append(mean_price)
            convergence_data['std_errors'].append(std_error)
            convergence_data['confidence_intervals'].append(ci_95)

        final_price = np.mean(adjusted_payoffs)
        return final_price, convergence_data, variance_reduction

    return np.mean(adjusted_payoffs)

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Calculate all Greeks for Black-Scholes options.

    Greeks are sensitivity measures of option prices to various parameters.
    They are essential for risk management and hedging strategies.

    Returns:
        Dictionary with all Greeks and their mathematical symbols
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    pdf_d1 = norm.pdf(d1)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = (-S * pdf_d1 * sigma / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        theta = (-S * pdf_d1 * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    # Greeks that are same for calls and puts
    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T)

    # Higher-order Greeks
    vomma = vega * d1 * d2 / sigma  # Volga, sensitivity of vega to volatility
    vanna = -pdf_d1 * d2 / sigma    # Sensitivity of delta to volatility
    charm = -pdf_d1 * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))  # Delta decay

    return {
        'price': price,
        'delta': delta,          # Δ - Rate of change of price with respect to underlying
        'gamma': gamma,          # Γ - Rate of change of delta with respect to underlying
        'vega': vega / 100,      # ν - Sensitivity to volatility (per 1% change)
        'theta': theta / 365,    # Θ - Time decay (per day)
        'rho': rho / 100,        # ρ - Sensitivity to interest rate (per 1% change)
        'vomma': vomma,          # 𝜕²V/𝜕σ² - Second derivative with respect to volatility
        'vanna': vanna,          # 𝜕²V/𝜕S𝜕σ - Cross derivative
        'charm': charm,          # 𝜕²V/𝜕S𝜕t - Delta decay over time
        'symbols': {
            'delta': 'Δ',
            'gamma': 'Γ',
            'vega': 'ν (nu)',
            'theta': 'Θ',
            'rho': 'ρ',
            'vomma': '∂²V/∂σ²',
            'vanna': '∂²V/∂S∂σ',
            'charm': '∂²V/∂S∂t'
        }
    }