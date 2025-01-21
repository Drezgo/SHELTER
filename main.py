import flet as ft
import sqlite3

RESULTS = {}

def main(page: ft.Page):
    selected_option_1 = ""  # Змінна для зберігання вибраного варіанту
    result_text_1 = ft.Text("", size=16, weight="bold", color=ft.colors.GREEN)  # Динамічний текст для відображення вибору (ви обрали А-ІІ)
    description_text_1 = ft.Text("", size=14, italic=True, color=ft.colors.GREEN, width=500)   # Текст для опису з бази даних (пояснення шо таке А-ІІ) 
    txt_number_2 = ft.TextField(value="10", text_align=ft.TextAlign.RIGHT, width=100) # Поле для введення числа

    # print(type(selected_option_1))
    # print(type(description_text))

    # Налаштування сторінки
    page.window.width = 900
    page.window.height = 600
    page.title = "Розрахунок захисту укриттів від радіації"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.window.icon = "Radiation.png"

    def third_page(e): # Третя сторінка зроблена по зразку першої
        page.controls.clear()

        dropdown_left_1 = ft.Dropdown(
            label="Характер забудови",  
            options=[
                ft.dropdown.Option("Промислова"),
                ft.dropdown.Option("Житлова та громадська"),
                ],
                width=300
            )
        dropdown_left_2 = ft.Dropdown(
            label="Матеріал стін огороджувальної конструкції", 
            options=[
                ft.dropdown.Option("Цегляна кладка "),
                ft.dropdown.Option("Легкий бетон"),
                ],
                width=300
            )
        
        page.update()
        page.add(
            ft.Container(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            tooltip="Назад",
                            on_click=go_back_to_2,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.Padding(10, 10, 0, 0),
                expand=False,
            ),
            ft.Column(
                [
                    ft.Text("Визначення коефіцієнту умов розташування", size=30, weight="bold"),
                    # KВизначення зниження дози проникаючої радіації у забудові
                    dropdown_left_1,
                    ft.Divider(),
                    # Визначення послаблення радіації огороджувальними конструкціями будівель
                    dropdown_left_2,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Продовжити"),
                                        ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT),  # Іконка після тексту
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                ),
                                #on_click=go_to_third_page,  # Функція переходу 
                                width=180,  # Ширина кнопки
                            )
                            
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            )
        )


    # Функція для переходу на другу сторінку
    def second_page(e):
        page.controls.clear()

        material_dropdown = ft.Dropdown(
            label="Вибір матеріалу",
            options=[
                ft.dropdown.Option("Бетон"),
                ft.dropdown.Option("Цегла"),
                ft.dropdown.Option("Грунт"),
                ft.dropdown.Option("Дерево"),
                ft.dropdown.Option("Поліетилен"),
                ft.dropdown.Option("Сталь"),
            ],
            width=300,
        )

        row = ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number_2,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Матеріал")),
                ft.DataColumn(ft.Text("Товщина")),
                ft.DataColumn(ft.Text("Дії")),
            ],
            rows=[],
        )

        def load_data():
            # Завантажуємо дані з бази
            connection = sqlite3.connect("db\MainBase.db")
            cursor = connection.cursor()
            cursor.execute("SELECT rowid, Material, Thickness FROM Uses_choice_G1")
            data = cursor.fetchall()
            connection.close()

            table.rows.clear()
            for row in data:
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        # ft.IconButton(ft.icons.EDIT, on_click=lambda e, row_id=row[0]: edit_row(row_id)),
                                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, row_id=row[0]: delete_row(row_id)),
                                    ]
                                )
                            ),
                        ]
                    )
                )
            page.update()

        def add_to_db(e):
            # Додаємо дані до бази
            connection = sqlite3.connect("db\MainBase.db")
            cursor = connection.cursor()
            material = material_dropdown.value
            thickness = txt_number_2.value
            cursor.execute("INSERT INTO Uses_choice_G1 (Material, Thickness) VALUES (?, ?)", (material, thickness))
            connection.commit()
            connection.close()
            load_data()

        def delete_row(row_id):
            # Видаляємо запис
            connection = sqlite3.connect("db\MainBase.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Uses_choice_G1 WHERE rowid = ?", (row_id,))
            connection.commit()
            connection.close()
            load_data()

        def edit_row(row_id):
            # Логіка редагування (заповнення полів значеннями)
            pass

        def go_to_third_page(e):
            # Переходимо на третю сторінку
            page.controls.clear()
            third_page(e)
            page.update()

        page.add(
            ft.Container(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            tooltip="Назад",
                            on_click=go_back_to_1,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.Padding(10, 10, 0, 0),
                expand=False,
            ),
            ft.Column(
                [
                    ft.Text(f"Ви обрали клас сховища: {selected_option_1}", size=20, weight="bold"),
                    material_dropdown,
                    ft.Text("Вибір товщини шару матеріалу (кратний 5)", size=16, weight="bold"),
                    row,
                    ft.Row(
                        [
                            ft.ElevatedButton("Додати", on_click=add_to_db, width=150),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Продовжити"),
                                        ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT),  # Іконка після тексту
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                ),
                                on_click=go_to_third_page,  # Функція переходу на третю сторінку
                                width=180,  # Ширина кнопки
                            )

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(),
                    ft.Text("Таблиця введених даних:", size=18, weight="bold"),
                    table,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
            ),
        )
        load_data()

    def minus_click(e):
        txt_number_2.value = str(int(txt_number_2.value) - 5)
        page.update()

    def plus_click(e):
        txt_number_2.value = str(int(txt_number_2.value) + 5)
        page.update()
    
    # Функція для повернення на першу сторінку
    def go_back_to_1(e):
        page.controls.clear()
        page.add(first_page())  # Виклик функції для повернення вмісту першої сторінки
        page.update()

    # Функція для повернення на другу сторінку
    def go_back_to_2(e):
        page.controls.clear()
        page.add(second_page(e))  # Виклик функції для повернення вмісту першої сторінки
        page.update()

    # Функція для оновлення тексту вибору
    def on_dropdown_change(e):
        nonlocal selected_option_1
        selected_option_1 = e.control.value
        result_text_1.value = f"Ви обрали: {selected_option_1}" if selected_option_1 else "Error"
        RESULTS["option1"] = e.control.value

        # Отримання опису з бази даних
        if selected_option_1:
            connection = sqlite3.connect("db\MainBase.db")
            cursor = connection.cursor()
            cursor.execute("SELECT description FROM a1 WHERE class = ?", (selected_option_1,))
            result = cursor.fetchone()
            connection.close()

            # Оновлення тексту опису
            if result:
                description_text_1.value = result[0]
            else:
                description_text_1.value = "Опис для цього класу відсутній."
        else:
            description_text_1.value = ""

        page.update()

    # Видалення таблиці вибору шарів стін (Табл Г1)
    def delete_table_G1():
        try:
            connection = sqlite3.connect("db\MainBase.db")
            cursor = connection.cursor()

            # Видалити всі рядки з таблиці Uses_choice_G1
            cursor.execute("DELETE FROM Uses_choice_G1")

            connection.commit()
            print("Всі дані з таблиці Uses_choice_G1 успішно видалено.")

        except sqlite3.Error as error:
            print(f"Помилка при очищенні таблиці Uses_choice_G1: {error}")
        finally:
            if connection:
                connection.close()

    # Перша сторінка
    def first_page():
        dropdown = ft.Dropdown(
            label="Клас сховища",
            options=[
                ft.dropdown.Option("A-I"),
                ft.dropdown.Option("A-II"),
                ft.dropdown.Option("A-III"),
                ft.dropdown.Option("A-IV"),
            ],
            width=250,
            on_change=on_dropdown_change,
        )
        return ft.Column(
            [
                ft.Text("Виберіть клас сховища залежно від класу споруди", size=20, weight="bold"),
                dropdown,
                ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Продовжити"),
                                        ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT),  # Іконка після тексту
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                ),
                                on_click=second_page,  # Функція переходу на другу сторінку
                                width=180,  # Ширина кнопки
                            ),
                result_text_1,  # Відображення вибору під кнопкою
                description_text_1,   # Відображення опису класу споруди з бази а1
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # видалення табл шарів
    delete_table_G1()
    # Відображення першої сторінки
    page.add(first_page())  # Викликаємо функцію first_page

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
# assets_dir="assets", view=ft.AppView.WEB_BROWSER