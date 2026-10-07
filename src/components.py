import flet as ft

class TimerDisplay(ft.Text):
    """Custom text widget for the timer display."""
    def __init__(self):
        super().__init__(value="00:00:00", size=30, weight=ft.FontWeight.BOLD)


class ControlButton(ft.FilledButton):
    """Custom rectangular button for Start/Pause actions."""
    def __init__(self, click_action):
        super().__init__(
            "Start",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=click_action,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=15
            )
        )


class ResetButton(ft.TextButton):
    """Custom stadium-shaped button for Stop actions."""
    def __init__(self, click_action):
        super().__init__(
            "Stop",
            icon=ft.Icons.STOP_CIRCLE_ROUNDED,
            disabled=True,
            on_click=click_action,
            style=ft.ButtonStyle(
                shape=ft.StadiumBorder(),
                padding=15
            )
        )
