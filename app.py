from fastapi import FastAPI, HTTPException
import redis, psycopg2

app = FastAPI()

# Redis init

try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.ping()
except:
    r = None

# Postgres init
try:
    conn = psycopg2.connect(
        dbname="demo", user="demo", password="password", host="db"
    )
except:
    conn = None


@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}


@app.get("/cache/{key}")
def cache_get(key: str):
    if not r: raise HTTPException(500, "Redis unavailable")
    val = r.get(key)
    if val is None: raise HTTPException(404, "Key not found")
    return {"key": key, "value": val}


@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r: raise HTTPException(500, "Redis unavailable")
    r.set(key, value)
    return {"status": "ok"}


@app.get("/dbtest")
def db_test():
    if not conn: raise HTTPException(500, "Postgres unavailable")
    cur = conn.cursor(); cur.execute("SELECT 1;")
    return {"status": "Postgres OK"}

