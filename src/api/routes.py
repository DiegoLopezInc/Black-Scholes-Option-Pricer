from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.models.black_scholes import black_scholes, monte_carlo_option_price
from src.services.option_pricing_service import OptionPricingService
import numpy as np

app = FastAPI(title="Black-Scholes Option Pricer API")
option_service = OptionPricingService()

class OptionRequest(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str = 'call'

class MonteCarloRequest(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str = 'call'
    num_simulations: int = 100000

@app.get("/")
def read_root():
    return {"message": "Black-Scholes Option Pricer API", "version": "1.0"}

@app.post("/price")
def calculate_price(request: OptionRequest):
    """Calculate option price using Black-Scholes formula"""
    try:
        price = black_scholes(
            request.S, request.K, request.T,
            request.r, request.sigma, request.option_type
        )
        return {
            "price": float(price),
            "method": "black_scholes",
            "parameters": request.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/monte-carlo")
def monte_carlo_price(request: MonteCarloRequest):
    """Calculate option price using Monte Carlo simulation with convergence tracking"""
    try:
        price, convergence_data = monte_carlo_option_price(
            request.S, request.K, request.T,
            request.r, request.sigma, request.option_type,
            request.num_simulations, track_convergence=True
        )

        # Also calculate Black-Scholes for comparison
        bs_price = black_scholes(
            request.S, request.K, request.T,
            request.r, request.sigma, request.option_type
        )

        return {
            "monte_carlo_price": float(price),
            "black_scholes_price": float(bs_price),
            "difference": float(abs(price - bs_price)),
            "convergence_data": {
                "iterations": convergence_data['iterations'],
                "prices": [float(p) for p in convergence_data['prices']],
                "std_errors": [float(se) for se in convergence_data['std_errors']],
                "confidence_intervals": [float(ci) for ci in convergence_data['confidence_intervals']]
            },
            "method": "monte_carlo",
            "parameters": request.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/heatmap")
def generate_heatmap(request: OptionRequest, price_range: float = 0.2, vol_range: float = 0.5):
    """Generate heatmap data for option prices"""
    try:
        prices, vols, heatmap_data = option_service.generate_heatmap_data(
            request.S, request.K, request.T,
            request.r, request.sigma, request.option_type,
            price_range, vol_range
        )
        return {
            "prices": prices.tolist(),
            "volatilities": vols.tolist(),
            "heatmap_data": heatmap_data.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
