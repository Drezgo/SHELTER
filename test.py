from tkinter.font import BOLD
from turtle import color
import flet as ft


def main(page: ft.Page):
    counter = 0
    
    # if type(dropdown.value) != str and selected_option_1 == "":
    #     page.open(snackBar("клас сховища"))
    # else:
    #     second_page(page)
        
    # page.theme_mode=ft.ThemeMode.LIGHT
    def on_click(e):
        nonlocal counter
        page.open(
            ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
                        ft.Text(f"Counter value at {counter}", weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.START,  # Вирівнювання зліва
                    spacing=10,  
                ),
                bgcolor=ft.Colors.AMBER_100,
                action="OK",
                duration=3000,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )
        counter += 1
        page.update()

    page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))


ft.app(main)

# def main(page):
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

#     def banner(value):
#         banner = ft.Banner(
#         bgcolor=ft.Colors.AMBER_100,
#         leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
#         content=ft.Text(
#             value=f"Помилка! Спочатку виберіть {value}",
#             color=ft.Colors.BLACK,
#         ),
#         actions=[
#             ft.TextButton(text="OK", style=ft.ButtonStyle(color=ft.Colors.BLUE), on_click=lambda e: page.close(banner))
#         ],
#         )
#         return banner

#     page.add(ft.ElevatedButton("Show Banner", on_click=lambda e: page.open(banner("################"))))