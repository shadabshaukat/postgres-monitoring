from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncpg
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATABASES = json.loads(os.getenv("DATABASES", "{}"))
db_pools = {}

async def create_pools():
    for db_name, conn_str in DATABASES.items():
        db_pools[db_name] = await asyncpg.create_pool(conn_str)

@app.on_event("startup")
async def startup():
    logger.debug("Starting up...")
    try:
        await create_pools()
        logger.debug("Database pools created successfully.")
    except Exception as e:
        logger.error(f"Error creating database pools: {e}")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "databases": list(DATABASES.keys())})

@app.get("/databases")
async def list_databases():
    return list(DATABASES.keys())

@app.get("/query/top_queries")
async def top_queries(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        try:
            return await conn.fetch(
                """SELECT query, calls, total_exec_time
                FROM pg_stat_statements
                WHERE query != '<insufficient privilege>'
                ORDER BY total_exec_time DESC
                LIMIT 10"""
            )
        except asyncpg.exceptions.UndefinedTableError:
            return {"error": "pg_stat_statements extension is not installed or enabled."}

@app.get("/query/index_usage")
async def index_usage(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT schemaname, relname, indexrelname, idx_scan FROM pg_stat_user_indexes")


@app.get("/query/locks")
async def locks(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch(
            """SELECT l.locktype, l.relation::regclass, l.mode, l.granted, l.pid, a.query
            FROM pg_locks l
            JOIN pg_stat_activity a ON l.pid = a.pid"""
        )

@app.get("/query/cache_hit")
async def cache_hit(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT datname, (blks_hit::float/(blks_hit+blks_read+1))*100 as ratio FROM pg_stat_database")

@app.get("/query/replication")
async def replication(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT client_addr, state, write_lag FROM pg_stat_replication")

@app.get("/query/connections")
async def connections(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT state, count(*) FROM pg_stat_activity GROUP BY state")

@app.get("/query/dead_tuples")
async def dead_tuples(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT schemaname, relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables")

@app.get("/query/wal")
async def wal(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT wal_bytes, stats_reset FROM pg_stat_wal")

@app.get("/query/bgwriter")
async def bgwriter(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT checkpoints_timed, buffers_checkpoint FROM pg_stat_bgwriter")

@app.get("/query/table_sizes")
async def table_sizes(db_name: str):
    async with db_pools[db_name].acquire() as conn:
        return await conn.fetch("SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
