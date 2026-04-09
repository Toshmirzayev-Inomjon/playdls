from utils import load_orders, save_orders, new_order_id, now_str

# Yangi buyurtma yaratish
def add_order(user_id, item_name, price, username=None, amount=1, payment_method=None, note=None):
    orders = load_orders()

    order_id = new_order_id()
    orders[order_id] = {
        "user_id": user_id,
        "username": username,
        "item": item_name,
        "amount": amount,
        "price": price,
        "payment_method": payment_method,
        "status": "yangi",
        "note": note,
        "created_at": now_str()
    }

    save_orders(orders)
    return order_id

# Bitta buyurtmani olish
def get_order(order_id):
    orders = load_orders()
    return orders.get(order_id)

# Barcha buyurtmalarni olish
def all_orders():
    return load_orders()

# Buyurtma holatini yangilash
def update_order_status(order_id, status, admin_id=None):
    orders = load_orders()
    if order_id in orders:
        orders[order_id]['status'] = status
        if admin_id:
            orders[order_id]['admin_id'] = admin_id
        save_orders(orders)
        return True
    return False
