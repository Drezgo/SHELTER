import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = ft.Image(
        src=f"Screenshot.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    images = ft.Row(expand=1, wrap=False, scroll="always")

    page.add(img, images)

    images.controls.append(
        ft.Image(
            src=f"Screenshot.png",
            width=200,
            height=200,
            fit=ft.ImageFit.NONE,
            border_radius=ft.border_radius.all(10),
        )
    )
    page.update()

ft.app(
    target=main,
    assets_dir="assets",
    view=ft.AppView.WEB_BROWSER,
)