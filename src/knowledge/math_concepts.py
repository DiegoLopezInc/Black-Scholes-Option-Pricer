"""
Mathematical Concepts Knowledge Base

This module contains a comprehensive mapping of mathematical concepts, optimization techniques,
Greeks (both financial and mathematical), and their interconnections.

Inspired by Terence Tao's work on mathematical discovery at scale using AlphaEvolve.
Reference: https://github.com/google-deepmind/alphaevolve_repository_of_problems
"""

MATHEMATICAL_GREEKS = {
    # Classical Greek Letters in Mathematics
    "alpha": {
        "symbol": "α",
        "uses": [
            "Significance level in statistics",
            "Learning rate in machine learning",
            "Angle in geometry",
            "First-order approximation",
            "Elasticity in economics"
        ],
        "fields": ["statistics", "machine_learning", "geometry", "economics"],
        "related_to": ["beta", "hypothesis_testing", "gradient_descent"]
    },
    "beta": {
        "symbol": "β",
        "uses": [
            "Type II error in statistics",
            "Regression coefficients",
            "Angle in geometry",
            "Beta function",
            "Financial asset correlation"
        ],
        "fields": ["statistics", "regression", "finance"],
        "related_to": ["alpha", "hypothesis_testing", "CAPM"]
    },
    "gamma": {
        "symbol": "γ, Γ",
        "uses": [
            "Euler-Mascheroni constant (γ ≈ 0.5772)",
            "Gamma function Γ(n) = (n-1)!",
            "Christoffel symbols in differential geometry",
            "Discount factor in reinforcement learning",
            "Option price convexity (finance)"
        ],
        "fields": ["analysis", "geometry", "reinforcement_learning", "finance"],
        "related_to": ["factorial", "delta", "calculus_of_variations"]
    },
    "delta": {
        "symbol": "δ, Δ",
        "uses": [
            "Dirac delta function",
            "Kronecker delta",
            "Finite difference Δx",
            "Variational derivative",
            "Option price sensitivity (finance)"
        ],
        "fields": ["functional_analysis", "numerical_methods", "finance"],
        "related_to": ["epsilon", "gamma", "derivatives"]
    },
    "epsilon": {
        "symbol": "ε",
        "uses": [
            "Small positive quantity in limits",
            "Error term in regression",
            "Permittivity in physics",
            "Machine epsilon in numerical analysis",
            "ε-greedy in reinforcement learning"
        ],
        "fields": ["analysis", "statistics", "numerical_analysis", "reinforcement_learning"],
        "related_to": ["delta", "limits", "approximation"]
    },
    "zeta": {
        "symbol": "ζ",
        "uses": [
            "Riemann zeta function ζ(s) = Σ 1/nˢ",
            "Weierstrass zeta function",
            "Dedekind zeta function"
        ],
        "fields": ["number_theory", "complex_analysis"],
        "related_to": ["prime_numbers", "riemann_hypothesis"]
    },
    "eta": {
        "symbol": "η",
        "uses": [
            "Efficiency parameter",
            "Viscosity in fluid dynamics",
            "Dirichlet eta function",
            "Learning rate in neural networks"
        ],
        "fields": ["optimization", "physics", "machine_learning"],
        "related_to": ["alpha", "gradient_descent"]
    },
    "theta": {
        "symbol": "θ, Θ",
        "uses": [
            "Angle measurement",
            "Parameter vector in statistics",
            "Big Theta notation (Θ(n))",
            "Option time decay (finance)",
            "Heaviside step function θ(x)"
        ],
        "fields": ["geometry", "statistics", "complexity_theory", "finance"],
        "related_to": ["parameters", "angles", "asymptotic_notation"]
    },
    "lambda": {
        "symbol": "λ, Λ",
        "uses": [
            "Eigenvalue",
            "Lagrange multiplier",
            "Wavelength in physics",
            "Rate parameter in Poisson distribution",
            "Lambda calculus"
        ],
        "fields": ["linear_algebra", "optimization", "probability", "computer_science"],
        "related_to": ["eigenvector", "optimization", "lagrangian"]
    },
    "mu": {
        "symbol": "μ",
        "uses": [
            "Mean (expected value)",
            "Friction coefficient",
            "Chemical potential",
            "Möbius function in number theory"
        ],
        "fields": ["statistics", "physics", "number_theory"],
        "related_to": ["sigma", "expected_value", "distributions"]
    },
    "nu": {
        "symbol": "ν",
        "uses": [
            "Degrees of freedom",
            "Frequency",
            "Kinematic viscosity",
            "Option vega (volatility sensitivity)"
        ],
        "fields": ["statistics", "physics", "finance"],
        "related_to": ["chi_square", "t_distribution", "vega"]
    },
    "xi": {
        "symbol": "ξ",
        "uses": [
            "Random variable",
            "Riemann xi function",
            "Damping ratio"
        ],
        "fields": ["probability", "analysis", "engineering"],
        "related_to": ["random_variables", "zeta_function"]
    },
    "pi": {
        "symbol": "π, Π",
        "uses": [
            "Circle constant π ≈ 3.14159",
            "Product notation Π",
            "Prime counting function π(x)",
            "Stationary distribution in Markov chains"
        ],
        "fields": ["geometry", "number_theory", "probability"],
        "related_to": ["e", "circle", "product"]
    },
    "rho": {
        "symbol": "ρ",
        "uses": [
            "Correlation coefficient",
            "Density",
            "Spectral radius",
            "Option interest rate sensitivity (finance)"
        ],
        "fields": ["statistics", "physics", "linear_algebra", "finance"],
        "related_to": ["correlation", "covariance"]
    },
    "sigma": {
        "symbol": "σ, Σ",
        "uses": [
            "Standard deviation",
            "Summation notation Σ",
            "Sigma algebra",
            "Stress in mechanics",
            "Volatility in finance"
        ],
        "fields": ["statistics", "measure_theory", "physics", "finance"],
        "related_to": ["mu", "variance", "normal_distribution"]
    },
    "tau": {
        "symbol": "τ",
        "uses": [
            "Circle constant τ = 2π",
            "Kendall's tau correlation",
            "Torque in physics",
            "Time constant"
        ],
        "fields": ["geometry", "statistics", "physics"],
        "related_to": ["pi", "correlation"]
    },
    "phi": {
        "symbol": "φ, Φ",
        "uses": [
            "Golden ratio φ = (1+√5)/2 ≈ 1.618",
            "Euler's totient function φ(n)",
            "Standard normal CDF Φ(x)",
            "Angle in spherical coordinates"
        ],
        "fields": ["number_theory", "geometry", "statistics"],
        "related_to": ["golden_ratio", "fibonacci", "normal_distribution"]
    },
    "chi": {
        "symbol": "χ",
        "uses": [
            "Chi-squared distribution",
            "Euler characteristic χ(X)",
            "Electric susceptibility"
        ],
        "fields": ["statistics", "topology", "physics"],
        "related_to": ["chi_square_test", "hypothesis_testing"]
    },
    "psi": {
        "symbol": "ψ, Ψ",
        "uses": [
            "Wave function in quantum mechanics",
            "Digamma function ψ(x) = Γ'(x)/Γ(x)",
            "Stream function in fluid dynamics"
        ],
        "fields": ["quantum_mechanics", "analysis", "physics"],
        "related_to": ["gamma_function", "quantum_states"]
    },
    "omega": {
        "symbol": "ω, Ω",
        "uses": [
            "Angular frequency",
            "Sample space Ω",
            "First uncountable ordinal ω₁",
            "Big Omega notation Ω(n)"
        ],
        "fields": ["physics", "probability", "set_theory", "complexity_theory"],
        "related_to": ["frequency", "probability_space", "asymptotic_notation"]
    }
}

OPTIONS_GREEKS = {
    "delta": {
        "symbol": "Δ",
        "formula": "∂V/∂S",
        "meaning": "Rate of change of option value with respect to underlying asset price",
        "range_call": "[0, 1]",
        "range_put": "[-1, 0]",
        "interpretation": "Hedge ratio - number of shares to hold to delta-hedge",
        "related_to": ["gamma", "hedging"]
    },
    "gamma": {
        "symbol": "Γ",
        "formula": "∂²V/∂S² = ∂Δ/∂S",
        "meaning": "Rate of change of delta with respect to underlying asset price",
        "properties": "Always positive, highest at-the-money",
        "interpretation": "Convexity of option value, indicates how often hedge needs rebalancing",
        "related_to": ["delta", "convexity"]
    },
    "vega": {
        "symbol": "ν (sometimes 𝓥)",
        "formula": "∂V/∂σ",
        "meaning": "Sensitivity to volatility (per 1% change)",
        "properties": "Always positive for long positions",
        "interpretation": "Exposure to implied volatility changes",
        "note": "Not actually a Greek letter; sometimes called kappa (κ)",
        "related_to": ["volatility", "vomma"]
    },
    "theta": {
        "symbol": "Θ",
        "formula": "∂V/∂t",
        "meaning": "Time decay of option value (per day)",
        "properties": "Typically negative for long positions",
        "interpretation": "Daily P&L from passage of time",
        "related_to": ["time_value", "charm"]
    },
    "rho": {
        "symbol": "ρ",
        "formula": "∂V/∂r",
        "meaning": "Sensitivity to interest rate (per 1% change)",
        "properties": "Positive for calls, negative for puts",
        "interpretation": "Impact of interest rate changes on option value",
        "related_to": ["interest_rates", "carry"]
    },
    "vomma": {
        "symbol": "∂²V/∂σ²",
        "formula": "∂Vega/∂σ",
        "meaning": "Second derivative with respect to volatility",
        "alternative_names": ["volga", "vega convexity"],
        "interpretation": "How vega changes as volatility changes",
        "related_to": ["vega", "volatility_smile"]
    },
    "vanna": {
        "symbol": "∂²V/∂S∂σ",
        "formula": "∂Delta/∂σ = ∂Vega/∂S",
        "meaning": "Cross derivative - sensitivity of delta to volatility",
        "interpretation": "How delta changes with volatility or how vega changes with spot",
        "related_to": ["delta", "vega", "volatility_skew"]
    },
    "charm": {
        "symbol": "∂²V/∂S∂t",
        "formula": "∂Delta/∂t",
        "meaning": "Delta decay over time",
        "alternative_names": ["delta bleed"],
        "interpretation": "How delta changes as time passes",
        "related_to": ["delta", "theta"]
    }
}

OPTIMIZATION_TECHNIQUES = {
    "variance_reduction": {
        "category": "Monte Carlo Methods",
        "techniques": {
            "antithetic_variates": {
                "description": "Use paired simulations with negatively correlated random variables",
                "variance_reduction": "~50% for smooth functions",
                "complexity": "O(1) overhead",
                "reference": "Hammersley & Morton (1956)",
                "best_for": ["symmetric problems", "smooth payoffs"]
            },
            "control_variates": {
                "description": "Use correlated variable with known expectation to reduce variance",
                "variance_reduction": "Depends on correlation, can be >90%",
                "complexity": "O(1) overhead",
                "reference": "Lavenberg & Welch (1981)",
                "best_for": ["when analytical solutions available for related problems"]
            },
            "importance_sampling": {
                "description": "Sample from alternative distribution to reduce variance in tails",
                "variance_reduction": "Problem-dependent, can be dramatic",
                "complexity": "Requires density ratio calculation",
                "best_for": ["rare event simulation", "tail probabilities"]
            },
            "stratified_sampling": {
                "description": "Partition sample space and sample proportionally from each stratum",
                "variance_reduction": "Guarantees reduction",
                "complexity": "Requires stratification scheme",
                "best_for": ["when stratification is natural"]
            }
        }
    },
    "gradient_methods": {
        "category": "Optimization",
        "techniques": {
            "gradient_descent": {
                "update_rule": "x_{t+1} = x_t - α∇f(x_t)",
                "convergence": "O(1/t) for convex, exp for strongly convex",
                "hyperparameters": ["learning rate α"],
                "variants": ["batch", "stochastic", "mini-batch"]
            },
            "momentum": {
                "update_rule": "v_{t+1} = βv_t + ∇f(x_t), x_{t+1} = x_t - αv_{t+1}",
                "benefit": "Accelerates in consistent directions, dampens oscillations",
                "hyperparameters": ["learning rate α", "momentum β"]
            },
            "adam": {
                "description": "Adaptive Moment Estimation",
                "combines": ["momentum", "RMSprop"],
                "hyperparameters": ["α", "β₁", "β₂", "ε"],
                "reference": "Kingma & Ba (2014)"
            }
        }
    },
    "tao_alphaevolve": {
        "category": "AI-Assisted Mathematical Discovery",
        "description": "LLM-powered optimization tool for mathematical problem solving",
        "paper": "Mathematical exploration and discovery at scale",
        "authors": ["Terence Tao", "Bogdan Georgiev", "Javier Gomez-Serrano", "Adam Zsolt Wagner"],
        "github": "https://github.com/google-deepmind/alphaevolve_repository_of_problems",
        "problems_studied": 67,
        "key_achievement": "Improved asymptotic construction of finite field Nikodym sets",
        "methodology": [
            "Translate problems to optimization form",
            "Use LLM to generate candidate solutions",
            "Iteratively refine using feedback",
            "Verify results mathematically"
        ],
        "applications": ["combinatorics", "number_theory", "analysis", "discrete_optimization"]
    }
}

MATHEMATICAL_CONCEPTS = {
    "convergence": {
        "types": {
            "pointwise": "f_n(x) → f(x) for each x",
            "uniform": "sup|f_n(x) - f(x)| → 0",
            "L^p": "∫|f_n - f|^p → 0",
            "in_distribution": "F_n → F weakly",
            "almost_sure": "P(lim f_n = f) = 1"
        },
        "related_to": ["limits", "sequences", "series"],
        "applications": ["analysis", "probability", "numerical_methods"]
    },
    "ergodic_theory": {
        "description": "Study of dynamical systems with invariant measure",
        "key_theorem": "Birkhoff ergodic theorem",
        "applications": ["statistical_mechanics", "number_theory", "probability"],
        "connection_to_tao": "Studied in additive combinatorics and arithmetic progressions"
    },
    "fourier_analysis": {
        "transform": "f̂(ξ) = ∫f(x)e^{-2πixξ}dx",
        "inverse": "f(x) = ∫f̂(ξ)e^{2πixξ}dξ",
        "applications": ["signal_processing", "PDE", "number_theory"],
        "greeks_used": ["ξ", "π", "ω"]
    },
    "information_theory": {
        "entropy": "H(X) = -Σ p(x)log p(x)",
        "mutual_information": "I(X;Y) = H(X) - H(X|Y)",
        "applications": ["machine_learning", "compression", "statistics"],
        "greeks_used": ["epsilon", "delta"]
    }
}

CROSS_DISCIPLINARY_CONNECTIONS = {
    "options_to_physics": {
        "black_scholes_heat_equation": "Options PDE is heat equation with change of variables",
        "path_integral": "Option pricing as Feynman path integral",
        "greeks_as_derivatives": "Financial Greeks analogous to physical derivatives"
    },
    "optimization_to_machine_learning": {
        "gradient_descent": "Core of backpropagation",
        "variance_reduction": "Used in stochastic gradient descent",
        "control_variates": "Baseline methods in reinforcement learning"
    },
    "number_theory_to_cryptography": {
        "modular_arithmetic": "RSA encryption",
        "prime_numbers": "Key generation",
        "discrete_log": "Elliptic curve cryptography"
    }
}

def search_concepts(query: str, max_results: int = 10):
    """
    Search mathematical concepts by keyword.

    Args:
        query: Search string
        max_results: Maximum number of results to return

    Returns:
        List of relevant concepts with their details
    """
    query_lower = query.lower()
    results = []

    # Search in mathematical Greeks
    for name, details in MATHEMATICAL_GREEKS.items():
        if query_lower in name or query_lower in str(details).lower():
            results.append({
                'type': 'mathematical_greek',
                'name': name,
                'details': details
            })

    # Search in options Greeks
    for name, details in OPTIONS_GREEKS.items():
        if query_lower in name or query_lower in str(details).lower():
            results.append({
                'type': 'options_greek',
                'name': name,
                'details': details
            })

    # Search in optimization techniques
    for category, details in OPTIMIZATION_TECHNIQUES.items():
        if query_lower in category or query_lower in str(details).lower():
            results.append({
                'type': 'optimization',
                'category': category,
                'details': details
            })

    # Search in mathematical concepts
    for concept, details in MATHEMATICAL_CONCEPTS.items():
        if query_lower in concept or query_lower in str(details).lower():
            results.append({
                'type': 'concept',
                'name': concept,
                'details': details
            })

    return results[:max_results]

def get_related_concepts(concept_name: str):
    """Get concepts related to a given concept."""
    related = []

    # Check mathematical Greeks
    if concept_name in MATHEMATICAL_GREEKS:
        related_names = MATHEMATICAL_GREEKS[concept_name].get('related_to', [])
        for name in related_names:
            if name in MATHEMATICAL_GREEKS:
                related.append({'type': 'mathematical_greek', 'name': name})

    # Check options Greeks
    if concept_name in OPTIONS_GREEKS:
        related_names = OPTIONS_GREEKS[concept_name].get('related_to', [])
        for name in related_names:
            if name in OPTIONS_GREEKS:
                related.append({'type': 'options_greek', 'name': name})

    return related

def export_to_sonnet_prompt(concept_data):
    """
    Export concept data as a markdown prompt for Claude Sonnet 4.5.

    Args:
        concept_data: Dictionary containing concept information

    Returns:
        Markdown-formatted prompt string
    """
    markdown = "# Mathematical Concept Research Prompt\n\n"
    markdown += "## Query Summary\n\n"
    markdown += f"Please help me understand the following mathematical concept in depth:\n\n"
    markdown += f"**Concept:** {concept_data.get('name', 'Unknown')}\n\n"

    if 'details' in concept_data:
        markdown += "## Known Information\n\n"
        markdown += f"```\n{concept_data['details']}\n```\n\n"

    markdown += "## Questions to Explore\n\n"
    markdown += "1. What are the fundamental principles and historical development?\n"
    markdown += "2. How is this concept applied in practice across different fields?\n"
    markdown += "3. What are common misconceptions or pitfalls?\n"
    markdown += "4. Can you provide concrete examples with worked solutions?\n"
    markdown += "5. What are the most important related theorems or results?\n"
    markdown += "6. How does this connect to modern research or applications?\n\n"

    markdown += "## Output Format\n\n"
    markdown += "Please provide:\n"
    markdown += "- Clear explanations suitable for someone with mathematical maturity\n"
    markdown += "- Concrete examples with step-by-step solutions\n"
    markdown += "- References to key papers or textbooks\n"
    markdown += "- Connections to related concepts\n\n"

    markdown += "---\n"
    markdown += "*Generated by Black-Scholes Mathematical Knowledge System*\n"
    markdown += "*Copy this prompt and paste it to Claude Sonnet 4.5 for detailed analysis*\n"

    return markdown
