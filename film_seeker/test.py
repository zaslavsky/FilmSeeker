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

database.connect()
print("Подключено успешно!")

def do_exit(something=None):
    get_app().exit(result=False)

def debug_output():
    output_target.text = str([e.values[0][1] for e in Categoryes if e.checked]) + '\n\n\n'+ str(dir(Categoryes[0]))

Categoryes = [Checkbox(text=row.name) for row in Category.select()]

year_completer = WordCompleter([str(film.release_year) for film in Film.select(Film.release_year).distinct()])

result_output_area = TextArea(read_only=True)
name_input_area = TextArea()
year_input_area = TextArea(prompt="Введите год: ", completer=year_completer)
category_input_area = HSplit(Categoryes)

test_button = Button(
    text="Запилить", handler=lambda: debug_output()
)
search_button = Button(
    text="Нйти",
    handler=lambda: serach()
)

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
    # Год писали?
    if year_input_area.text != "":
        query = query.where(Film.release_year == year_input_area.text)
    # Посмотрим что мы там начекбоксили
    Categoryes_list = [e.values[0][1] for e in Categoryes if e.checked]
    # Если что-то начекбоксили то применим доп. фильтр
    if len(Categoryes_list)!=0:
        query = query.where(Category.name.in_(Categoryes_list))

    # ВЫХЛОП
    result = "\n".join([str(i) for i in query.dicts()])
    result_output_area.text = result

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
                Frame(
                    title="Жанры кино",
                    body=category_input_area,
                ),
            ]
        ),
        test_button,
        search_button,
        Frame(body=result_output_area, title="Результаты поиска"),
    ]
)

root_container = MenuContainer(
    body=main_container,
    menu_items=[
        MenuItem("Menu",
                 children=[
                     MenuItem("Help"),
                     MenuItem("About"),
                     MenuItem("Exit", handler=do_exit)  # Допили нормальный хэндлер с диалогом
                     ]
                )
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
# bindings.add("left")(focus_previous)
# bindings.add("right")(focus_next)
bindings.add("c-q")(do_exit)


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


def run():
    application.run()


if __name__ == "__main__":
    run()
