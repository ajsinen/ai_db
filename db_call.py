import config


async def call_db(sql_query):
    return await config.databases.fetch_all(sql_query)

