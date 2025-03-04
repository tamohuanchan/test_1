import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:pass@192.168.0.139:5434/task_1")
time.sleep(5)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL,
            salary INTEGER NOT NULL
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM employees;")
    cursor.executemany(
            "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s);",
            [
                ("Иван", "Разработчик", 55000),
                ("Анна", "Аналитик", 48000),
                ("Сергей", "Менеджер", 60000),
                ("Мария", "Дизайнер", 53000),
                ("Дмитрий", "Тестировщик", 49000),
            ],
    )

    print("Сотрудники с зарплатой больше 50 000:")
    cursor.execute("SELECT * FROM employees WHERE salary > 50000;")
    for i in cursor.fetchall():
        print(i)

    cursor.execute("UPDATE employees SET salary = 60000 WHERE name = 'Иван';")
    print("Зарплата обновлена.")

    cursor.execute("DELETE FROM employees WHERE name = 'Анна';")
    print("Сотрудник удален из базы данных.")

    conn.commit()
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Ошибка при работе с БД:", e)
