from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

DB_FILE = "db.sqlite"


# Pydantic Models
class Customer(BaseModel):
    name: str
    phone: str


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    customer_id: int
    items: List[Item]
    notes: Optional[str] = None


def execute_query(query: str, params: tuple = (), fetchone: bool = False, fetchall: bool = False):
    """Helper function to execute queries and handle database connections."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return cursor.lastrowid


# Customer Endpoints
@app.post("/customers")
def create_customer(customer: Customer):
    try:
        query = "INSERT INTO customers (name, phone) VALUES (?, ?)"
        customer_id = execute_query(query, (customer.name, customer.phone))
        return {"id": customer_id, "message": "Customer created successfully."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")


@app.get("/customers/{id}")
def get_customer(id: int):
    query = "SELECT id, name, phone FROM customers WHERE id = ?"
    customer = execute_query(query, (id,), fetchone=True)
    if customer:
        return {"id": customer[0], "name": customer[1], "phone": customer[2]}
    raise HTTPException(status_code=404, detail="Customer not found.")


@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    query = "SELECT * FROM customers WHERE id = ?"
    existing_customer = execute_query(query, (id,), fetchone=True)

    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    query = "UPDATE customers SET name = ?, phone = ? WHERE id = ?"
    execute_query(query, (customer.name, customer.phone, id))
    
    return {"message": "Customer updated successfully."}


@app.delete("/customers/{id}")
def delete_customer(id: int):
    query = "SELECT * FROM customers WHERE id = ?"
    customer = execute_query(query, (id,), fetchone=True)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    query = "DELETE FROM customers WHERE id = ?"
    execute_query(query, (id,))
    
    return {"message": "Customer deleted successfully."}


# Item Endpoints
@app.post("/items")
def create_item(item: Item):
    query = "INSERT INTO items (name, price) VALUES (?, ?)"
    item_id = execute_query(query, (item.name, item.price))
    return {"id": item_id, "message": "Item created successfully."}


@app.get("/items/{id}")
def get_item(id: int):
    query = "SELECT id, name, price FROM items WHERE id = ?"
    item = execute_query(query, (id,), fetchone=True)
    if item:
        return {"id": item[0], "name": item[1], "price": item[2]}
    raise HTTPException(status_code=404, detail="Item not found.")


@app.put("/items/{id}")
def update_item(id: int, item: Item):
    query = "SELECT * FROM items WHERE id = ?"
    existing_item = execute_query(query, (id,), fetchone=True)

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found.")

    query = "UPDATE items SET name = ?, price = ? WHERE id = ?"
    execute_query(query, (item.name, item.price, id))
    
    return {"message": "Item updated successfully."}


@app.delete("/items/{id}")
def delete_item(id: int):
    query = "SELECT * FROM items WHERE id = ?"
    existing_item = execute_query(query, (id,), fetchone=True)
    
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found.")
    
    query = "DELETE FROM items WHERE id = ?"
    execute_query(query, (id,))
    
    return {"message": "Item deleted successfully."}


# Order Endpoints
@app.post("/orders")
def create_order(order: Order):
    query = "SELECT id FROM customers WHERE id = ?"
    customer = execute_query(query, (order.customer_id,), fetchone=True)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    
    query = "INSERT INTO orders (customer_id, notes, timestamp) VALUES (?, ?, strftime('%s', 'now'))"
    order_id = execute_query(query, (order.customer_id, order.notes or ""))

    price_adjustments = []  # To track price adjustments

    for item in order.items:
        item_query = "SELECT id, price FROM items WHERE name = ?"
        item_data = execute_query(item_query, (item.name,), fetchone=True)
        
        if item_data:
            item_id, correct_price = item_data
            if item.price != correct_price:
                price_adjustments.append(f"Item '{item.name}' price adjusted from {item.price} to {correct_price}.")
            
            insert_query = "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)"
            execute_query(insert_query, (order_id, item_id))
        else:
            raise HTTPException(status_code=404, detail=f"Item {item.name} not found.")
    
    response = {
        "id": order_id,
        "message": "Order created successfully."
    }
    
    if price_adjustments:
        response["price_adjustments"] = price_adjustments
    
    return response


@app.get("/orders/{id}")
def get_order(id: int):
    query = "SELECT o.id, o.customer_id, o.notes FROM orders o WHERE o.id = ?"
    order = execute_query(query, (id,), fetchone=True)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    item_query = "SELECT i.name, i.price FROM order_items oi JOIN items i ON oi.item_id = i.id WHERE oi.order_id = ?"
    items = execute_query(item_query, (id,), fetchall=True)
    
    return {
        "id": order[0],
        "customer_id": order[1],
        "notes": order[2],
        "items": [{"name": item[0], "price": item[1]} for item in items]
    }


@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    query = "UPDATE orders SET customer_id = ?, notes = ? WHERE id = ?"
    execute_query(query, (order.customer_id, order.notes or "", id))

    price_adjustments = []  # To track price adjustments

    delete_query = "DELETE FROM order_items WHERE order_id = ?"
    execute_query(delete_query, (id,))
    
    for item in order.items:
        item_query = "SELECT id, price FROM items WHERE name = ?"
        item_data = execute_query(item_query, (item.name,), fetchone=True)
        
        if item_data:
            item_id, correct_price = item_data
            if item.price != correct_price:
                price_adjustments.append(f"Item '{item.name}' price adjusted from {item.price} to {correct_price}.")
            
            insert_query = "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)"
            execute_query(insert_query, (id, item_id))
        else:
            raise HTTPException(status_code=404, detail=f"Item {item.name} not found.")

    response = {
        "id": id,
        "message": "Order updated successfully."
    }

    if price_adjustments:
        response["price_adjustments"] = price_adjustments

    return response

@app.delete("/orders/{id}")
def delete_order(id: int):
    # Check if the order exists
    query = "SELECT * FROM orders WHERE id = ?"
    order = execute_query(query, (id,), fetchone=True)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    # Proceed with deletion if the order exists
    query = "DELETE FROM orders WHERE id = ?"
    execute_query(query, (id,))
    
    return {"message": "Order deleted successfully."}

