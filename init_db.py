import sqlite3

def init_db():
    """Initialize the database by creating necessary tables if they do not exist."""
    with sqlite3.connect("db.sqlite") as conn:
        cursor = conn.cursor()

        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL
            )
        """)

        # Create items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL
            )
        """)

        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL,
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)

        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
