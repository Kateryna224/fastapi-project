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


def read_items() -> list[Item]:
    return items_db


# def update_item(item_id: int, item: dict):
#     if item_id in items_db:
#         items_db[item_id] = item
#         return item
#     return None

# def delete_item(item_id: int):p
#     return items_db.pop(item_id, None)
