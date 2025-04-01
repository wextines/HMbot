import asyncpg
import asyncio
import re
from config import DB_URL  # Добавьте строку подключения из config.py

pool = None  # Глобальный пул соединений

async def init_db():
    """Создание пула соединений при старте"""
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DB_URL)  # Передаем строку подключения
    print("[INFO] Database pool initialized")

async def close_db():
    """Закрытие пула соединений"""
    global pool
    if pool:
        await pool.close()
        pool = None
        print("[INFO] Database pool closed")

async def get_pool():
    """Возвращает пул соединений с проверкой"""
    global pool
    if pool is None:
        await init_db()
    return pool

async def CREATE_INSERT(input_string):
    """Добавление данных в таблицу"""
    try:
        pool = await get_pool()  # Получаем пул соединений
        async with pool.acquire() as conn:
            async with conn.transaction():  # Открываем транзакцию
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS keys(
                        id SERIAL PRIMARY KEY,
                        key VARCHAR(1) NOT NULL
                    );
                """)

                keys_list = [(char,) for char in input_string if re.match(r'[a-zA-Zа-яА-Я]', char)]
                
                if keys_list:  # Проверяем, есть ли данные для вставки
                    await conn.executemany("INSERT INTO keys (key) VALUES ($1)", keys_list)

    except Exception as e:
        print("[ERROR] CREATE_INSERT:", e)


async def DELETE_TABLE():
    """Удаление таблицы с логами и перезапуском соединения"""
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():  # Открываем транзакцию для гарантии выполнения
                await conn.execute("DROP TABLE IF EXISTS keys;")
                print("[INFO] Table 'keys' deleted successfully!")

    except Exception as e:
        print("[ERROR] DELETE_TABLE:", e)

async def GET_KEYS():
    """Получение всех ключей"""
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT key FROM keys;")
            return [row["key"] for row in rows]
    except Exception as e:
        print("[ERROR] GET_KEYS:", e)
        return []
