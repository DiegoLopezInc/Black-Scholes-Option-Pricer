"""
Test script for variance reduction techniques
Tests antithetic variates and control variates methods
"""
import sys
sys.path.append('/home/user/Black-Scholes-Option-Pricer')

from src.models.black_scholes import (
    black_scholes,
    monte_carlo_option_price,
    monte_carlo_antithetic,
    monte_carlo_control_variate,
    calculate_greeks
)
import numpy as np

def test_variance_reduction():
    """Test all variance reduction techniques"""
    print("=" * 70)
    print("VARIANCE REDUCTION TECHNIQUES TEST")
    print("=" * 70)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    option_type = 'call'
    num_sims = 50000

    print(f"\nParameters: S={S}, K={K}, T={T}, r={r}, sigma={sigma}")
    print(f"Option type: {option_type}")
    print(f"Simulations: {num_sims:,}\n")

    # Analytical solution
    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    print(f"Black-Scholes (analytical): ${bs_price:.6f}\n")

    # Standard Monte Carlo
    print("Running Standard Monte Carlo...")
    mc_price, mc_conv = monte_carlo_option_price(
        S, K, T, r, sigma, option_type, num_sims
    )
    mc_error = abs(mc_price - bs_price)
    mc_final_std = mc_conv['std_errors'][-1]
    print(f"  Price: ${mc_price:.6f}")
    print(f"  Error: ${mc_error:.6f} ({mc_error/bs_price*100:.4f}%)")
    print(f"  Final Std Error: ${mc_final_std:.6f}\n")

    # Antithetic variates
    print("Running Antithetic Variates...")
    anti_price, anti_conv, var_red_anti = monte_carlo_antithetic(
        S, K, T, r, sigma, option_type, num_sims // 2
    )
    anti_error = abs(anti_price - bs_price)
    anti_final_std = anti_conv['std_errors'][-1]
    print(f"  Price: ${anti_price:.6f}")
    print(f"  Error: ${anti_error:.6f} ({anti_error/bs_price*100:.4f}%)")
    print(f"  Final Std Error: ${anti_final_std:.6f}")
    print(f"  Variance Reduction: {var_red_anti:.2f}%\n")

    # Control variates
    print("Running Control Variates...")
    cv_price, cv_conv, var_red_cv = monte_carlo_control_variate(
        S, K, T, r, sigma, option_type, num_sims
    )
    cv_error = abs(cv_price - bs_price)
    cv_final_std = cv_conv['std_errors'][-1]
    print(f"  Price: ${cv_price:.6f}")
    print(f"  Error: ${cv_error:.6f} ({cv_error/bs_price*100:.4f}%)")
    print(f"  Final Std Error: ${cv_final_std:.6f}")
    print(f"  Variance Reduction: {var_red_cv:.2f}%\n")

    # Comparison table
    print("=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print(f"{'Method':<20} {'Price':<12} {'Error':<12} {'Std Error':<12} {'Var Red %'}")
    print("-" * 70)
    print(f"{'Black-Scholes':<20} ${bs_price:<11.6f} {'-':<12} {'-':<12} {'-'}")
    print(f"{'Standard MC':<20} ${mc_price:<11.6f} ${mc_error:<11.6f} ${mc_final_std:<11.6f} {'baseline'}")
    print(f"{'Antithetic':<20} ${anti_price:<11.6f} ${anti_error:<11.6f} ${anti_final_std:<11.6f} {var_red_anti:.2f}%")
    print(f"{'Control Variate':<20} ${cv_price:<11.6f} ${cv_error:<11.6f} ${cv_final_std:<11.6f} {var_red_cv:.2f}%")
    print()

    # Check variance reduction
    assert var_red_anti > 0, "Antithetic variates should reduce variance"
    assert var_red_cv > 0, "Control variates should reduce variance"

    print("✅ All variance reduction tests passed!\n")

def test_greeks():
    """Test Greeks calculation"""
    print("=" * 70)
    print("GREEKS CALCULATION TEST")
    print("=" * 70)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

    print("\nCall Option Greeks:")
    call_greeks = calculate_greeks(S, K, T, r, sigma, 'call')

    for greek_name, value in call_greeks.items():
        if greek_name != 'symbols':
            symbol = call_greeks['symbols'].get(greek_name, '')
            print(f"  {greek_name.capitalize():<12} ({symbol:<15}): {value:>10.6f}")

    print("\nPut Option Greeks:")
    put_greeks = calculate_greeks(S, K, T, r, sigma, 'put')

    for greek_name, value in put_greeks.items():
        if greek_name != 'symbols':
            symbol = put_greeks['symbols'].get(greek_name, '')
            print(f"  {greek_name.capitalize():<12} ({symbol:<15}): {value:>10.6f}")

    # Verify put-call parity for delta
    call_delta = call_greeks['delta']
    put_delta = put_greeks['delta']
    delta_diff = call_delta - put_delta
    print(f"\nPut-Call Delta Relationship:")
    print(f"  Call Delta - Put Delta = {delta_diff:.6f}")
    print(f"  (Should be ≈ 1.0 for European options)")

    assert abs(delta_diff - 1.0) < 0.01, "Put-call delta relationship failed"

    print("\n✅ Greeks calculation tests passed!\n")

def test_convergence_tracking():
    """Test convergence tracking across methods"""
    print("=" * 70)
    print("CONVERGENCE TRACKING TEST")
    print("=" * 70)

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    num_sims = 10000

    # All methods should return convergence data
    _, mc_conv = monte_carlo_option_price(S, K, T, r, sigma, 'call', num_sims)
    _, anti_conv, _ = monte_carlo_antithetic(S, K, T, r, sigma, 'call', num_sims // 2)
    _, cv_conv, _ = monte_carlo_control_variate(S, K, T, r, sigma, 'call', num_sims)

    print(f"\nStandard MC checkpoints: {len(mc_conv['iterations'])}")
    print(f"Antithetic checkpoints: {len(anti_conv['iterations'])}")
    print(f"Control Variate checkpoints: {len(cv_conv['iterations'])}")

    # Verify convergence data structure
    for name, conv in [("Standard MC", mc_conv), ("Antithetic", anti_conv), ("CV", cv_conv)]:
        assert 'iterations' in conv
        assert 'prices' in conv
        assert 'std_errors' in conv
        assert 'confidence_intervals' in conv
        assert len(conv['iterations']) == len(conv['prices'])
        print(f"\n{name} convergence data structure: ✓")

    print("\n✅ Convergence tracking tests passed!\n")

if __name__ == "__main__":
    try:
        test_variance_reduction()
        test_greeks()
        test_convergence_tracking()

        print("=" * 70)
        print("✅ ALL OPTIMIZATION TESTS PASSED!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run optimization comparison: marimo edit notebooks/optimization_comparison.py")
        print("2. Launch math search: streamlit run src/gui/math_search.py")
        print("3. Read documentation: docs/OPTIMIZATION_TECHNIQUES.md")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
