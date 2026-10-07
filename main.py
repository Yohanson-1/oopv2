import asyncio
import time
import flet as ft

# Importing our custom components and logic from separate files
from components import TimerDisplay, ControlButton, ResetButton
from logic import format_hhmmss

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

    # Creating instances of our custom English-named components
    timer = TimerDisplay()
    toggle_btn = ControlButton(click_action=handle_toggle)
    stop_btn = ResetButton(click_action=handle_stop)

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
                src="https://pinimg.com",
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
