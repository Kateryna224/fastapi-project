from app.schemas.item import Item
from typing import Optional

items_db: list[Item] = [Item(name="name", description="description")]

def create_item(item: Item) -> Item:
    items_db.append(item)
    return item

def read_item(item_id: int) -> Optional[Item]:
    try:
        return items_db[item_id]
    except IndexError:
        return None

def read_items(skip: int = 0, limit: int = 10) -> list[Item]:
    return items_db[skip:skip + limit]

def update_item(item_id: int, item: Item) -> Optional[Item]:
    if 0 <= item_id < len(items_db):
        items_db[item_id] = item
        return item
    return None

def delete_item(item_id: int) -> Optional[Item]:
    if 0 <= item_id < len(items_db):
        return items_db.pop(item_id)
    return None