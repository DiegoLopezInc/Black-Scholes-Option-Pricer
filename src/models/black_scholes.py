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