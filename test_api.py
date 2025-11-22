"""
Quick test script for Black-Scholes API endpoints
Run this to verify the API is working correctly
"""
import sys
sys.path.append('/home/user/Black-Scholes-Option-Pricer')

from src.models.black_scholes import black_scholes, monte_carlo_option_price
import json

def test_black_scholes():
    """Test Black-Scholes pricing"""
    print("=" * 60)
    print("Testing Black-Scholes Pricing")
    print("=" * 60)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

    call_price = black_scholes(S, K, T, r, sigma, 'call')
    put_price = black_scholes(S, K, T, r, sigma, 'put')

    print(f"Parameters: S={S}, K={K}, T={T}, r={r}, sigma={sigma}")
    print(f"Call Option Price: ${call_price:.6f}")
    print(f"Put Option Price: ${put_price:.6f}")
    print(f"Put-Call Parity Check: {abs((call_price - put_price) - (S - K * (1 + r)**(-T))) < 0.01}")
    print()

def test_monte_carlo():
    """Test Monte Carlo with convergence tracking"""
    print("=" * 60)
    print("Testing Monte Carlo Convergence")
    print("=" * 60)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    num_sims = 50000

    print(f"Running {num_sims:,} simulations...")
    mc_price, conv_data = monte_carlo_option_price(
        S, K, T, r, sigma, 'call', num_sims, track_convergence=True
    )
    bs_price = black_scholes(S, K, T, r, sigma, 'call')

    print(f"\nResults:")
    print(f"  Black-Scholes Price: ${bs_price:.6f}")
    print(f"  Monte Carlo Price:   ${mc_price:.6f}")
    print(f"  Difference:          ${abs(mc_price - bs_price):.6f}")
    print(f"  Relative Error:      {abs(mc_price - bs_price)/bs_price * 100:.4f}%")

    print(f"\nConvergence Tracking:")
    print(f"  Checkpoints: {len(conv_data['iterations'])}")
    print(f"  Final Std Error: ${conv_data['std_errors'][-1]:.6f}")
    print(f"  Final 95% CI: ±${conv_data['confidence_intervals'][-1]:.6f}")

    print(f"\nLast 3 Convergence Points:")
    print(f"  {'Iterations':<12} {'Price':<12} {'Std Error':<12} {'95% CI':<12}")
    print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*12}")
    for i in range(-3, 0):
        print(f"  {conv_data['iterations'][i]:<12,} "
              f"${conv_data['prices'][i]:<11.6f} "
              f"${conv_data['std_errors'][i]:<11.6f} "
              f"±${conv_data['confidence_intervals'][i]:.6f}")
    print()

def test_convergence_quality():
    """Test convergence quality metrics"""
    print("=" * 60)
    print("Testing Convergence Quality")
    print("=" * 60)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    bs_price = black_scholes(S, K, T, r, sigma, 'call')

    print(f"Black-Scholes benchmark: ${bs_price:.6f}\n")
    print(f"{'Simulations':<15} {'MC Price':<12} {'Error %':<10} {'Status'}")
    print(f"{'-'*15} {'-'*12} {'-'*10} {'-'*20}")

    for num_sims in [1000, 10000, 50000, 100000]:
        mc_price = monte_carlo_option_price(
            S, K, T, r, sigma, 'call', num_sims, track_convergence=False
        )
        error_pct = abs(mc_price - bs_price) / bs_price * 100
        status = "✓ Good" if error_pct < 1 else "⚠ High error"
        print(f"{num_sims:<15,} ${mc_price:<11.6f} {error_pct:<9.4f}% {status}")
    print()

if __name__ == "__main__":
    try:
        test_black_scholes()
        test_monte_carlo()
        test_convergence_quality()

        print("=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run API server: python -m src.api.routes")
        print("2. Run Streamlit: streamlit run src/gui/streamlit_app.py")
        print("3. Run Marimo notebook: marimo edit notebooks/model_validation.py")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
