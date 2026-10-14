from db_orm import engine

with engine.connect() as connection:
    result = connection.exec_driver_sql("SELECT 1")
    print(result.scalar())

print("Подключение к PostgreSQL работает!")
