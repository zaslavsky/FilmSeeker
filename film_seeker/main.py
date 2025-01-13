from prompt_toolkit import prompt
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

database.connect()
print("Подключено успешно!")

Categoryes = [Checkbox(text=row.name) for row in Category.select()]

year_completer = WordCompleter(
    [str(film.release_year) for film in Film.select(Film.release_year).distinct()]
)

result_output_area = TextArea(read_only=True, scrollbar=True)
name_input_area = TextArea(focus_on_click=True)
year_input_area = TextArea(focus_on_click=True, completer=year_completer)
category_input_area = HSplit(Categoryes)
test_button = Button(text="Запилить", handler=lambda: debug_output())
search_button = Button(text="Нйти", handler=lambda: serach())


# Функция для обработки ответа на запрос подтверждения выхода
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
    result_output_area.text = str(get_app().layout.container.content.get_children()[-1])


def serach():
    # default query
    query = (
        Film.select(Film.film_id, Film.title, Category.name, Film.release_year)
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

    # ВЫХЛОП
    result = "\n".join([str(i) for i in query.dicts()])
    result_output_area.text = result


# Функция для вызова диалогового окна
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
                    ],
                ),
                Frame(title="Жанры кино", body=category_input_area),
            ]
        ),
        test_button,
        search_button,
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
                        test_button,
                        search_button,
                    ],
                    width=20,
                ),
                Frame(body=result_output_area, title="Результаты поиска"),
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
                MenuItem("Layout 1", handler=lambda: change_layout(main_container)),
                MenuItem("Layout 2", handler=lambda: change_layout(main_container_2))
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

style = Style.from_dict(
    {
        "window.border": "#888888",
        "shadow": "bg:#222222",
        "menu-bar": "bg:#aaaaaa #888888",
        "menu-bar.selected-item": "bg:#ffffff #000000",
        "menu": "bg:#888888 #ffffff",
        "menu.border": "#aaaaaa",
        "window.border shadow": "#444444",
        "focused  button": "bg:#880000 #ffffff noinherit",
        # Styling for Dialog widgets.
        "button-bar": "bg:#aaaaff",
    }
)

application = Application(
    layout=Layout(root_container, focused_element=main_container),
    key_bindings=bindings,
    style=style,
    mouse_support=True,
    full_screen=True,
)

if __name__ == "__main__":
    application.run()
