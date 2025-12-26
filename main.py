# app/main.py
from fastapi import FastAPI
from database import get_db_connection
from routes.connections import router as connections_router

app = FastAPI()

app.include_router(connections_router)

@app.get("/health/db")
def db_health_check():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    cur.close()
    conn.close()
    return {"status": "Database connected successfully"}
