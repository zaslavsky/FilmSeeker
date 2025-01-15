from tabulate import tabulate
from time import sleep
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import Float, HSplit, VSplit
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.widgets import (
    Box,
    Button,
    Checkbox,
    Dialog,
    Frame,
    Label,
    MenuContainer,
    MenuItem,
    ProgressBar,
    RadioList,
    TextArea,
    CheckboxList,
)
from sakila_models import *
import info_texts


# Подключение нам необходимо с нулевой так что мы не можем себе позволить проверять подключения после инициализации
# т.к поле (Жанры кино) подтягивается сразу из базы
db_connection_info = f"""
    Сервер:         {db_server}
    БД:             {db_name}
    Пользователь:   {db_user}\n
    """

#Пытаемся долбится к базе
try:
    database.connect()
    message_dialog(title="Успешно подключено к БД",text=f"{db_connection_info}").run()
except OperationalError:
    message_dialog(
        title="Ошибка подключения к БД",
        text=f"{info_texts.db_connection_fail_instructions}"
            +f"\nТекущие параметры соединеня:\n{db_connection_info}"
        ).run()

# Тянем Жанры кино из базы
Categoryes = [Checkbox(text=row.name) for row in Category.select()]

# Тянем года выхода фильмов из базы 
# (Мы не будем предлагать несуществующие года к автозаполнению поля)
year_completer = WordCompleter(
    [str(film.release_year) for film in Film.select(Film.release_year).distinct()]
)

# Создаём виджеты
result_output_area = TextArea(read_only=False, scrollbar=True, text = info_texts.logo)
name_input_area = TextArea(focus_on_click=True, multiline=False)
year_input_area = TextArea(focus_on_click=True, completer=year_completer, multiline=False)
category_input_area = HSplit(Categoryes)
test_button = Button(text="Запилить", handler=lambda: debug_output())
search_button = Button(text="Нйти", handler=lambda: serach())
raw_output_checkbox = Checkbox(text="Упрощённый вывод")



def confirm_exit(should_exit):
    root_container.floats.pop()
    if should_exit:
        get_app().exit(result=True)


def do_exit(something=None):
    get_app().exit(result=False)


def do_exit_with_confirm(something=None):
    dialog = Dialog(
        title="Подтверждение выхода",
        body=Label(text="Уже наигрались?"),
        buttons=[
            Button(text="Да", handler=lambda: confirm_exit(True)),
            Button(text="Нет", handler=lambda: confirm_exit(False)),
        ],
    )
    root_container.floats.append(Float(content=dialog))


def debug_output():
    # result_output_area.text = str(get_app().layout.container.content.get_children()[-1])
    result_output_area.text = info_texts.logo


def show_warn(head, body):
    dialog = Dialog(
        title=head,
        body=Label(body),
        buttons=[Button(text="OK", handler=lambda: root_container.floats.pop())],
    )
    root_container.floats.append(Float(content=dialog))


def build_cool_output(query):
    data = [
        {
            "Название": film["title"],
            "Описание": film["description"],
            "Год выхода": film["release_year"],
            "Жанр": film["category"],
        }
        for film in query
    ]
    return tabulate(data, headers="keys", tablefmt="grid")

# Основная функция обработки запроса
def serach():
    # Базовый запрос. Будем прикручивать к нему фильтры по ходу
    query = (
        Film.select(
            Film.film_id, 
            Film.title, 
            Category.name.alias("category"), 
            Film.release_year,
            Film.description
        )
        .join(FilmCategory, on=(Film.film_id == FilmCategory.film_id))
        .join(Category, on=(FilmCategory.category_id == Category.category_id))
    )
    # Название писали?
    if name_input_area.text != "":
        name = name_input_area.text
        query = query.where(Film.title.contains(name))
    # А Год писали?
    if year_input_area.text != "":
        query = query.where(Film.release_year == year_input_area.text)
    # Посмотрим что мы там начекбоксили
    Categoryes_list = [e.values[0][1] for e in Categoryes if e.checked]
    # Если что-то начекбоксили то применим доп. фильтр
    if len(Categoryes_list) != 0:
        query = query.where(Category.name.in_(Categoryes_list))

    # ВЫХЛОП если что-то нашли
    if len(query) != 0:
        # Если чекбокс "Упрощённый вывод" включён
        if raw_output_checkbox.checked:
            result = "\n".join([str(i) for i in query.dicts()])
        # Если хотим красивый вывод
        # Но помним, что печать символов в консоль дорогая операция
        else:
            result = build_cool_output(query.dicts())
    # ВЫХЛОП если хрен там плавал
    else:
        show_warn(
            "По вашему запросу ничего не найдено",
            f"Ключевые слова: '{name_input_area.text}'\n"
            + f"Год: '{year_input_area.text}'\n"
            + f"Жанры: {str(Categoryes_list)}\n",
        )
        result = info_texts.logo
    # Выхлопываем
    result_output_area.text = result

def show_help():
    dialog = Dialog(
        title="help",
        body=Label(info_texts.help),
        buttons=[Button(text="OK", handler=lambda: root_container.floats.pop())],
    )
    root_container.floats.append(Float(content=dialog))


def show_about():
    dialog = Dialog(
        title="Обаут xD",
        body=Label(info_texts.about),
        buttons=[Button(text="OK", handler=lambda: root_container.floats.pop())],
    )
    root_container.floats.append(Float(content=dialog))


def change_layout(container_placeholder):
    app = get_app()
    app.layout.container.content.get_children()[-1] = container_placeholder
    app.invalidate()


def close_dialog():
    root_container.floats.pop()


main_container = HSplit(
    [
        VSplit(
            [
                HSplit(
                    [
                        Frame(title="Поиск по названию", body=name_input_area),
                        Frame(title="Год выхода", body=year_input_area),
                        raw_output_checkbox,
                    ],
                ),
                Frame(title="Жанры кино", body=category_input_area),
            ]
        ),
        search_button,
        Button(text="Хочу пони!", handler=lambda: debug_output()),
        Frame(body=result_output_area, title="Результаты поиска"),
    ]
)

main_container_2 = HSplit(
    [
        VSplit(
            [
                HSplit(
                    [
                        Frame(title="Слова", body=name_input_area, height=5),
                        Frame(title="Год выхода", body=year_input_area, height=5),
                        Frame(title="Жанры кино", body=category_input_area),
                        raw_output_checkbox,
                        search_button,
                    ],
                    width=20,
                ),
                Frame(body=result_output_area, title="Результаты поиска"),
            ]
        )
    ]
)

main_container_3 = HSplit(
    [
        VSplit(
            [   
                Frame(body=result_output_area, title="Результаты поиска"),
                HSplit(
                    [
                        Frame(title="Слова", body=name_input_area, height=5),
                        Frame(title="Год выхода", body=year_input_area, height=5),
                        Frame(title="Жанры кино", body=category_input_area),
                        raw_output_checkbox,
                        search_button,
                    ],
                    width=20,
                ),
            ]
        )
    ]
)

root_container = MenuContainer(
    body=main_container_2,
    menu_items=[
        MenuItem(
            "Menu",
            children=[
                MenuItem("Help", handler=show_help),
                MenuItem("About", handler=show_about),
                MenuItem("Exit", handler=do_exit_with_confirm),
            ],
        ),
        MenuItem(
            "Layouts",
            children=[
                MenuItem("Layout ugly", handler=lambda: change_layout(main_container)),
                MenuItem("Layout left sided", handler=lambda: change_layout(main_container_2)),
                MenuItem("Layout right sided", handler=lambda: change_layout(main_container_3)),
            ],
        ),
    ],
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=19, scroll_offset=2),
        ),
    ],
)

# Global key bindings.
bindings = KeyBindings()
bindings.add("s-tab")(focus_previous)
bindings.add("tab")(focus_next)
bindings.add("c-q")(do_exit)
bindings.add("c-c")(do_exit)

# style = Style.from_dict(
#     {
#         "window.border": "#ff8888",
#         "shadow": "bg:#222222",
#         "menu-bar": "bg:#aaaaaa #888888",
#         "menu-bar.selected-item": "bg:#ffffff #000000",
#         "menu": "bg:#888888 #ffffff",
#         "menu.border": "#aaaaaa",
#         "window.border shadow": "#444444",
#         "focused  button": "bg:#880000 #ffffff noinherit",
#         # Styling for Dialog widgets.
#         "button-bar": "bg:#aaaaff fg:#ffffff",
#         "checkbox": "bg:#444444 fg:#ffffff",      # Стиль для текста чекбокса
#         "checkbox.checked": "bg:#228B22 fg:#00ff00",  # Стиль для отмеченного чекбокса
#         "checkbox.unchecked": "bg:#8B0000 fg:#ff0000",  # Стиль для неотмеченного чекбокса
#     }
# )

style = Style.from_dict({
    # Основной фон и текст
    "": "bg:#000000 fg:#ffffff",  # Общий стиль
    "frame": "bg:#444444 fg:#ffffff",  # Стиль рамок
    "frame.label": "bg:#FFFFFF fg:#000000 bold",  # Заголовок рамок
    "dialog.body": "bg:#333333 fg:#ffffff",  # Тело диалога
    "button": "bg:#555555 fg:#ffffff",  # Кнопки
    "button.focused": "bg:#228b22 fg:#ffffff bold",  # Активная кнопка
    "checkbox": "bg:#444444 fg:#ffffff",  # Чекбоксы
    "checkbox.checked": "bg:#228b22 fg:#ffffff",  # Отмеченные чекбоксы
    "checkbox.unchecked": "bg:#8b0000 fg:#ffffff",  # Неотмеченные чекбоксы
    "input": "bg:#222222 fg:#ffffff",  # Поля ввода
    "text-area": "bg:#222222 fg:#ffffff",  # Текстовые области
    "menu-bar": "bg:#444444 fg:#ffffff",  # Меню
    "menu-bar.selected-item": "bg:#228b22 fg:#ffffff bold",  # Выбранный элемент меню
    "menu": "bg:#333333 fg:#ffffff",  # Выпадающее меню
    "menu.border": "bg:#228b22",  # Граница меню
    "scrollbar.background": "bg:#555555",  # Ползунок прокрутки
    "scrollbar.button": "bg:#888888",  # Кнопка ползунка
    "status-bar": "bg:#333333 fg:#ffffff",  # Статусная строка
    "status-bar.title": "bold",  # Заголовок в статусной строке
})

application = Application(
    layout=Layout(root_container, focused_element=main_container),
    key_bindings=bindings,
    style=style,
    mouse_support=True,
    full_screen=True,
)

if __name__ == "__main__":
    application.run()
