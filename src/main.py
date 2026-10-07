import asyncio  # Модуль для асинхронного выполнения задач (нужен для секундных пауз)
import time  # Модуль для замера точного системного времени компьютера
import flet as ft  # Импортируем Flet под коротким именем ft

# Импортируем наши переопределенные ООП-классы и функцию из соседних файлов модулей
from src.components import TimerDisplay, ControlButton, ResetButton
from logic import format_hhmmss

# Главная функция приложения, управляющая страницей (page)
def main(page: ft.Page):
    # Центрируем весь будущий контент окна по вертикали и горизонтали
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Переменные состояния таймера (мозг приложения)
    running = False  # Флаг: запущен ли таймер в данный момент
    paused = False  # Флаг: стоит ли запущенный таймер на паузе
    elapsed = 0  # Текущее количество секунд, которое прошло и отображается на экране
    base_elapsed = 0  # Накопленное количество секунд до нажатия на паузу
    started_at = 0.0  # Точная временная метка компьютера, когда таймер был запущен

    # Настраиваем цветовую схему (красная палитра Material 3)
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.RED,  # Основной цвет (FilledButton зальется им)
            primary_container=ft.Colors.RED_200  # Дополнительный контейнерный оттенок
        )
    )

    # Функция-обработчик нажатия на кнопку Старт/Пауза
    def handle_toggle(e):
        nonlocal running, paused, elapsed, base_elapsed, started_at  # Разрешаем менять переменные из main()

        # СЦЕНАРИЙ 1: Таймер полностью стоял. Нажимаем Старт.
        if not running:
            running = True  # Включаем режим работы
            paused = False  # Убираем паузу
            base_elapsed = elapsed  # Базовым временем становится текущее сохраненное
            started_at = time.time()  # Фиксируем на часах компьютера точную секунду старта
            page.run_task(ticker)  # Запускаем фоновую асинхронную функцию тиканья во встроенном потоке Flet
            sync_ui()  # Обновляем внешний вид кнопок
            return  # Выходим из функции

        # СЦЕНАРИЙ 2: Таймер активно работал. Нажимаем Паузу.
        if not paused:
            # Считаем, сколько прошло секунд с последнего старта, и сохраняем в накопленную базу
            base_elapsed += int(time.time() - started_at)
            elapsed = base_elapsed  # Синхронизируем текущие секунды с базой
            paused = True  # Включаем флаг паузы (фоновый ticker перестанет прибавлять время)
            sync_ui()  # Обновляем кнопки
            return  # Выходим из функции

        # СЦЕНАРИЙ 3: Таймер был на паузе. Нажимаем Старт для продолжения.
        paused = False  # Снимаем флаг паузы
        started_at = time.time()  # Ставим новую точку отсчета системного времени
        sync_ui()  # Обновляем интерфейс

    # Функция-обработчик нажатия на кнопку Стоп (полный сброс)
    def handle_stop(e):
        nonlocal running, paused, elapsed, base_elapsed, started_at  # Даем доступ к переменным состояния
        running = False  # Останавливаем цикл в ticker
        paused = False  # Сбрасываем паузу
        elapsed = 0  # Стираем прошедшие секунды
        base_elapsed = 0  # Обнуляем накопленную базу времени
        started_at = 0.0  # Сбрасываем метку времени старта
        sync_ui()  # Принудительно перерисовываем интерфейс в начальное состояние

    # Создаем экземпляры (объекты) наших кастомных ООП-классов
    timer = TimerDisplay()  # Создаем объект текстового табло
    toggle_btn = ControlButton(click_action=handle_toggle)  # Создаем кнопку старта и передаем ей функцию handle_toggle
    stop_btn = ResetButton(click_action=handle_stop)  # Создаем кнопку сброса и передаем ей функцию handle_stop

    # Функция для ручной синхронизации и обновления UI
    def sync_ui():
        nonlocal elapsed  # Используем общую переменную секунд
        timer.value = format_hhmmss(elapsed)  # Форматируем секунды и записываем в текст табло

        # Меняем иконку кнопки Старт/Пауза в зависимости от состояния
        if running and not paused:
            toggle_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED  # Если таймер идет — ставим паузу
        else:
            toggle_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED  # Если остановлен/на паузе — ставим стрелку Play

        # Кнопка Stop отключается (disabled=True), если таймер не работает И время на нуле
        stop_btn.disabled = (not running) and (elapsed == 0)

    # Асинхронная функция-тикалка, которая живет в фоновом режиме
    async def ticker():
        nonlocal elapsed  # Читаем/пишем общую переменную elapsed
        while running:  # Пока флаг running равен True, цикл работает бесконечно
            if not paused:  # Если при этом нет паузы, выполняем математику
                # Точный расчет: берем старую сохраненную базу и добавляем чистую разницу системного времени
                elapsed = base_elapsed + int(time.time() - started_at)
                timer.value = format_hhmmss(elapsed)  # Форматируем полученное число в текст
                timer.update()  # Локально обновляем только текстовый виджет таймера на экране (для высокой скорости)
            await asyncio.sleep(1)  # Засыпаем ровно на 1 секунду, не блокируя прорисовку интерфейса окна

    page.padding = 0  # Убираем внутренние отступы страницы, чтобы фон прилегал прямо к краям десктопного окна

    # Добавляем элементы интерфейса на экран
    page.add(
        ft.Container(  # Базовый контейнер-подложка
            image=ft.DecorationImage(  # Настраиваем фоновое изображение
                src="https://pinimg.com",  # Картинка леса
                fit=ft.BoxFit.COVER,  # Растягиваем изображение на всю ширину и высоту без искажений
            ),
            expand=True,  # Заставляем контейнер растянуться на всё десктопное окно
            blur=ft.Blur(15, 15, ft.BlurStyle.NORMAL),  # Применяем мягкий эффект размытия (Blur) к картинке леса

            content=ft.SafeArea(  # Защитная прослойка SafeArea
                content=ft.Column(  # Строим вертикальный столбец
                    spacing=20,  # Задаем отступ в 20 пикселей между табло и строкой кнопок
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Центрируем элементы внутри столбца по горизонтали
                    alignment=ft.MainAxisAlignment.CENTER,  # Центрируем элементы внутри столбца по вертикали
                    controls=[
                        timer,  # Размещаем на экране наш ООП-виджет табло
                        ft.Row(  # Создаем горизонтальную строку для кнопок
                            alignment=ft.MainAxisAlignment.CENTER,  # Сдвигаем кнопки строго по центру строки
                            controls=[
                                toggle_btn,  # Размещаем ООП-кнопку Старт/Пауза
                                stop_btn,    # Размещаем ООП-кнопку Стоп
                            ],
                        ),
                    ],
                )
            )
        )
    )

    sync_ui()  # При первом запуске принудительно вызываем синхронизацию для правильной блокировки кнопки Stop


# Точка запуска Python скрипта
if __name__ == "__main__":
    ft.run(main)  # Передаем управление новой функции запуска Flet 1.0 (1.x)