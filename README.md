# Final_Project
# Order Management System API

This is a simple RESTful API for managing customers, items, and orders in a store. The API is built using **FastAPI**, **SQLite**, and **Pydantic**.

### Features:
- **Customers**: Manage customer information (create, read, update, delete).
- **Items**: Manage items in the store (create, read, update, delete).
- **Orders**: Create, update, and view orders, with automatic price adjustments if the entered price is wrong.

---

## Setup

### Prerequisites:
- Python 3.8+
- SQLite (SQLite is used as the database)

## API Endpoints

### 1. **Create Order**

- **Endpoint**: `POST /orders`
- **Description**: Create a new order for a customer.
- **Request Body**:
    ```json
    {
        "customer_id": 1,
        "items": [
            {
                "name": "Item Name"
            }
        ],
        "notes": "Order Notes"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "message": "Order created successfully."
    }
    ```

### 2. **Update Order**

- **Endpoint**: `PUT /orders/{id}`
- **Description**: Update an existing order. Replaces old items with new items.
- **Request Body**:
    ```json
    {
        "customer_id": 1,
        "items": [
            {
                "name": "Updated Item Name"
            }
        ],
        "notes": "Updated order notes"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Order updated successfully."
    }
    ```

### 3. **Get Order by ID**

- **Endpoint**: `GET /orders/{id}`
- **Description**: Fetch the details of an order by its ID.
- **Response**:
    ```json
    {
        "id": 1,
        "customer_id": 1,
        "notes": "Order Notes",
        "items": [
            {
                "name": "Item Name",
                "price": 20.5
            }
        ]
    }
    ```

### 4. **Delete Order**

- **Endpoint**: `DELETE /orders/{id}`
- **Description**: Delete an order by its ID.
- **Response**:
    ```json
    {
        "message": "Order deleted successfully."
    }
    ```

### 5. **Create Customer**

- **Endpoint**: `POST /customers`
- **Description**: Create a new customer.
- **Request Body**:
    ```json
    {
        "name": "Customer Name",
        "phone": "123-456-7890"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Customer created successfully."
    }
    ```

### 6. **Get Customer by ID**

- **Endpoint**: `GET /customers/{id}`
- **Description**: Fetch customer details by their ID.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "Customer Name",
        "phone": "123-456-7890"
    }
    ```

### 7. **Update Customer**

- **Endpoint**: `PUT /customers/{id}`
- **Description**: Update customer details by their ID.
- **Request Body**:
    ```json
    {
        "name": "Updated Name",
        "phone": "987-654-3210"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Customer updated successfully."
    }
    ```

### 8. **Delete Customer**

- **Endpoint**: `DELETE /customers/{id}`
- **Description**: Delete a customer by their ID.
- **Response**:
    ```json
    {
        "message": "Customer deleted successfully."
    }
    ```

### 9. **Create Item**

- **Endpoint**: `POST /items`
- **Description**: Add a new item to the store.
- **Request Body**:
    ```json
    {
        "name": "Item Name",
        "price": 20.5
    }
    ```
- **Response**:
    ```json
    {
        "message": "Item created successfully."
    }
    ```

### 10. **Get Item by ID**

- **Endpoint**: `GET /items/{id}`
- **Description**: Get item details by its ID.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "Item Name",
        "price": 20.5
    }
    ```

### 11. **Update Item**

- **Endpoint**: `PUT /items/{id}`
- **Description**: Update item details by its ID.
- **Request Body**:
    ```json
    {
        "name": "Updated Item Name",
        "price": 30.5
    }
    ```
- **Response**:
    ```json
    {
        "message": "Item updated successfully."
    }
    ```

### 12. **Delete Item**

- **Endpoint**: `DELETE /items/{id}`
- **Description**: Delete an item by its ID.
- **Response**:
    ```json
    {
        "message": "Item deleted successfully."
    }
    ```

---

## Notes

- All prices for items in orders will be automatically adjusted if a wrong price is provided. The price will be fetched from the `items` table.
- The system handles customer and item data integrity, ensuring the relevant entities exist before creating orders or associating items.

---

