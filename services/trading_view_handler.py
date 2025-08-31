from tradingview_screener.column import col
from tradingview_screener.query import Query
from http.cookiejar import CookieJar
from utils.formatting import format_number
import requests

def authenticate(username: str, password: str) -> CookieJar:
    session = requests.Session()
    r = session.post(
       'https://www.tradingview.com/accounts/signin/', 
       headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.tradingview.com'}, 
       data={'username': username, 'password': password, 'remember': 'on'}, 
       timeout=60,
    )
    r.raise_for_status()
    if r.json().get('error'):
        raise Exception(f'Failed to authenticate: \n{r.json()}')
    return session.cookies

def screen_trading_view(pct_drop, cookies=None):
    q = (
        Query()
        .select(
            'name',
            'description',
            'sector',
            'market_cap_basic',
            'change',
            'change|5',
        )
        .where(
            col('exchange').isin(['AMEX', 'CBOE', 'NASDAQ', 'NYSE']),
            col('is_primary') == True,
            col('typespecs').has('common'),
            col('typespecs').has_none_of('preferred'),
            col('type') == 'stock',
            col('change|5') < pct_drop  # 5-day change > 7%
        )
        .order_by('market_cap_basic', ascending=False, nulls_first=False)
        .limit(3000)
        .set_markets('america')
        .set_property('preset', 'large_cap')
        .set_property('symbols', {'query': {'types': ['stock', 'fund', 'dr', 'structured']}})
    )
    _, df = q.get_scanner_data(cookies=cookies)

    df['market_cap_basic'] = df['market_cap_basic'].apply(format_number)

    return df