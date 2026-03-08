from screeners.base_screener import BaseScreener

class FinancialsScreener(BaseScreener):
    def __init__(self):
        super().__init__(
            "Strong Financials",
            "Stocks with positive daily gains"
        )
    
    def get_criteria(self) -> dict:
        return {'financials': True}
    
    def get_warning_message(self) -> str:
        return "No stocks with positive daily gains"
