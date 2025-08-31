import streamlit as st
from services.trading_view_handler import screen_trading_view
from utils.cache import load_cache, save_cache
from models.column_map import COLUMN_MAP

cookies = {'sessionid': 'SESSION_ID_HERE'}  # Replace with your actual session ID

st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📈 Stock Screener")

def color_cell(val):
    try:
        val_float = float(str(val).replace('%', ''))
    except:
        val_float = 0
    color = 'green' if val_float > 0 else 'red' if val_float < 0 else 'black'
    val_rounded = f"{val_float:.2f} %" 
    return f'<span style="color:{color}; font-weight:bold">{val_rounded}</span>'

if st.button("Run Screener"):
    df = load_cache()
    if df is None:
        df = screen_trading_view(pct_drop=-7, cookies=cookies)
        save_cache(df)
        st.success("✅ Fetched new data!")
    else:
        st.info("📦 Loaded from cache.")

    if df.empty:
        st.warning("⚠️ No major stocks dropped more than 7% over the last 5 trading days.")
    else:
        df['TradingView Chart'] = df['ticker'].apply(
            lambda t: f"<a href='https://www.tradingview.com/chart/?symbol={t}' target='_blank'>Open Chart</a>"
        )
        df = df.drop(columns=['ticker'])
        df = df.rename(columns=COLUMN_MAP)

        df['Change Today'] = df['Change Today'].apply(color_cell)
        df['5-Day Change'] = df['5-Day Change'].apply(color_cell)

        st.subheader("Results")
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
else:
    st.write("👉 Click the button above to run the screener.")
