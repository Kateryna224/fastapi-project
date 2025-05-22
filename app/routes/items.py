from fastapi import APIRouter, HTTPException, Path, Query, Body
from app.schemas.item import Item
from app.crud import items

router = APIRouter()

@router.post("/items/")
def create_item(
    item: Item = Body(..., title="Item Body")
) -> Item:
    return items.create_item(item)

@router.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., title="Item id", ge=0)
) -> Item:
    item = items.read_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/items/")
def get_items(
    skip: int = Query(0, ge=0, title="Skip number of items"),
    limit: int = Query(10, ge=1, title="Limit number of items")
) -> list[Item]:
    return items.read_items(skip=skip, limit=limit)

@router.put("/items/{item_id}")
def update_item(
    item_id: int = Path(..., title="Item id", ge=0),
    item: Item = Body(..., title="Updated Item Body")
) -> Item:
    updated = items.update_item(item_id, item)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/items/{item_id}")
def delete_item(
    item_id: int = Path(..., title="Item id", ge=0)
) -> dict:
    deleted = items.delete_item(item_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}
