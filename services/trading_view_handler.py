from tradingview_screener.column import col
from tradingview_screener.query import Query
from http.cookiejar import CookieJar
from utils.formatting import format_number
import requests

def authenticate(username: str, password: str) -> CookieJar:
    session = requests.Session()
    response = session.post(
        'https://www.tradingview.com/accounts/signin/',
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.tradingview.com'
        },
        data={'username': username, 'password': password, 'remember': 'on'},
        timeout=60,
    )
    response.raise_for_status()
    if response.json().get('error'):
        raise Exception(f'Authentication failed: {response.json()}')
    return session.cookies

def screen_trading_view(pct_drop=None, financials=False, cookies=None):
    query = Query()
    
    query.select(
        'name', 'description', 'sector', 'market_cap_basic', 'change',
        'change|5', 'change|30', 'change|60', 'change|90', 'change|26', 'change|52',
    )
    
    conditions = [
        col('exchange').isin(['AMEX', 'CBOE', 'NASDAQ', 'NYSE']),
        col('is_primary') == True,
        col('typespecs').has('common'),
        col('typespecs').has_none_of('preferred'),
        col('type') == 'stock',
    ]
    
    if pct_drop is not None:
        conditions.append(col('change|5') < pct_drop)
    
    if financials:
        conditions.append(col('change') > 0)
    
    query.where(*conditions)
    query.order_by('market_cap_basic', ascending=False, nulls_first=False)
    query.limit(3000)
    query.set_markets('america')
    query.set_property('preset', 'large_cap')
    query.set_property('symbols', {'query': {'types': ['stock', 'fund', 'dr', 'structured']}})
    
    _, df = query.get_scanner_data(cookies=cookies)
    df['market_cap_basic'] = df['market_cap_basic'].apply(format_number)
    
    return df