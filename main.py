import asyncio
import time

import flet as ft

class ТаблоТаймера(ft.Text):
    def __init__(self):
        super().__init__(value="00:00:00", size=30, weight=ft.FontWeight.BOLD)


class КнопкаУправления(ft.FilledButton):
    def __init__(self, действие_при_клике):
        super().__init__(
            "Start",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=действие_при_клике,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=15
            )
        )


class КнопкаСброса(ft.TextButton):
    def __init__(self, действие_при_клике):
        super().__init__(
            "Stop",
            icon=ft.Icons.STOP_CIRCLE_ROUNDED,
            disabled=True,
            on_click=действие_при_клике,
            style=ft.ButtonStyle(
                shape=ft.StadiumBorder(),
                padding=15
            )
        )


def format_hhmmss(seconds: int) -> str:
    # Функция для форматирования секунд в формат ЧЧ:ММ:СС
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    running = False
    paused = False
    elapsed = 0
    base_elapsed = 0
    started_at = 0.0

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.RED,
            primary_container=ft.Colors.RED_200
        )
    )

    # Функции-обработчики для кнопок
    def handle_toggle(e):
        nonlocal running, paused, elapsed, base_elapsed, started_at

        if not running:
            running = True
            paused = False
            base_elapsed = elapsed
            started_at = time.time()
            page.run_task(ticker)
            sync_ui()
            return

        if not paused:
            base_elapsed += int(time.time() - started_at)
            elapsed = base_elapsed
            paused = True
            sync_ui()
            return

        paused = False
        started_at = time.time()
        sync_ui()

    def handle_stop(e):
        nonlocal running, paused, elapsed, base_elapsed, started_at
        running = False
        paused = False
        elapsed = 0
        base_elapsed = 0
        started_at = 0.0
        sync_ui()

    timer = ТаблоТаймера()
    toggle_btn = КнопкаУправления(действие_при_клике=handle_toggle)
    stop_btn = КнопкаСброса(действие_при_клике=handle_stop)

    def sync_ui():
        nonlocal elapsed
        timer.value = format_hhmmss(elapsed)

        if running and not paused:
            toggle_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
        else:
            toggle_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED

        stop_btn.disabled = (not running) and (elapsed == 0)

    async def ticker():
        nonlocal elapsed
        while running:
            if not paused:
                elapsed = base_elapsed + int(time.time() - started_at)
                timer.value = format_hhmmss(elapsed)
                timer.update()
            await asyncio.sleep(1)

    page.padding = 0

    page.add(
        ft.Container(
            image=ft.DecorationImage(
                src="https://i.pinimg.com/736x/da/44/83/da448376d3145d26a82d51359b8dad1f.jpg",
                fit=ft.BoxFit.COVER,
            ),
            expand=True,
            blur=ft.Blur(15, 15, ft.BlurStyle.NORMAL),

            content=ft.SafeArea(
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        timer,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                toggle_btn,
                                stop_btn,
                            ],
                        ),
                    ],
                )
            )
        )
    )

    sync_ui()


if __name__ == "__main__":
    ft.run(main)