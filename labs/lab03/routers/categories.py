import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status
from labs.lab03 import repository
from labs.lab03.schemas import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryRead])
def get_categories():
    return repository.get_all_categories()


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate):
    try:
        return repository.create_category(payload.name)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Категорія з назвою '{payload.name}' вже існує",
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    if category_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Некоректний ID"
        )
    try:
        deleted = repository.delete_category(category_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Категорію не знайдено"
            )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Неможливо видалити категорію, яка містить записи",
        )
