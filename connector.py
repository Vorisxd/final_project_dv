import duckdb

def connect_to_duckdb(db_path=':memory:'):
    """
    Подключается к базе данных DuckDB.
    
    Args:
        db_path (str): Путь к файлу базы данных. Используйте ':memory:' для базы данных в памяти.
    
    Returns:
        duckdb.Connection: Объект подключения к базе данных.
    """
    try:
        conn = duckdb.connect(database=db_path, read_only=False)
        print(f"Успешное подключение к базе данных: {db_path}")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None
    
