# utils.py
import json
import os
from datetime import datetime
from config import ORDERS_FILE

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def new_order_id():
    # unik id: YYYYMMDDHHMMSSffffff
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

def now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
