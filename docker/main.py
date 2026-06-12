from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


fake_db = {}
counter = 1


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


@app.post("/items/")
def create_item(item: Item):
    global counter
    fake_db[counter] = item
    response = {"id": counter, "item": item, "message": "Item created!"}
    counter += 1
    return response
@app.get("/items/")
def get_all_items():
    return fake_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_id] = item
    return {"id": item_id, "item": item, "message": "Item updated!"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return {"message": "Item deleted!"}