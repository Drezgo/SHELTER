import sqlite3

# Створення бази даних та таблиці
conn = sqlite3.connect("DataBases\A1.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE Uses_choice_G_2_3 (
    Material TEXT NOT NULL,
    Thickness INTEGER NOT NULL
);
""")

conn.commit()
conn.close()

print("База даних створена та наповнена!")


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
