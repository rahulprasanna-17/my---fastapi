from fastapi import FastAPI, Header, HTTPException, Request, File, UploadFile
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

API_KEY = "rahul1234"

@app.middleware("http")
async def main_entrance_guard(request: Request, call_next):
    start_time = time.time()
    print(f"Someone is visiting: {request.url}")
    response = await call_next(request)
    end_time = time.time()
    print(f"Request took: {end_time - start_time} seconds")
    return response

def create_table():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            food TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

class Order(BaseModel):
    name: str
    food: str

class UpdateOrder(BaseModel):
    name: str
    food: str

@app.get("/hello")
async def say_hello():
    return {"message": "Hello! I am your FastAPI waiter! 🍕"}

@app.get("/greet/{name}")
async def greet_person(name: str):
    return {"message": f"Hello {name}! Welcome to my API! 🎉"}

@app.post("/order")
async def place_order(order: Order, api_key: str = Header(None, alias="api-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key!! Access Denied!! 🚫")
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (name, food) VALUES (?, ?)",
                   (order.name, order.food))
    conn.commit()
    conn.close()
    return {"message": f"{order.name} ordered {order.food}! Saved permanently!! 🎉"}

@app.get("/orders")
async def see_all_orders(api_key: str = Header(None, alias="api-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key!! Access Denied!! 🚫")
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return {"all_orders": orders}

@app.delete("/order/{id}")
async def delete_order(id: int, api_key: str = Header(None, alias="api-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key!! Access Denied!! 🚫")
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": f"Order {id} deleted successfully!! 🗑️"}

@app.put("/order/{id}")
async def update_order(id: int, order: UpdateOrder, api_key: str = Header(None, alias="api-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key!! Access Denied!! 🚫")
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET name = ?, food = ? WHERE id = ?",
                   (order.name, order.food, id))
    conn.commit()
    conn.close()
    return {"message": f"Order {id} updated successfully!! ✏️"}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents),
        "message": f"File {file.filename} uploaded successfully!! 📁"
    }
