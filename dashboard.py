import streamlit as st
from services.trading_view_handler import screen_trading_view
from utils.cache import load_cache, save_cache, clear_all_cache
from models.column_map import COLUMN_MAP
from screeners.config import SCREENERS
import time
import pandas as pd

COOKIES = {'sessionid': 'SESSION_ID_HERE'}

st.set_page_config(page_title="Stock Screener", layout="wide")

title_col, options_col = st.columns([0.92, 0.08])

with title_col:
    st.title("📈 Stock Screener")

with options_col:
    st.write("")
    st.write("")
    with st.popover("⚙️", use_container_width=False):
        st.subheader("Options", anchor=False)
        session_id = st.text_input("Session ID", value=COOKIES.get('sessionid'), key="session_id_input")
        if session_id != COOKIES.get('sessionid'):
            COOKIES['sessionid'] = session_id
            st.success("✅ Session ID updated!")
        st.divider()
        if st.button("🗑️ Clear Cache", key="clear_cache_button", use_container_width=True):
            clear_all_cache()
            st.success("✅ Cache cleared!")

def get_percentage_style(value):
    try:
        num = float(str(value).replace('%', ''))
    except:
        num = 0
    
    if num > 0:
        return 'color: green; font-weight: bold'
    elif num < 0:
        return 'color: red; font-weight: bold'
    return 'color: black'

def format_market_cap(value):
    if pd.isna(value) or value == 0:
        return '0'
    num = float(value)
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(num) < 1000:
            result = f"{num:.2f}".rstrip('0').rstrip('.')
            return f"{result}{unit}"
        num /= 1000
    result = f"{num:.2f}".rstrip('0').rstrip('.')
    return f"{result}P"

PERCENTAGE_COLUMNS = [
    'Change Today', '5-Day Change', '1-Month Change',
    '2-Month Change', '3-Month Change', '6-Month Change', '1-Year Change'
]

def display_results(df, screener, from_cache=False):
    if df.empty:
        st.warning(screener.get_warning_message())
        return
    
    display_df = df.copy().rename(columns=COLUMN_MAP)
    
    for col in PERCENTAGE_COLUMNS:
        if col in display_df.columns:
            display_df[col] = display_df[col].fillna(0).round(2)
    
    st.subheader("Results")
    if from_cache:
        time.sleep(0.5)
    
    styled_df = display_df.style
    
    for col in PERCENTAGE_COLUMNS:
        if col in display_df.columns:
            styled_df = styled_df.format({col: "{:.2f}%"})
            styled_df = styled_df.map(get_percentage_style, subset=[col])
    
    if 'Market Cap' in display_df.columns:
        styled_df = styled_df.format({'Market Cap': format_market_cap})
    
    column_config = {col: st.column_config.NumberColumn(format="%.2f%%") for col in PERCENTAGE_COLUMNS if col in display_df.columns}
    
    st.dataframe(styled_df, column_config=column_config, width='stretch', hide_index=True)
    
    with st.expander("🔗 External Links"):
        for ticker in df['ticker']:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[📈 Yahoo: {ticker}](https://finance.yahoo.com/quote/{ticker.split(':')[1]})")
            with col2:
                st.markdown(f"[📊 TradingView: {ticker}](https://www.tradingview.com/chart/?symbol={ticker})")

st.subheader("Select a Screener")
col1, col2, col3 = st.columns(3)

screener_buttons = [
    (col1, '📉 Drop 7%', 'drop_7_button', 'drop_7'),
    (col2, '📉 Drop 5%', 'drop_5_button', 'drop_5'),
    (col3, '💰 Strong Financials', 'financials_button', 'financials'),
]

selected_screener_key = None
for col, label, key, screener_id in screener_buttons:
    with col:
        if st.button(label, key=key):
            selected_screener_key = screener_id

if selected_screener_key:
    screener = SCREENERS[selected_screener_key]
    criteria = screener.get_criteria()
    
    st.info(f"{screener.name} - {screener.description}")
    
    df = load_cache(screener_key=selected_screener_key)
    from_cache = df is not None
    
    if df is None:
        with st.spinner("📊 Fetching data..."):
            if 'pct_drop' in criteria:
                df = screen_trading_view(pct_drop=criteria['pct_drop'], cookies=COOKIES)
            elif criteria.get('financials'):
                df = screen_trading_view(financials=True, cookies=COOKIES)
        save_cache(df, screener_key=selected_screener_key)
        st.success("✅ Data fetched!")
    else:
        st.success("📦 Cached data")
    
    display_results(df, screener, from_cache=from_cache)
else:
    st.write("Select a screener above")
