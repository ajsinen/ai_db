import config
import asyncio


async def raw_query(query):
    conn = await config.get_db_connection()
    try:
        result = await conn.fetch(query)
        return [dict(row) for row in result]
    finally:
        await conn.close()

