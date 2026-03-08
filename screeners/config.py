from screeners.drop_percent_screener import DropPercentScreener
from screeners.financials_screener import FinancialsScreener

SCREENERS = {
    'drop_7': DropPercentScreener(pct_drop=-7),
    'drop_5': DropPercentScreener(pct_drop=-5),
    'financials': FinancialsScreener(),
}
