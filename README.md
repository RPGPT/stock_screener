# 📈 Stock Screener

A simple, interactive stock screener web app built with [Streamlit](https://streamlit.io/) that uses TradingView's API to find major stocks that have dropped more than 7% over the last 5 trading days.

---

## Features

- Screens major stocks using TradingView data
- Highlights stocks with significant drops
- Direct links to TradingView charts
- Caching for faster repeated queries
- Clean UI powered by Streamlit

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [requests](https://pypi.org/project/requests/)
- [pandas](https://pandas.pydata.org/)
- [TradingView Screener API (unofficial)](https://github.com/StreamAlpha/TradingView-API)  

---

## Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/RPGPT/stock_screener.git
    cd stock_screener
    ```

2. **Install dependencies:**
    ```
    pip install streamlit pandas requests tradingview_screener
    ```

3. **Set your TradingView session cookie:**
    - Open `dashboard.py` and replace `'SESSION_ID_HERE'` with your actual TradingView session ID.

---

## Usage

1. **Run the app using Streamlit:**
```
python -m streamlit run dashboard.py
```

2. **If that doesn't work, try this alternative:**
```
python -m streamlit run dashboard.py
```

Dashboard will be hosted on port `8501` by default.
---

## Notes

- The UI is built using [Streamlit](https://streamlit.io/).
- You need a valid TradingView session cookie for data access.
- This project is for educational purposes and is not affiliated with TradingView.

---

## License

MIT License

---

*Happy screening!*