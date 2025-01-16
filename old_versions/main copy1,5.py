import flet as ft
import sqlite3

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


    # Функція для переходу на другу сторінку
    def go_to_second_page(e):
        page.controls.clear()

        row = ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number_2,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Друга сторінка
        page.add(
            ft.Container(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            tooltip="Назад",
                            on_click=go_back,  # Функція для повернення
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.Padding(10, 10, 0, 0),  # Відступи для кнопки
                expand=False,
            ),
            ft.Column(
                [
                    ft.Text(f"Ви обрали клас сховища: {selected_option_1}", size=20, weight="bold"),
                    ft.Dropdown(
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
                    ),
                    ft.Text("Вибір товщини шару матеріалу (кратний 5)", size=16, weight="bold"),
                    row,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            )
        )
        page.update()

    def minus_click(e):
        txt_number_2.value = str(int(txt_number_2.value) - 5)
        page.update()

    def plus_click(e):
        txt_number_2.value = str(int(txt_number_2.value) + 5)
        page.update()
    
    # Функція для повернення на першу сторінку
    def go_back(e):
        page.controls.clear()
        page.add(first_page())  # Виклик функції для повернення вмісту першої сторінки
        page.update()

    # Функція для оновлення тексту вибору
    def on_dropdown_change(e):
        nonlocal selected_option_1
        selected_option_1 = e.control.value
        result_text_1.value = f"Ви обрали: {selected_option_1}" if selected_option_1 else "Error"

        # Отримання опису з бази даних
        if selected_option_1:
            connection = sqlite3.connect("DataBases\A1.db")
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
                    "Продовжити",
                    on_click=go_to_second_page,
                    width=150,
                ),
                result_text_1,  # Відображення вибору під кнопкою
                description_text_1,   # Відображення опису класу споруди з бази а1
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # Відображення першої сторінки
    page.add(first_page())  # Викликаємо функцію first_page

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
# assets_dir="assets", view=ft.AppView.WEB_BROWSER