import os
import pickle
import time

CACHE_DIR = "cache"
CACHE_TTL = 1800

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_file(screener_key=None):
    if screener_key:
        return os.path.join(CACHE_DIR, f"tv_cache_{screener_key}.pkl")
    return os.path.join(CACHE_DIR, "tv_cache.pkl")

def load_cache(screener_key=None):
    cache_file = get_cache_file(screener_key)
    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime < CACHE_TTL:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
    return None

def save_cache(df, screener_key=None):
    cache_file = get_cache_file(screener_key)
    with open(cache_file, "wb") as f:
        pickle.dump(df, f)

def clear_all_cache():
    if os.path.exists(CACHE_DIR):
        for file in os.listdir(CACHE_DIR):
            if file.endswith('.pkl'):
                filepath = os.path.join(CACHE_DIR, file)
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")