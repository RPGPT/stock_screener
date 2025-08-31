import os
import pickle
import time

CACHE_FILE = "tv_cache.pkl"
CACHE_TTL = 1800  # 30 minutes

def load_cache():
    if os.path.exists(CACHE_FILE):
        mtime = os.path.getmtime(CACHE_FILE)
        if time.time() - mtime < CACHE_TTL:
            with open(CACHE_FILE, "rb") as f:
                return pickle.load(f)
    return None

def save_cache(df):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(df, f)