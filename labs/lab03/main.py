from contextlib import asynccontextmanager
from fastapi import FastAPI
from shared.student import STUDENT_NAME, GROUP_NAME, VARIANT_NUMBER
from labs.lab03.config import DOMAIN_NAME, VALUE_UNIT, THRESHOLD_VALUE
from labs.lab03.database import initialize_database
from labs.lab03.routers import categories, records


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title=f"Lab 3 API - {DOMAIN_NAME}",
    description=f"Сервіс обліку вимірювань. Одиниця вимірювання: {VALUE_UNIT}, поріг: {THRESHOLD_VALUE}",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(categories.router)
app.include_router(records.router)


@app.get("/ping", tags=["Service"])
def ping():
    return {"status": "ok"}


@app.get("/student", tags=["Service"])
def get_student_info():
    return {
        "student_name": STUDENT_NAME,
        "group_name": GROUP_NAME,
        "variant_number": VARIANT_NUMBER,
    }
