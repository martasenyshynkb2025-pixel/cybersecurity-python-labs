import sqlite3
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from labs.lab03 import repository
from labs.lab03.schemas import RecordCreate, RecordRead, RecordReplace

router = APIRouter(prefix="/records", tags=["Records"])


@router.get("", response_model=List[RecordRead])
def get_records(
    category_id: Optional[int] = Query(None, gt=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    min_value: Optional[float] = Query(None, ge=0.0),
    q: Optional[str] = Query(None, min_length=1, max_length=120),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return repository.get_records(
        category_id=category_id,
        status=status_filter,
        min_value=min_value,
        q=q,
        limit=limit,
        offset=offset,
    )


@router.get("/{record_id}", response_model=RecordRead)
def get_record(record_id: int):
    if record_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ID повинен бути > 0",
        )
    record = repository.get_record_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запис не знайдено"
        )
    return record


@router.post("", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(payload: RecordCreate):
    try:
        return repository.create_record(
            code=payload.code,
            title=payload.title,
            category_id=payload.category_id,
            value=payload.value,
            status=payload.status,
        )
    except sqlite3.IntegrityError as e:
        err_msg = str(e)
        if "FOREIGN KEY" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вказана категорія не існує",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Запис із таким code вже існує"
        )


@router.put("/{record_id}", response_model=RecordRead)
def update_record(record_id: int, payload: RecordReplace):
    if record_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ID повинен бути > 0",
        )
    try:
        updated = repository.update_record(
            record_id=record_id,
            code=payload.code,
            title=payload.title,
            category_id=payload.category_id,
            value=payload.value,
            status=payload.status,
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Запис не знайдено"
            )
        return updated
    except sqlite3.IntegrityError as e:
        err_msg = str(e)
        if "FOREIGN KEY" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вказана категорія не існує",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Конфлікт унікальності code"
        )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int):
    if record_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ID повинен бути > 0",
        )
    deleted = repository.delete_record(record_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запис не знайдено"
        )


@router.post(
    "/bulk", response_model=List[RecordRead], status_code=status.HTTP_201_CREATED
)
def bulk_create(payload: List[RecordCreate]):
    if not payload or len(payload) > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Розмір пакета 1-100 елементів",
        )

    records_data = [item.model_dump() for item in payload]
    try:
        return repository.bulk_create_records(records_data)
    except sqlite3.IntegrityError as e:
        err_msg = str(e)
        if "FOREIGN KEY" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Одна з категорій у пакеті не існує",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Дублікат code у базі або всередині пакета",
        )
