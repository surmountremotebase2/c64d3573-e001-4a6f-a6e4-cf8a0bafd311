from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Define the tickers you intend to use in your strategy
        self.tickers = ["AAPL", "GOOG"]

    @property
    def assets(self):
        # Specify the assets that your strategy will trade
        return self.tickers

    @property
    def interval(self):
        # Set the data interval to 1 hour, as required for this strategy
        return "1hour"

    def run(self, data):
        # Initialize allocation equally among assets (this can be adjusted)
        allocation_dict = {"AAPL": 0.5, "GOOG": 0.5}

        # Calculate the short and long EMAs for both AAPL and GOOG
        aapl_ema_short = EMA("AAPL", data["ohlcv"], length=12)
        aapl_ema_long = EMA("AAPL", data["ohlcv"], length=26)
        goog_ema_short = EMA("GOOG", data["ohlcv"], length=12)
        goog_ema_long = EMA("GOOG", data["ohlcv"], length=26)

        # Check if EMA lists are filled to ensure calculations can be made
        if aapl_ema_short and aapl_ema_long and goog_ema_short and goog_ema_long:
            # Calculate the latest divergence for both AAPL and GOOG
            aapl_divergence = aapl_ema_short[-1] - aapl_ema_long[-1]
            goog_divergence = goog_ema_short[-1] - goog_ema_long[-1]

            # Logic to adjust allocations based on the divergence
            # If AAPL underperforms GOOG (i.e., AAPL divergence is less than GOOG's), increase allocation to AAPL
            if aapl_divergence < goog_divergence:
                allocation_dict["AAPL"] = 0.6  # Adjust allocation as required
                allocation_dict["GOOG"] = 0.4
            # Conversely, if GOOG underperforms AAPL, increase allocation to GOOG
            elif goog_divergence < aapl_divergence:
                allocation_dict["AAPL"] = 0.4
                allocation_dict["GOOG"] = 0.6
            # Log the divergence for both stocks for observation
            log(f"AAPL Divergence: {aapl_divergence}, GOOG Divergence: {goog_divergence}")

        # The TargetAllocation object takes a dictionary with tickers as keys and their respective allocations as values
        return TargetAllocation(allocation_dict)