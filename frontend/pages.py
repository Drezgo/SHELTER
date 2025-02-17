# Всі сторінки Flet UI

import glob
from tkinter.font import BOLD
import flet as ft
import sqlite3

from config import DB_PATH, LOGO_URL, THEME, DBN_URL, STEPS_SELECT_RESULTS
from db import store_coeficients_attenuation_coefficients, load_materials, load_shelter_classes, load_building_types, load_building_height_by_type, load_building_density_by_type, load_wall_materials, load_wall_thickness_by_material, get_coefficient_zab, get_coefficient_bud, get_shelter_class
from logic import formyla, formula_elements, substituted_values, Az, Azf, Ky, Kn, Kzab, Kbud, KN


selected_option_1 = ""  # Змінна для зберігання вибраного варіанту
# material_dropdown = ""  # Змінна для зберігання вибраного варіанту
result_text_1 = ft.Text(
    "", size=16, weight="bold", color=ft.Colors.GREEN
)  # Динамічний текст для відображення вибору (ви обрали А-ІІ)
description_text_1 = ft.Text(
    "", size=14, italic=True, color=ft.Colors.GREEN, width=500
)  # Текст для опису з бази даних (пояснення шо таке А-ІІ)


def fifth_page(page):
    page.controls.clear()
    print("Результат станом на 5 сторінку, перед обрахунками: ", STEPS_SELECT_RESULTS)
    formyla()
    # Таблиця
    table = ft.DataTable(
        border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
        border_radius=20,
        columns=[ft.DataColumn(ft.Text(element, weight="bold")) for element in formula_elements],  # Елементи формули як заголовки колонок
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(value, size=12, text_align=ft.TextAlign.CENTER, weight="bold")) for value in substituted_values],  # Підставлені значення
            )
        ],
        column_spacing=10,  # Зменшення відстані між колонками
        visible=False,  #  таблиця прихована за замовчуванням
        expand=True,
    )

    result_text = ft.Text(
        spans=[
            ft.TextSpan("Результат: \n", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            ft.TextSpan(f"Очікуваний ступінь захисту (Aз) = {Az}\nРозрахований ступінь захисту (Aзф) = {round(Azf, 2)}\n"),
            # ft.TextSpan("Аз ≤ Азф: "),
            ft.TextSpan(
                "\nCтупеню послаблення радіаційного впливу досягнуто." if Az <= Azf else "Cтупеню послаблення радіаційного впливу не досягнуто.",
                style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400 if Az <= Azf else ft.Colors.RED_400),  # Зелений для True, червоний для False
            ),
        ],
        size=16,
    )

    image_Follout = (
        "https://images.pexels.com/photos/30404800/pexels-photo-30404800.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    if Az <= Azf
    else "https://images.pexels.com/photos/30404801/pexels-photo-30404801.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    )

    def toogle_table(e):
        # print(e.control.value)
        table.visible = e.control.value  # Приховуємо або показуємо таблицю
        page.update()  # Оновлюємо сторінку, щоб відобразити зміни
    
    page.add(
        ft.Row(
            [
                rail(page),
                ft.VerticalDivider(width=1),
                ft.Column(  # column для Column з текстом
                    [
                        ft.Container(  # Container для першого Row
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK,
                                        tooltip="Назад",
                                        on_click=lambda e: go_back_to_4(page),
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START, 
                            ),
                            padding=ft.Padding(10, 10, 0, 0),
                            expand=False,
                        ),
                        result_text, # Результат порівняння
                        ft.Switch(label="   Показати обрахунки", value=False, on_change=toogle_table),
                        table,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=20,
                ),
                ft.Column([ft.Image(src=image_Follout, width=400, height=400),], # Зображення
                # width=400,
                spacing=30,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,  #  для другого Column
                ),
        ],
        expand=True,
    )
)

def fourth_page(page):  # 4 сторінка
    page.controls.clear()

    # Отримуємо збережені значення з сесії
    zabudova = page.session.get("zabudova")  
    material = page.session.get("material")

    # завантажуємо можливі варіанти висоти будинків для промислових
    building_heights = load_building_height_by_type(zabudova)

    # створюємо drop down
    options = []
    for height in building_heights:
        options.append(ft.dropdown.Option(key=height[0]))

    # продублювати. для промислової і житлової. іф попередня змінна = промислова, то виводять бетони одні.елсе...
    dropdown_left_Pr1 = ft.Dropdown(  # промислові
        label="Висота будинків",
        options=options,
        width=300,
        
    )

    # завантажуємо можливі варіанти Щільність забудови для промислових
    building_densities = load_building_density_by_type(zabudova)

    # створюємо drop down
    options = []
    for density in building_densities:
        options.append(ft.dropdown.Option(key=density[0]))

    dropdown_left_Pr2 = ft.Dropdown(
        label="Щільність забудови",
        options=options,
        width=300,
    )

    # завантажуємо можливі варіанти Товщина стін
    wall_thickness = load_wall_thickness_by_material(material)

    # створюємо drop down
    options = []
    for thickness in wall_thickness:
        options.append(ft.dropdown.Option(key=thickness[0]))

    dropdown_right_1kerpich = ft.Dropdown(
        label="Товщина стін",
        options=options,
        width=300,
    )

    dropdown_right_2 = ft.Dropdown(
        label="Площина отворів",
        options=[
            ft.dropdown.Option("10"),
            ft.dropdown.Option("20"),
            ft.dropdown.Option("30"),
            ft.dropdown.Option("40"),
            ft.dropdown.Option("50"),
        ],
        width=300,
    )

    text_block = ft.Text(
        spans=[
            ft.TextSpan(
                "Ви обрали:\n",  # Заголовок
                style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            ),
            ft.TextSpan("Клас сховища:   "),
            ft.TextSpan(
                selected_option_1,  # Виділення змінної жирним
                style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
            ),
            ft.TextSpan("\nХарактер забудови:   "),
            ft.TextSpan(
                zabudova,  # Виділення змінної жирним
                style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
            ),
            ft.TextSpan("\nМатеріал стін:   "),
            ft.TextSpan(
                material,  # Виділення змінної жирним
                style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
            ),
        ],
    )

    def go_to_fifth_page(e):
        # Зберігаємо вибрані значення в сесії
        page.session.set("building_height", dropdown_left_Pr1.value)
        page.session.set("building_density", dropdown_left_Pr2.value)
        page.session.set("wall_thickness", dropdown_right_1kerpich.value)
        page.session.set("area_relation_percent", dropdown_right_2.value)

        coefficient_zab = get_coefficient_zab(
            building_type_name=page.session.get("zabudova"),
            building_height=page.session.get("building_height"),
            building_density=page.session.get("building_density"),
        )
        STEPS_SELECT_RESULTS["coefficient_zab"] = coefficient_zab[0]

        coefficient_bud = get_coefficient_bud(
            wall_material_name=page.session.get("material"),
            building_type_name=page.session.get("zabudova"),
            wall_thickness=page.session.get("wall_thickness"),
            area_relation_percent=page.session.get("area_relation_percent"),
        )
        STEPS_SELECT_RESULTS["coefficient_bud"] = coefficient_bud[0]

        print(STEPS_SELECT_RESULTS)
        # Переходимо на третю сторінку
        page.controls.clear()
        fifth_page(page)
        page.update()

    page.add(
        ft.Row([
            rail(page),
            ft.VerticalDivider(width=1),
            ft.Column([
                ft.Container(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                tooltip="Назад",
                                on_click=lambda e: go_back_to_3(page),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.Padding(10, 10, 0, 0),
                    expand=False,
                ),
                ft.Container(
                    text_block,
                    alignment=ft.alignment.center_left,  # Вирівнювання text_block зліва
                    padding=ft.Padding(50, 0, 0, 0),
                    expand=False,
                ),
                ft.Row(
                    [   
                    ft.Column([
                        ft.Text("Висота будинків забудови (м)", size=30, weight="bold"),
                        dropdown_left_Pr1,
                        ft.Text("Щільність забудови (%)", size=30, weight="bold"),
                        dropdown_left_Pr2,
                    ], 
                    # alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    spacing=30,
                    ),
                    ft.Column([
                        ft.Text("Товщина стін огорожі (см)", size=30, weight="bold"),
                        dropdown_right_1kerpich,
                        ft.Text("Відносна площа отворів огорожі (%)", size=30, weight="bold"),
                        dropdown_right_2,
                    ],
                    expand=True, 
                    # alignment=ft.MainAxisAlignment.CENTER, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,    
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Продовжити", weight=ft.FontWeight.BOLD),
                                        ft.Icon(
                                            ft.Icons.KEYBOARD_ARROW_RIGHT
                                        ),  # Іконка після тексту
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                ),
                                on_click=go_to_fifth_page,  # Функція переходу на другу сторінку
                                width=160,  # Ширина кнопки
                                height=40,
                                bgcolor=ft.Colors.GREEN_200,
                                color=ft.Colors.GREEN_900,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(0, 30, 0, 50),
                ),
            ],  
            # alignment=ft.MainAxisAlignment.CENTER,
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=30,
            ),
        ],
        expand=True,
        )
    )
    # page.update()

def third_page(page):  # Третя сторінка зроблена по зразку першої
    page.controls.clear()

    # завантажуємо Характер забудови
    building_types = load_building_types()

    # створюємо drop down
    options = []
    for building_type in building_types:
        name = building_type[0]
        options.append(ft.dropdown.Option(key=name))

    dropdown_left_1 = ft.Dropdown(
        label="Характер забудови",
        options=options,
        width=300,
        value=page.session.get(
            "zabudova"
        ),  # Завантаження збереженого 
    )

    # завантажуємо Характер забудови
    wall_materials = load_wall_materials()

    # створюємо drop down
    options = []
    for wall_material in wall_materials:
        name = wall_material[0]
        options.append(ft.dropdown.Option(key=name))

    dropdown_left_2 = ft.Dropdown(
        label="Матеріал стін огороджувальної конструкції",
        options=options,
        width=300,
        value=page.session.get(
            "material"
        ),  # Завантаження збереженого значення
    )

    def go_to_fourth_page(e):
        # Зберігаємо вибрані значення в сесії
        page.session.set(
            "zabudova", dropdown_left_1.value
        )  
        page.session.set(
            "material", dropdown_left_2.value
        )

        # Переходимо на третю сторінку
        page.controls.clear()
        fourth_page(page)
        page.update()

    page.add(
        ft.Row([
            rail(page),
            ft.VerticalDivider(width=1),
            ft.Column(
                    [ft.Container(
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Назад",
                                    on_click=lambda e: go_back_to_2(page),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.Padding(10, 10, 0, 0),
                        expand=False,
                    ),
                    ft.Text(
                        "Визначення коефіцієнту умов розташування",
                        size=30,
                        weight="bold",
                    ),
                    # KВизначення зниження дози проникаючої радіації у забудові
                    dropdown_left_1,
                    # ft.Divider(), #полоска
                    # Визначення послаблення радіації огороджувальними конструкціями будівель
                    dropdown_left_2,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Продовжити", weight=ft.FontWeight.BOLD),
                                        ft.Icon(
                                            ft.Icons.KEYBOARD_ARROW_RIGHT
                                        ),  # Іконка після тексту
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                ),
                                on_click=go_to_fourth_page,  # Функція переходу на другу сторінку
                                width=160,  # Ширина кнопки
                                bgcolor=ft.Colors.GREEN_200,
                                color=ft.Colors.GREEN_900,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                expand=True,    
            )
        ],expand=True)
    )
    page.update() 

# Функція для переходу на другу сторінку
def second_page(page):
    page.controls.clear()

    # завантажуємо матеріали з бази даних
    materials = load_materials()

    # створюємо dropdown
    options = []
    for material in materials:
        name = material[0]
        options.append(ft.dropdown.Option(key=name))

    material_dropdown= ft.Dropdown(
        label="Вибір матеріалу",
        options=options,
        width=300,
        on_change=lambda e: material_dropdown_change(e),
    )

    # Функція для оновлення тексту вибору
    def material_dropdown_change(e):
        nonlocal material_dropdown
        material_dropdown = e.control.value
    
    txt_number_2 = ft.TextField(
        value="10", 
        text_align=ft.TextAlign.RIGHT, 
        width=100, 
        # keyboard_type=ft.KeyboardType.NUMBER,  # Включає числову клавіатуру
        # on_change=lambda e: validate_input(e),  # Перевірка на зміну тексту
        on_blur=lambda e: validate_input(e),  # Перевірка при втраті фокусу               мабуть буде    ERROR
    )  # Поле для введення числа

    def minus_click(page):
        value = int(txt_number_2.value)
        if value > 10:  # Мінімальне значення
            txt_number_2.value = str(value - 5)
        page.update()

    def plus_click(page):
        value = int(txt_number_2.value)
        if material_dropdown == "Сталь" and value >= 50 :
            txt_number_2.value = "50"  # обмеження для сталі
        else:
            if value < 150 :  # Максимальне значення
                txt_number_2.value = str(value + 5)
        page.update()

    # Функція для валідації введення товщини шару матеріалу
    def validate_input(e):
        try:
            # Перевіряємо, чи введено число в межах діапазону
            value = int(txt_number_2.value)
            if value < 10 or value == "" or value % 5 != 0:
                txt_number_2.value = "10"  # Встановлюємо мінімальне значення
            elif value > 150 or value == "" or value % 5 != 0:
                txt_number_2.value = "150"  # Встановлюємо максимальне значення
            elif material_dropdown == "Сталь" and value > 50:
                txt_number_2.value = "50"
        except ValueError:
            # Якщо введення не є числом, повертаємо мінімальне значення
            txt_number_2.value = "10"
        page.update()

    row = ft.Row(
        [
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: minus_click(page)),
            txt_number_2,
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: plus_click(page)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Матеріал")),
            ft.DataColumn(ft.Text("Товщина (см)")),
            ft.DataColumn(ft.Text("Дії")),
        ],
        rows=[],
    )

    def load_data():
        # Завантажуємо дані з бази
        connection = sqlite3.connect(DB_PATH)
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
                                    # ft.IconButton(ft.Icons.EDIT, on_click=lambda e, row_id=row[0]: edit_row(row_id)),
                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        on_click=lambda e, row_id=row[
                                            0
                                        ]: delete_row(row_id),
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
        page.update()

    def add_to_db(e):
        # Додаємо дані до бази
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        material = material_dropdown
        thickness = txt_number_2.value
        cursor.execute(
            "INSERT INTO Uses_choice_G1 (Material, Thickness) VALUES (?, ?)",
            (material, thickness),
        )
        connection.commit()
        connection.close()
        load_data()

    def delete_row(row_id):
        # Видаляємо запис
        connection = sqlite3.connect(DB_PATH)
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

        store_coeficients_attenuation_coefficients()

        third_page(page)
        page.update()

    page.add(
        ft.Row([
            rail(page),
            ft.VerticalDivider(width=1),
            ft.Container(
                ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                tooltip="Назад",
                                on_click=lambda e: go_back_to_1(page),
                            )
                        ],
                        # alignment = ft.MainAxisAlignment.START,
                    ),
                padding=ft.Padding(10, 10, 0, 0),
                alignment=ft.alignment.top_left,
            ),
            ft.Row(
                [   
                    ft.Column(
                        [
                            ft.Text(
                                spans=[
                                    ft.TextSpan(
                                        "Ви обрали ",  # Заголовок
                                        style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                                    ),
                                    ft.TextSpan("клас сховища:   "),
                                    ft.TextSpan(
                                        selected_option_1,  # Виділення змінної жирним
                                        style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                                    ),
                                ],
                            ),
                            ft.Text(
                                "1. Виберіть матеріал стіни (стін можна створити декілька)",
                                size=16,
                                weight="bold",
                            ),
                            material_dropdown,
                            ft.Text(
                                "2. Вкажіть товщину шару матеріалу стіни (см)*",
                                size=16,
                                weight="bold",
                            ),
                            row,
                            ft.Text(
                                "* Товщина має бути від 10 до 150 см та кратною 5 см ",
                                size=12,
                                weight="bold",
                                color=ft.Colors.RED,
                            ),
                            ft.Row(
                                [
                                    ft.OutlinedButton("Додати", on_click=add_to_db, width=150, style=ft.ButtonStyle(side=ft.BorderSide(2, ft.Colors.BLUE))),
                                    ft.ElevatedButton(
                                        content=ft.Row(
                                            [
                                                ft.Text("Продовжити", weight=ft.FontWeight.BOLD),
                                                ft.Icon(
                                                    ft.Icons.KEYBOARD_ARROW_RIGHT
                                                ),  # Іконка після тексту
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                                        ),
                                        on_click=go_to_third_page,  # Функція переходу на другу сторінку
                                        width=150,  # Ширина кнопки
                                        bgcolor=ft.Colors.GREEN_200,
                                        color=ft.Colors.GREEN_900,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.VerticalDivider(),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        spacing=20,
                    ),
                    ft.Column(
                        [
                            ft.Text("Таблиця введених даних:", size=18, weight="bold"),
                            table,
                            # ft.OutlinedButton("Очистити таблицю", on_click=delete_table_G1(), width=150, style=ft.ButtonStyle(side=ft.BorderSide(2, ft.Colors.RED))),
                        ],  
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                        expand=True,  # Забезпечує, що контейнер займає всю доступну площу
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
        ],expand=True)
    )
    load_data()

# Функція для повернення на першу сторінку
def go_back_to_home(page):
    page.controls.clear()
    page.add(welcome_page(page))  # Виклик функції для повернення вмісту першої сторінки
    page.update()
    # delete_table_G1()
    STEPS_SELECT_RESULTS = {}#!!!!!!!!!!!!!! !!!!!!!!!!!!!!! !!!!!!! має стерти всі дані, але не стирає всі! доробити
    # анулювання змінних для зберігання даних з STEPS_SELECT_RESULTS та інші змініні:

# Функція для повернення на першу сторінку
def go_back_to_1(page):
    page.controls.clear()
    page.add(first_page(page))  # Виклик функції для повернення вмісту першої сторінки
    page.update()

# Функція для повернення на другу сторінку
def go_back_to_2(page):
    page.controls.clear()
    # page.add(second_page(e))#error
    second_page(page)
    page.update()

# Функція для повернення на третю сторінку
def go_back_to_3(page):
    page.controls.clear()
    # page.add(third_page(e))#error
    third_page(page)  
    page.update()

# Функція для повернення на четверту сторінку
def go_back_to_4(page):
    page.controls.clear()
    fourth_page(page)  
    page.update()

# Видалення таблиці вибору шарів стін (Табл Г1)
def delete_table_G1():
    try:
        connection = sqlite3.connect(DB_PATH)
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
# Функція для перемикання теми
def toggle_theme(page):
    global THEME
    if THEME == ft.ThemeMode.LIGHT:
        THEME = ft.ThemeMode.DARK
    else:
        THEME = ft.ThemeMode.LIGHT
    page.theme_mode = THEME
    page.update()

def navigation_change(page, e):
    selected_index = e.control.selected_index
    if selected_index == 0:
        print("Методика обрана")
        page.launch_url(DBN_URL)
    elif selected_index == 1:
        print("Таблиці обрані")
        page.controls.clear()
        page.add(tables(page))  # Виклик функції для повернення вмісту сторінки
        page.update()
    elif selected_index == 2:
        print("Про Forteck обрано")
        page.controls.clear()
        page.add(welcome_page(page))  # Виклик функції для повернення вмісту першої сторінки
        page.update()

def rail(page):
    return ft.NavigationRail(
        # selected_index=0,   # дефолтно обрана кнопка
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.Icons.HOME, text="Головна", on_click=lambda e: go_back_to_home(page)),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(  #0
                icon=ft.Icons.TEXT_SNIPPET_ROUNDED,
                # selected_icon=ft.Icons.TEXT_SNIPPET_OUTLINED,
                label="Методика"
            ),
            ft.NavigationRailDestination(   #1
                icon=ft.Icon(ft.Icons.LIST_ALT_ROUNDED),
                selected_icon=ft.Icon(ft.Icons.VIEW_LIST_ROUNDED),
                label="Таблиці",
            ),
            ft.NavigationRailDestination(   #2
                icon=ft.Icon(ft.Icons.INFO_OUTLINED),
                selected_icon=ft.Icon(ft.Icons.INFO_ROUNDED),
                label="Про Forteck",
            ),
            # ft.NavigationRailDestination(
            #     icon=#################,
            #     selected_icon=ft.Icon(################3),
            #     label_content=ft.Text("як користуватись?"),
            # ),
            # ft.NavigationRailDestination(
            #     icon=ft.Icons.SETTINGS_OUTLINED,
            #     selected_icon=ft.Icon(ft.Icons.SETTINGS),
            #     label_content=ft.Text("Налаштування"),
            # ),
        ],
        on_change=lambda e: navigation_change(page),
        trailing=ft.IconButton(icon=ft.Icons.BRIGHTNESS_4_SHARP, on_click=lambda e: toggle_theme(page)),
    )



def tables(page):
    # image_path = "https://images.pexels.com/photos/30404714/pexels-photo-30404714.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # if os.path.exists(image_path):
    #     print(f"[INFO] Зображення знайдено: {image_path}")
    #     image = ft.Image(src=f"/{image_path}",)
    # else:
    #     print(f"[ERROR] Зображення не знайдено: {image_path}")  # Виведення помилки в консоль

    # page.route = "/tables"

    table2 = ft.DataTable( #A1
        border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
        border_radius=20,
        columns=[
            ft.DataColumn(
                ft.Container(
                    content=ft.Text(
                        "Клас сховища, СПП із захисними властивостями сховищ",
                        # size=12,
                        no_wrap=False,  # Дозволяє перенос тексту
                    ),
                    width=200,  # Встановлює ширину колонки
                )
            ),
            ft.DataColumn(
                ft.Container(
                    content=ft.Text(
                        "Розміщення сховищ, СПП із захисними властивостями сховищ",
                        # size=12,
                        no_wrap=False,
                    ),
                    width=250,
                )
            ),
            ft.DataColumn(
                ft.Container(
                    content=ft.Text(
                        "Надмірний тиск повітряної ударної хвилі кПа",
                        # size=12,
                        no_wrap=False,
                    ),
                    width=180,
                )
            ),
            ft.DataColumn(
                ft.Container(
                    content=ft.Text(
                        "Ступінь послаблення радіаційного впливу (ступінь захисту) Аз",
                        # size=12,
                        no_wrap=False,
                    ),
                    width=250,
                    
                ), 
            ),
        ],
        column_spacing=20,  # Відстань між колонками
        heading_row_height=70,  # Висота заголовків
        data_row_min_height=58,  # Мінімальна висота рядків
        height=280,
        rows=[],
        expand=True,
    )
    
    table3 = ft.DataTable( #Г1
        border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
        border_radius=20,
        columns=[
            ft.DataColumn(ft.Text("Матеріал шару")),
            ft.DataColumn(ft.Text("Товщина шару (см)")),
            ft.DataColumn(ft.Text("Коефіцієнт послаблення дози гамма-випромінювання Kn")),
            ft.DataColumn(ft.Text("Коефіцієнт послаблення нейтронів проникаючої радіації Ky")),
        ],
        rows=[],
        expand=True,
    )

    table4 = ft.DataTable( #Г2
        border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
        border_radius=20,
        columns=[
            ft.DataColumn(ft.Text("Тип будівлі")),
            ft.DataColumn(ft.Text("Висота будівлі забудови (м)")),
            ft.DataColumn(ft.Text("Щільність забудови (%)")),
            ft.DataColumn(ft.Text("Коефіцієнт зниження дози проникаючої радіації Kзаб")),
        ],
        rows=[],
    )

    table5 = ft.DataTable( #Г3
        border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
        border_radius=20,
        columns=[
            ft.DataColumn(ft.Text("Матеріал стін")),
            ft.DataColumn(ft.Text("Тип забудови")),
            ft.DataColumn(ft.Text("Товщина стін")),
            ft.DataColumn(ft.Text("Вага")),
            ft.DataColumn(ft.Text("Площа отворів по відношенню до площі огороджувальних конструкцій будинків,%")),
            ft.DataColumn(ft.Text("Коефіцієнт Кбуд")),
        ],
        rows=[],
    )

    # table6 = ft.DataTable( #Г4
    #     border=ft.border.all(2, "black" if THEME == ft.ThemeMode.LIGHT else "white"),
    #     border_radius=20,
    #     columns=[
    #         ft.DataColumn(ft.Text("Матеріал стін")),
    #         ft.DataColumn(ft.Text("тип забудови")),
    #         ft.DataColumn(ft.Text("товщина стін")),
    #         ft.DataColumn(ft.Text("вага")),
    #         ft.DataColumn(ft.Text("Площа отворів по відношенню до площі огороджувальних конструкцій будинків,%")),
    #         ft.DataColumn(ft.Text("Коефіцієнт Кбуд")),
    #     ],
    #     rows=[],
    # )

    def load_data_table5():
        # Завантажуємо дані з бази
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT wall_material_name, building_type_name, wall_thickness, weight, area_relation_percent, coefficient FROM building_coefficients")
        data = cursor.fetchall()
        connection.close()

        table5.rows.clear()
        for row in data:
            table5.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(str(row[1]))),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                        ft.DataCell(ft.Text(row[4])),
                        ft.DataCell(ft.Text(row[5])),
                    ]
                )
            )
        page.update()

    def load_data_table4():
        # Завантажуємо дані з бази
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT building_type_name, building_height, building_density, coefficient FROM location_condition_coefficients")
        data = cursor.fetchall()
        connection.close()

        table4.rows.clear()
        for row in data:
            table4.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(str(row[1]))),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                    ]
                )
            )
        page.update()

    def load_data_table3():
        # Завантажуємо дані з бази
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT material_name, material_thickness, neutron_dose_coefficient, gamma_dose_coefficient FROM attenuation_coefficients")
        data = cursor.fetchall()
        connection.close()

        table3.rows.clear()
        for row in data:
            table3.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(str(row[1]))),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                    ]
                )
            )
        page.update()

    def load_data_table2():
        # Завантажуємо дані з бази
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM storage_classes")
        data = cursor.fetchall()
        connection.close()

        table2.rows.clear()
        for row in data:
            table2.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(str(row[1]))),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                    ],
                )
            )
        page.update()
    
    container = ft.Row(
        [
        rail(page),
        ft.VerticalDivider(width=1),
        ft.Column(
            [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Назад",
                        on_click=lambda e: go_back_to_1(page),
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Text(
                "       У даній веб-програмі для автоматизації розрахунку рівня захисту протирадіаційних укриттів та сховищ використані такі таблиці:", 
                size=18, 
                ),  # Текст
            ft.Column(
                [
                    ft.Text("Таблиця введених даних Аз:", size=18, weight="bold"),
                    table2
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
            ),
            ft.Column(
                [
                    ft.Text("Таблиця введених ШАРІВ:", size=18, weight="bold"),
                    table3
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
            ),
            ft.Column(
                [
                    ft.Text("Таблиця введених kzab:", size=18, weight="bold"),
                    table4
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
            ),
            ft.Column(
                [
                    ft.Text("Таблиця введених kбуд:", size=18, weight="bold"),
                    table5
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,  # Додає скролінг, якщо елементів занадто багато
                expand=True,  # Забезпечує, що контейнер займає всю доступну площу
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,  # Додаємо expand=True для Column
        spacing=20,
    )
    ],
    expand=True,

)


    load_data_table2()
    load_data_table3()
    load_data_table4()
    load_data_table5()

    return container

# Перша сторінка
def first_page(page):

    shelter_classes = load_shelter_classes()

    options = []
    for shelter_class in shelter_classes:
        (
            protection_class,
            description,
            overpressure_air_blast_wave,
            radiation_protection_level,
        ) = shelter_class
        options.append(ft.dropdown.Option(key=protection_class))

    dropdown = ft.Dropdown(
        label="Клас сховища",
        options=options,
        width=250,
        on_change=lambda e: on_dropdown_change(page, e),
    )

    # Функція для оновлення тексту вибору
    def on_dropdown_change(page, e):
        global selected_option_1
        selected_option_1 = e.control.value
        result_text_1.value = (
            f"Ви обрали: {selected_option_1}" if selected_option_1 else "Error"
        )

        # Отримання опису з бази даних
        if selected_option_1:
            result = get_shelter_class(selected_option_1)
            (
                protection_class,
                description,
                overpressure_air_blast_wave,
                radiation_protection_level,
            ) = result

            # збережемо значення ступінь захисту
            STEPS_SELECT_RESULTS["Az"] = radiation_protection_level

            # Оновлення тексту опису
            if result:
                description_text_1.value = description
            else:
                description_text_1.value = "Опис для цього класу відсутній."
        else:
            description_text_1.value = ""

        page.update()

    return ft.Row(
        [
            rail(page),
            ft.VerticalDivider(width=1),
            ft.Column([ft.Text(
                        "Виберіть клас сховища залежно від класу споруди",
                        size=20,
                        weight="bold",
                    ),
                    dropdown,
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Text("Продовжити", weight=ft.FontWeight.BOLD),
                                ft.Icon(
                                    ft.Icons.KEYBOARD_ARROW_RIGHT
                                ),  # Іконка після тексту
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                        ),
                        on_click=lambda e: second_page(page),  # Функція переходу на другу сторінку
                        width=160,  # Ширина кнопки
                        bgcolor=ft.Colors.GREEN_200,
                        color=ft.Colors.GREEN_900,
                    ),
                    result_text_1,  # Відображення вибору під кнопкою
                    description_text_1,  # Відображення опису класу споруди з бази а1
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand= True,
            )
        ],
        expand=True,    
    )
        
def welcome_page(page):
    # image_path = "https://images.pexels.com/photos/30404714/pexels-photo-30404714.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # if os.path.exists(image_path):       #тільки для файлів у дерикторіях
    #     print(f"[INFO] Зображення знайдено: {image_path}")
    #     image = ft.Image(src=f"/{image_path}",)
    # else:
    #     print(f"[ERROR] Зображення не знайдено: {image_path}")  # Виведення помилки в консоль

    content = ft.Row(
        [   
            rail(page),
            ft.VerticalDivider(width=1),
            ft.Column(
                [
                ft.Text("Forteck", size=40, weight=ft.FontWeight.BOLD),  # Заголовок
                ft.Container(
                    ft.Container(
                        ft.Text("Дана веб-програма розроблена для автоматизаціїі розрахунку рівня захисту протирадіаційних укриттів та сховищ. Програма базується на положеннях ДБН В.2.2-5:2023 «Захисні споруди цивільного захисту». Розроблений інструмент дозволяє спростити та пришвидшити процес оцінки захисних властивостей споруд, враховуючи різні параметри. Результати можуть бути використані для проєктування нових та оцінки існуючих захисних споруд.", size=18),  # Текст
                        border=ft.border.only(left=ft.border.BorderSide(width=5, color=ft.Colors.BLUE)),  # Додаємо лінію зліва
                        padding=ft.padding.only(left=20),  # Відступ зліва від лінії до кнопки
                    ),
                    padding=ft.Padding(70, 0, 0, 0),  
                ),
                ft.Container(
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Text("Розпочати", weight=ft.FontWeight.BOLD, size=18),   
                                ft.Icon(
                                    ft.Icons.KEYBOARD_ARROW_RIGHT
                                ),  # Іконка після тексту
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Вирівнювання по центру
                        ),
                        on_click=lambda e: go_back_to_1(page),  # Функція переходу на другу сторінку
                        width=180,  # Ширина кнопки
                        height=50,
                        bgcolor=ft.Colors.GREEN_200,
                        color=ft.Colors.GREEN_900,
                    ),
                    padding=ft.Padding(70, 0, 0, 0),
                    alignment=ft.Alignment(-1,-1),
                ),
                ],
                spacing=30,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                expand=True,  # Додаємо expand=True для Column
            ),
            ft.Column([ft.Image(src=LOGO_URL, # Зображення LOGO
                width=400, 
                height=400,
                ),],  
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Додаємо expand=True для другого Column
            ),
        ],
        expand=True,    
    )

    return content