# Початкове заповнення БД (якщо потрібно)

import pandas as pd
import sqlite3
import os

# Шлях до папки з JSON-файлами
folder_path = r"F:\UDAV\SHELTER\db\jsonTable"

# Шлях до SQLite бази даних
db_path = r"F:\UDAV\SHELTER\db\MainBase.db"

# Отримуємо список усіх JSON-файлів у папці
files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
print(f"Знайдено {len(files)} JSON-файлів у папці '{folder_path}': {files}")

# Підключення до SQLite
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

try:
    for file in files:
        # Отримуємо шлях до поточного JSON-файлу
        json_path = os.path.join(folder_path, file)

        # Отримуємо назву таблиці (видаляємо розширення .json)
        table_name = os.path.splitext(file)[0]
        print(f"\n⏳ Обробка файлу: {file} -> Таблиця: {table_name}")

        # Читаємо JSON у DataFrame
        try:
            df = pd.read_json(json_path)
            if df.empty:
                print(f"⚠️ Пропущено: {file} (порожній файл)")
                continue  # Пропускаємо порожні файли
            
            # Записуємо DataFrame у SQLite (заміна таблиці, якщо вже існує)
            df.to_sql(table_name, connection, if_exists="replace", index=False)
            print(f"✅ Таблиця '{table_name}' успішно оновлена ({len(df)} рядків).")
        
        except pd.errors.EmptyDataError:
            print(f"❌ Помилка: {file} має неправильний JSON-формат або порожній.")
        except ValueError as e:
            print(f"❌ Помилка обробки JSON у файлі '{file}': {e}")

except sqlite3.Error as e:
    print(f"❌ Помилка SQLite: {e}")

finally:
    # Закриваємо підключення
    connection.close()
    print("\n🔒 Підключення до бази даних закрито.")



# import sqlite3

# # Створення бази даних та таблиці
# conn = sqlite3.connect("DataBases\A1.db")
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE Uses_choice_G_2_3 (
#     Material TEXT NOT NULL,
#     Thickness INTEGER NOT NULL
# );
# """)

# conn.commit()
# conn.close()

# print("База даних створена та наповнена!")


# # Створення таблиці
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS a1 (
#     class TEXT PRIMARY KEY,
#     description TEXT
# )
# """)

# # Додавання даних
# data = [
#     ("A-I", "Опис для класу A-I"),
#     ("A-II", "Опис для класу A-II"),
#     ("A-III", "Опис для класу A-III"),
#     ("A-IV", "Опис для класу A-IV"),
# ]

# cursor.executemany("INSERT OR IGNORE INTO a1 (class, description) VALUES (?, ?)", data)
# conn.commit()
# conn.close()

# print("База даних створена та наповнена!")






# import sqlite3

# selected_option_1 = "A-I"  # Приклад значення для перевірки

# try:
#     conn = sqlite3.connect("DataBases\A1.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT description FROM a1 WHERE class = ?", (selected_option_1,))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         print(f"Description: {result[0]}")
#     else:
#         print("No description found.")
# except sqlite3.Error as e:
#     print(f"Database error: {e}")

# перетворення з JSON в SQLite

# import pandas as pd
# import sqlite3
# import os

# folder_path = r"F:\UDAV\SHELTER\db\jsonTable"
# files = os.listdir(folder_path)
# print(f"Файли в директорії '{folder_path}': {files}")

# try:
#     # Завантажуємо JSON файл у DataFrame
#     table_name = "wall_materials"
#     json_path = r"F:\UDAV\SHELTER\db\jsonTable\wall_materials.json"
#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"Файл JSON не знайдено за шляхом: {json_path}")
#     print(f"Файл JSON знайдено: {json_path}")

#     df = pd.read_json(json_path)
#     print("JSON успішно завантажено у DataFrame.")
#     # print(df.head())  # Виводимо перші кілька рядків для перевірки

#     # Підключаємося до SQLite
#     db_path = ".\db\MainBase.db"
#     print(f"Підключення до SQLite бази даних: {db_path}")
#     connection = sqlite3.connect(db_path)

#     # Зберігаємо DataFrame у таблиці SQLite
    
#     df.to_sql(table_name, connection, if_exists="replace", index=False)
#     print(f"Дані успішно записані в таблицю '{table_name}'.")

#     # Перевіряємо, чи таблиця існує, та виводимо кількість рядків
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
#     row_count = cursor.fetchone()[0]
#     print(f"Таблиця '{table_name}' створена. Кількість рядків: {row_count}")

# except FileNotFoundError as e:
#     print(f"Помилка: {e}")
# except pd.errors.EmptyDataError:
#     print("Помилка: JSON-файл порожній або має неправильний формат.")
# except sqlite3.Error as e:
#     print(f"Помилка SQLite: {e}")
# finally:
#     if 'connection' in locals() and connection:
#         connection.close()
#         print("Підключення до бази даних закрито.")
