import asyncpg
import asyncio
from asyncio import AbstractEventLoop

#Potential Database Functions
async def _connect():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    version = connection.get_server_version()
    print(f'Connected! Postgres version is {version}')
    await connection.close()


class DB:
    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.connect()

    def connect(self):
        asyncio.run_coroutine_threadsafe(_connect(), self.loop)


