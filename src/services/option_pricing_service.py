from src.models.black_scholes import black_scholes
import numpy as np

class OptionPricingService:
    def __init__(self):
        pass

    def calculate_option_prices(self, S, K, T, r, sigma, option_type):
        return black_scholes(S, K, T, r, sigma, option_type)

    def generate_heatmap_data(self, S, K, T, r, sigma, option_type, price_range=0.2, vol_range=0.5):
        prices = np.linspace(S * (1 - price_range), S * (1 + price_range), 50)
        vols = np.linspace(sigma * (1 - vol_range), sigma * (1 + vol_range), 50)
        
        heatmap_data = np.zeros((len(vols), len(prices)))
        
        for i, vol in enumerate(vols):
            for j, price in enumerate(prices):
                heatmap_data[i, j] = self.calculate_option_prices(price, K, T, r, vol, option_type)
        
        return prices, vols, heatmap_data