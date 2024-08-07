import duckdb
from sqlalchemy import create_engine

#Здесь создаются основные функции по работе с БД

def execute_sql_file(db_path, sql_file_path,create_df=False):
    """
    Подключается к базе данных DuckDB и выполняет SQL-запросы из файла.
    
    Arrgs:
        db_path (str): Путь к файлу базы данных.
        sql_file_path (str): Путь к файлу SQL, содержащему запросы.
        create_df (bool, optional): Если True, функция вернет DataFrame с результатами запроса. По умолчанию False.
    
     Returns:
        pandas.DataFrame: Если create_df равно True, функция вернет DataFrame с результатами запроса. В противном случае вернет None.
"""
    try:
        # Подключение к базе данных
        conn = duckdb.connect(database=db_path, read_only=False)
        print(f"Успешное подключение к базе данных: {db_path}")
        
        # Чтение SQL-запросов из файла
        with open(sql_file_path, 'r') as file:
            sql_queries = file.read()
        
        if create_df:
            # Выполнение SQL-запросов
            df = conn.execute(sql_queries).fetchdf()
            print("Запрос успешно выполнен. Создан датафейм")
            return df
        else:
            conn.execute(sql_queries)
            print("Запрос успешно выполнен.")

        
        # Закрытие подключения
        conn.close()
    except Exception as e:
        print(f"Ошибка выполнения запросов: {e}")


def insert_df_to_duckdb(df, db_path, table_name):
    """
    Загружает DataFrame в таблицу DuckDB.
    
    Args:
        df (pandas.DataFrame): DataFrame, содержащий данные для загрузки.
        db_path (str): Путь к файлу базы данных DuckDB.
        table_name (str): Имя таблицы (в базе данных), в которую будут загружены данные.
    
    Returns:
        None
    """
    try:
        conn = duckdb.connect(database=db_path, read_only=False)
        print(f"Успешное подключение к базе данных: {db_path}")
        
        conn.register('df_view', df)
        query = f"INSERT INTO {table_name} SELECT * FROM df_view"
        conn.execute(query)
        
        print(f"Данные успешно загружены в таблицу {table_name}.")
        conn.close()
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
    