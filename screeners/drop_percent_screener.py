from screeners.base_screener import BaseScreener

class DropPercentScreener(BaseScreener):
    def __init__(self, pct_drop: float):
        self.pct_drop = pct_drop
        name = f"Drop {abs(pct_drop)}%"
        description = f"Stocks dropped {abs(pct_drop)}% in 5 days"
        super().__init__(name, description)
    
    def get_criteria(self) -> dict:
        return {'pct_drop': self.pct_drop}
    
    def get_warning_message(self) -> str:
        return f"No stocks dropped {abs(self.pct_drop)}% in 5 days"
