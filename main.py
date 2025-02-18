import flet as ft

from config import THEME
from frontend import welcome_page, delete_table_G1


def main(page: ft.Page):

    # Налаштування сторінки
    page.window.width = 900    #для desktop-вікна
    page.window.height = 600    #для desktop-вікна
    page.title = "Forteck - розрахунок захисту укриттів від радіації" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = THEME
    # page.window.icon = "Radiation.png"

    # видалення табл шарів
    delete_table_G1()

    page.add(welcome_page(page))

ft.app(
    target=main,
    assets_dir="assets",
    view=ft.AppView.WEB_BROWSER,
)