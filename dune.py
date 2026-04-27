import os
import json
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from dune_client.client import DuneClient

load_dotenv()

# --- Config ---
DUNE_QUERY_ID = 5779439
CACHE_TTL = 60 * 60 * 24 * 3
CACHE_KEY = f"dune:query:{DUNE_QUERY_ID}"

# --- Dune Client ---
dune_api_key = os.getenv("DUNE_QUERY_API_KEY")
if not dune_api_key:
    raise RuntimeError("DUNE_QUERY_API_KEY environment variable is not set")

dune = DuneClient(dune_api_key)

# --- Smart Cache: Redis if available, in-memory fallback ---
_memory_cache = {}

try:
    import redis
    _redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
    _redis_client.ping()  # fail fast if Redis isn't actually reachable
    USE_REDIS = True
    print("Cache: Redis connected")
except Exception:
    _redis_client = None
    USE_REDIS = False
    print("Cache: Redis unavailable, falling back to in-memory")


def cache_get(key: str):
    if USE_REDIS:
        val = _redis_client.get(key)
        return json.loads(val) if val else None
    entry = _memory_cache.get(key)
    if entry and (time.time() - entry["ts"]) < CACHE_TTL:
        return entry["data"]
    return None


def cache_set(key: str, value):
    if USE_REDIS:
        _redis_client.setex(key, CACHE_TTL, json.dumps(value))
    else:
        _memory_cache[key] = {"data": value, "ts": time.time()}


def cache_delete(key: str):
    if USE_REDIS:
        _redis_client.delete(key)
    else:
        _memory_cache.pop(key, None)


# --- App ---
app = FastAPI(title="Dune Data API")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Dune Data API!",
        "swagger_ui": "/docs",
        "endpoints": ["/data", "/cache", "/health"],
        "cache_ttl_seconds": CACHE_TTL,
        "dune_query_id": DUNE_QUERY_ID,
        "cache_backend": "redis" if USE_REDIS else "in-memory",
    }


def fetch_from_dune() -> list[dict]:
    result = dune.get_latest_result(DUNE_QUERY_ID)
    return result.result.rows


def get_data() -> list[dict]:
    cached = cache_get(CACHE_KEY)
    if cached is not None:
        return cached
    rows = fetch_from_dune()
    cache_set(CACHE_KEY, rows)
    return rows


@app.get("/data")
def get_query_data():
    try:
        data = get_data()
        return {
            "source": "cache_or_dune",
            "cache_backend": "redis" if USE_REDIS else "in-memory",
            "row_count": len(data),
            "rows": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/cache")
def bust_cache():
    cache_delete(CACHE_KEY)
    return {"deleted": True, "key": CACHE_KEY}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "cache_backend": "redis" if USE_REDIS else "in-memory"
    }