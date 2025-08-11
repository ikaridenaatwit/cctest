#!/usr/bin/env python3


Requires:
  pip install mysql-connector-python

Run:
  python cli_driver.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple

import mysql.connector

# ---------------------------- DB Connection ---------------------------- #

def connect_to_db(host: str, port: int, user: str, password: str, database: str):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=False,
        )
        if conn.is_connected():
            print(f"\n✅ Connected to MySQL at {host}:{port}, DB={database}")
            return conn
    except mysql.connector.Error as err:
        print(f"\n❌ Error connecting to MySQL: {err}")
    return None


def prompt_connection() -> Dict[str, Any]:
    """Auto-select AWS RDS preset without prompting."""
    return {
        "host": "lease-link.cq7iaykk4axi.us-east-1.rds.amazonaws.com",
        "port": 3306,
        "user": "LeaseLinkadmin",
        "password": "leaselinkadmin",
        "database": "my_guitar_shop",
    }

# ---------------------------- Printing Helpers ---------------------------- #

def print_table(rows: List[dict]) -> None:
    if not rows:
        print("(no rows)")
        return
    headers = list(rows[0].keys())
    widths = [max(len(str(h)), *(len(str(r.get(h, ''))) for r in rows)) for h in headers]
    header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, widths))
    sep_line = "-+-".join("-" * w for w in widths)
    print(header_line)
    print(sep_line)
    for r in rows:
        print(" | ".join(f"{str(r.get(h, '')):<{w}}" for h, w in zip(headers, widths)))

# ---------------------------- Cart Model ---------------------------------- #

@dataclass
class CartItem:
    product_id: int
    qty: int

@dataclass
class Cart:
    items: Dict[int, CartItem] = field(default_factory=dict)

    def add(self, product_id: int, qty: int = 1):
        if product_id in self.items:
            self.items[product_id].qty += qty
        else:
            self.items[product_id] = CartItem(product_id, qty)

    def remove(self, product_id: int):
        self.items.pop(product_id, None)

    def clear(self):
        self.items.clear()

    def is_empty(self) -> bool:
        return not self.items

    def as_list(self) -> List[Tuple[int, int]]:
        return [(ci.product_id, ci.qty) for ci in self.items.values()]

# ---------------------------- Schema Helpers ------------------------------ #

def _column_exists(conn, table: str, column: str) -> bool:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND COLUMN_NAME = %s
        """,
        (table, column),
    )
    exists = cur.fetchone()[0] > 0
    cur.close()
    return bool(exists)

def _first_existing_column(conn, table: str, candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if _column_exists(conn, table, c):
            return c
    return None

def _address_columns(conn) -> dict:
    """
    Detect actual column names present in `addresses` and map to canonical keys:
    line1, city, state, postal (any may be None if missing in schema).
    """
    return {
        "line1":  _first_existing_column(conn, "addresses",
                    ["line1", "address1", "address_line1", "address_line_1", "street", "street1"]),
        "city":   _first_existing_column(conn, "addresses", ["city", "town"]),
        "state":  _first_existing_column(conn, "addresses", ["state", "province", "region"]),
        "postal": _first_existing_column(conn, "addresses",
                    ["postal_code", "zip_code", "zip", "postalcode", "postal"]),
    }

# ---------------------------- DB Accessors -------------------------------- #

def fetch_categories(conn) -> List[dict]:
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT category_id, category_name FROM categories ORDER BY category_name;")
    rows = cur.fetchall()
    cur.close()
    return rows

def fetch_products_by_category(conn, category_id: int) -> List[dict]:
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT product_id, product_name, list_price FROM products WHERE category_id=%s ORDER BY product_name;",
        (category_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows

def fetch_product(conn, product_id: int) -> Optional[dict]:
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT product_id, product_name, list_price FROM products WHERE product_id=%s;",
        (product_id,),
    )
    row = cur.fetchone()
    cur.close()
    return row

def get_or_create_customer(conn,
                           email: Optional[str] = None,
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None) -> int:
    """
    Finds or creates a customer. Uses email_address if available, else email if available,
    else falls back to name-only matching.
    """
    # Detect which email column (if any) exists
    email_col = None
    if _column_exists(conn, "customers", "email_address"):
        email_col = "email_address"
    elif _column_exists(conn, "customers", "email"):
        email_col = "email"

    cur = conn.cursor()

    # Try to find by email if possible
    if email_col and email:
        cur.execute(f"SELECT customer_id FROM customers WHERE {email_col}=%s;", (email,))
        row = cur.fetchone()
        if row:
            cur.close()
            return int(row[0])

    # Fallback lookup by name if no email column or no email provided
    if first_name or last_name:
        cur.execute(
            "SELECT customer_id FROM customers WHERE first_name=%s AND last_name=%s LIMIT 1;",
            (first_name or "Guest", last_name or "User"),
        )
        row = cur.fetchone()
        if row:
            cur.close()
            return int(row[0])

    # Create a new customer
    fn = first_name or "Guest"
    ln = last_name or "User"

    if email_col:
        cur.execute(
            f"INSERT INTO customers(first_name, last_name, {email_col}) VALUES (%s,%s,%s);",
            (fn, ln, email or "guest@example.com"),
        )
    else:
        cur.execute(
            "INSERT INTO customers(first_name, last_name) VALUES (%s,%s);",
            (fn, ln),
        )
    customer_id = cur.lastrowid
    conn.commit()
    cur.close()
    return int(customer_id)

def fetch_addresses(conn, customer_id: int) -> List[dict]:
    cols = _address_columns(conn)

    select_parts = ["address_id"]
    # alias to canonical names for consistent display
    if cols["line1"]:
        select_parts.append(f"{cols['line1']} AS line1")
    if cols["city"]:
        select_parts.append(f"{cols['city']} AS city")
    if cols["state"]:
        select_parts.append(f"{cols['state']} AS state")
    if cols["postal"]:
        select_parts.append(f"{cols['postal']} AS postal")

    sql = (
        f"SELECT {', '.join(select_parts)} "
        "FROM addresses WHERE customer_id=%s ORDER BY address_id;"
    )

    cur = conn.cursor(dictionary=True)
    cur.execute(sql, (customer_id,))
    rows = cur.fetchall()
    cur.close()
    return rows

def create_address(conn, customer_id: int, line1: str, city: str, state: str, postal: str) -> int:
    cols = _address_columns(conn)

    col_names = ["customer_id"]
    values = [customer_id]

    # Only insert the columns that actually exist
    if cols["line1"] and line1:
        col_names.append(cols["line1"]); values.append(line1)
    if cols["city"] and city:
        col_names.append(cols["city"]); values.append(city)
    if cols["state"] and state:
        col_names.append(cols["state"]); values.append(state)
    if cols["postal"] and postal:
        col_names.append(cols["postal"]); values.append(postal)

    if len(col_names) == 1:
        raise ValueError("No compatible address columns found in schema.")

    placeholders = ",".join(["%s"] * len(values))
    sql = f"INSERT INTO addresses({', '.join(col_names)}) VALUES ({placeholders});"

    cur = conn.cursor()
    cur.execute(sql, tuple(values))
    addr_id = cur.lastrowid
    conn.commit()
    cur.close()
    return int(addr_id)

def create_order(conn, customer_id: int, ship_address_id: int, cart: Cart) -> int:
    if cart.is_empty():
        raise ValueError("Cart is empty")

    cur = conn.cursor()
    try:
        # New order
        cur.execute(
            "INSERT INTO orders(customer_id, ship_address_id) VALUES (%s,%s);",
            (customer_id, ship_address_id),
        )
        order_id = int(cur.lastrowid)

        # Insert items using current prices from products
        for product_id, qty in cart.as_list():
            p = fetch_product(conn, product_id)
            if not p:
                raise ValueError(f"Product {product_id} not found")
            price = Decimal(str(p["list_price"]))
            cur.execute(
                "INSERT INTO order_items(order_id, product_id, quantity, item_price) VALUES (%s,%s,%s,%s);",
                (order_id, product_id, qty, price),
            )

        conn.commit()
        return order_id
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()

def list_orders(conn, customer_id: int) -> List[dict]:
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT o.order_id,
               o.order_date,
               ROUND(SUM(oi.quantity * oi.item_price), 2) AS total
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.customer_id = %s
        GROUP BY o.order_id, o.order_date
        ORDER BY o.order_date DESC;
        """,
        (customer_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows

def order_details(conn, order_id: int) -> List[dict]:
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT p.product_name,
               oi.quantity,
               oi.item_price,
               ROUND(oi.quantity * oi.item_price, 2) AS line_total
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        WHERE oi.order_id = %s
        ORDER BY p.product_name;
        """,
        (order_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows

# ---------------------------- UI Flows ------------------------------------ #

def pick_category(conn) -> Optional[int]:
    cats = fetch_categories(conn)
    if not cats:
        print("No categories found.")
        return None
    print("\nCategories:")
    print_table(cats)
    while True:
        raw = input("Enter category_id to browse (or blank to cancel): ").strip()
        if not raw:
            return None
        if raw.isdigit():
            cid = int(raw)
            if any(c["category_id"] == cid for c in cats):
                return cid
        print("Invalid category_id. Try again.")

def browse_products(conn, cart: Cart):
    cid = pick_category(conn)
    if cid is None:
        return
    prods = fetch_products_by_category(conn, cid)
    if not prods:
        print("No products in this category.")
        return
    print("\nProducts:")
    print_table(prods)
    while True:
        raw = input("Add product_id (or blank to stop): ").strip()
        if not raw:
            break
        if not raw.isdigit():
            print("Enter a numeric product_id.")
            continue
        pid = int(raw)
        if not any(p["product_id"] == pid for p in prods):
            print("That product_id is not in the list above.")
            continue
        qty_raw = input("Quantity [1]: ").strip() or "1"
        if not qty_raw.isdigit() or int(qty_raw) <= 0:
            print("Quantity must be a positive integer.")
            continue
        cart.add(pid, int(qty_raw))
        print("Added to cart.")

def view_cart(conn, cart: Cart):
    if cart.is_empty():
        print("\nYour cart is empty.")
        return
    rows: List[dict] = []
    total = Decimal("0.00")
    for pid, qty in cart.as_list():
        p = fetch_product(conn, pid)
        if not p:
            continue
        price = Decimal(str(p["list_price"]))
        line_total = price * qty
        total += line_total
        rows.append({
            "product_id": pid,
            "product_name": p["product_name"],
            "qty": qty,
            "price": f"{price:.2f}",
            "line_total": f"{line_total:.2f}",
        })
    print("\nCart:")
    print_table(rows)
    print(f"Total = ${total:.2f}")

def ensure_customer(conn) -> int:
    """Ask for name, and optional email if schema supports it; return customer_id."""
    has_email = _column_exists(conn, "customers", "email_address") or _column_exists(conn, "customers", "email")

    first = input("First name [Guest]: ").strip() or "Guest"
    last  = input("Last name [User]: ").strip() or "User"

    email = None
    if has_email:
        email = input("Email (optional; used to find/create): ").strip() or None

    cid = get_or_create_customer(conn, email=email, first_name=first, last_name=last)
    return cid

def pick_or_create_address(conn, customer_id: int) -> int:
    addrs = fetch_addresses(conn, customer_id)
    if addrs:
        print("\nYour addresses:")
        print_table(addrs)
    while True:
        choice = input("Use existing address_id or type 'new' to add one: ").strip()
        if choice.lower() == 'new':
            cols = _address_columns(conn)

            line1 = input("Line1: ").strip() if cols["line1"] else ""
            city  = input("City: ").strip()  if cols["city"]  else ""
            state = input("State: ").strip() if cols["state"] else ""
            postal= input("Postal/ZIP: ").strip() if cols["postal"] else ""

            if cols["line1"] and not line1:
                print("Line1 is required for your schema.")
                continue

            addr_id = create_address(conn, customer_id, line1, city, state, postal)
            print(f"Created address #{addr_id}.")
            return addr_id
        if choice.isdigit():
            aid = int(choice)
            if any(a["address_id"] == aid for a in addrs):
                return aid
            print("That address_id is not in your list.")
        else:
            print("Enter a numeric address_id or 'new'.")

def do_checkout(conn, cart: Cart):
    if cart.is_empty():
        print("Cart is empty.")
        return
    try:
        customer_id = ensure_customer(conn)
    except ValueError as e:
        print(e)
        return
    addr_id = pick_or_create_address(conn, customer_id)
    try:
        order_id = create_order(conn, customer_id, addr_id, cart)
        print(f"\n🎉 Order #{order_id} placed successfully!")
        details = order_details(conn, order_id)
        print_table(details)
        total = sum(Decimal(str(r["line_total"])) for r in details)
        print(f"Total charged: ${total:.2f}")
        cart.clear()
    except Exception as e:
        print(f"Checkout failed: {e}")

def show_orders(conn):
    try:
        customer_id = ensure_customer(conn)
    except ValueError as e:
        print(e)
        return
    orders = list_orders(conn, customer_id)
    if not orders:
        print("No orders found.")
        return
    print("\nYour orders:")
    print_table(orders)
    while True:
        raw = input("Enter order_id to view details (blank to exit): ").strip()
        if not raw:
            break
        if not raw.isdigit():
            print("Enter a valid order_id.")
            continue
        od = order_details(conn, int(raw))
        if not od:
            print("No such order or it has no items.")
            continue
        print_table(od)

# ---------------------------- Main Loop ----------------------------------- #

def main():
    print("\n=== Guitar Shop CLI ===")
    conn_info = prompt_connection()
    conn = connect_to_db(**conn_info)
    if not conn:
        print("Exiting. Could not connect to MySQL.")
        sys.exit(1)

    cart = Cart()

    try:
        while True:
            print("""
Menu:
  1) Browse products by category (add to cart)
  2) View cart
  3) Checkout
  4) View my orders
  5) Switch database connection
  6) Exit
""")
            choice = input("Select 1-6: ").strip()
            if choice == "1":
                browse_products(conn, cart)
            elif choice == "2":
                view_cart(conn, cart)
            elif choice == "3":
                do_checkout(conn, cart)
            elif choice == "4":
                show_orders(conn)
            elif choice == "5":
                try:
                    conn.close()
                except Exception:
                    pass
                conn_info = prompt_connection()
                conn = connect_to_db(**conn_info)
                if not conn:
                    print("Still not connected. Returning to menu…")
            elif choice == "6" or choice.lower() == "q":
                break
            else:
                print("Please choose a valid option.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        print("Goodbye!")

if __name__ == "__main__":
    main()
