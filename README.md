# FastAPI Order Management System

This project is a simple **Order Management System** built using Python's FastAPI framework and SQLite for data storage. The system allows you to manage customers, items, and orders efficiently through RESTful API endpoints.

## Features

- **Customer Management**: Add, view, update, and delete customer records.
- **Item Management**: Add, view, update, and delete item records.
- **Order Management**: Create, view, update, and delete orders. Automatically handle relationships between customers, items, and orders.

## Project Structure

The project is designed with simplicity and modularity in mind:

- **`main.py`**: Contains the FastAPI application with API endpoints for managing customers, items, and orders.
- **`init_db.py`**: Initializes the SQLite database by creating the required tables.
- **Database Schema**:
  - `customers`: Stores customer details (`id`, `name`, `phone`).
  - `items`: Stores item details (`id`, `name`, `price`).
  - `orders`: Stores order details (`id`, `customer_id`, `timestamp`, `notes`).
  - `order_items`: Stores the relationship between orders and items (`order_id`, `item_id`).
 
## API Endpoints

### Customer Endpoints
- **POST** `/customers`: Create a new customer.
- **GET** `/customers/{id}`: Retrieve customer details by ID.
- **PUT** `/customers/{id}`: Update customer details.
- **DELETE** `/customers/{id}`: Delete a customer.

### Item Endpoints
- **POST** `/items`: Add a new item to the menu.
- **GET** `/items/{id}`: Get item details by ID.
- **PUT** `/items/{id}`: Update an existing item in the menu.
- **DELETE** `/items/{id}`: Delete an item from the menu.

### Order Endpoints
- **POST** `/orders`: Create a new order for a customer with one or more items.
- **GET** `/orders/{id}`: Get order details, including items.
- **PUT** `/orders/{id}`: Update an existing order.
- **DELETE** `/orders/{id}`: Delete an order.


## How to Use

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up the Environment
Ensure you have Python 3.7+ installed. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### 3. Run the init_db.py script to create the necessary tables in the SQLite database:
```bash
pip install fastapi uvicorn
```

### 4. Start the Application
Run the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```

## Interact with the API

Once the application is running, you can interact with the API using tools like [Postman](https://www.postman.com/), [cURL](https://curl.se/), or directly through the interactive documentation provided by FastAPI.

### Accessing the Interactive API Documentation

FastAPI provides an automatic interactive interface for testing API endpoints:

1. Open your browser and go to:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

2. Use the interface to test API operations such as creating, retrieving, updating, and deleting customers, items, and orders.

## Notes

- All prices for items in orders will be automatically adjusted if a wrong price is provided. The price will be fetched from the `items` table.
- The system handles customer and item data integrity, ensuring the relevant entities exist before creating orders or associating items.

---


