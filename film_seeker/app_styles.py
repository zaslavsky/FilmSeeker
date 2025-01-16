from prompt_toolkit.styles import Style

black_white =  Style.from_dict({
    # Основной фон и текст
    "": "bg:#000000 #ffffff",  # Черный фон, белый текст
    "dialog.body": "bg:#000000 #ffffff",  # Тело диалога

    # Заголовки (например, для Frame)
    "frame.border": "bg:#000000 #ffffff",  # Белая рамка
    "frame.title": "bold #ffffff",  # Жирный белый текст для заголовков

    # Кнопки
    "button": "bg:#000000 #ffffff",  # Белый текст, черный фон
    "button.focused": "bg:#ffffff #000000 bold",  # Черный текст, белый фон при фокусе

    # Метки (Label)
    "label": "bg:#000000 #ffffff",  # Белый текст на черном фоне

    # Ввод текста
    "input-field": "bg:#000000 #ffffff",  # Белый текст в поле ввода
    "input-field.cursor": "bg:#ffffff #000000",  # Белый фон для курсора

    # Прокрутка
    "scrollbar": "bg:#000000 #808080",  # Черный фон, серый цвет для полосы
    "scrollbar.arrow": "bg:#808080 #000000",  # Серые стрелки
    "scrollbar.button": "bg:#808080",  # Серые кнопки

    # Выборы (Checkbox, Radio)
    "checkbox": "bg:#000000 #ffffff",  # Белый текст для чекбокса
    "checkbox.focused": "bg:#ffffff #000000 bold",  # Черный текст, белый фон при фокусе

    "radio": "bg:#000000 #ffffff",  # Радиокнопка
    "radio.focused": "bg:#ffffff #000000 bold",  # Черный текст, белый фон при фокусе

    # Подсказки (Toolbars, Menus)
    "menu-bar": "bg:#000000 #ffffff",  # Черный фон, белый текст
    "menu-bar.selected-item": "bg:#ffffff #000000",  # Белый фон, черный текст для выбранного элемента

    # Ошибки и предупреждения
    "error": "bg:#000000 #ff0000 bold",  # Красный текст для ошибок
    "warning": "bg:#000000 #ffff00 bold",  # Желтый текст для предупреждений

    # Активные элементы
    "focused": "bg:#ffffff #000000 bold",  # Белый фон, черный текст для активных элементов
})

cold_steel = Style.from_dict(
    {
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
    }
)

matrix_style = Style.from_dict({
    # Основной фон и текст
    "": "bg:#000000 #00ff00",  # Черный фон, зеленый текст
    "dialog.body": "bg:#000000 #00ff00",  # Тело диалога

    # Заголовки (например, для Frame)
    "frame.border": "bg:#000000 #00ff00",  # Зеленая рамка
    "frame.title": "bold #00ff00",  # Жирный зеленый текст для заголовков

    # Кнопки
    "button": "bg:#000000 #00ff00",  # Зеленый текст, черный фон
    "button.focused": "bg:#00ff00 #000000 bold",  # Черный текст, зеленый фон при фокусе
    

    # Метки (Label)
    "label": "bg:#000000 #00ff00",  # Зеленый текст на черном фоне

    # Ввод текста
    "input-field": "bg:#000000 #00ff00",  # Зеленый текст в поле ввода
    "input-field.cursor": "bg:#00ff00 #000000",  # Зеленый фон для курсора

    # Прокрутка
    "scrollbar": "bg:#003300",  # Темно-зеленый фон
    "scrollbar.arrow": "bg:#00ff00 #000000",  # Зеленые стрелки
    "scrollbar.button": "bg:#00ff00",  # Зеленая кнопка

    # Выборы (Checkbox, Radio)
    "checkbox": "bg:#000000 #00ff00",  # Зеленый текст для чекбокса
    "checkbox.focused": "bg:#00ff00 #000000",  # Зеленый фон при фокусе

    "radio": "bg:#000000 #00ff00",  # Радиокнопка
    "radio.focused": "bg:#00ff00 #000000",  # Зеленый фон при фокусе

    # Подсказки (Toolbars, Menus)
    "menu-bar": "bg:#003300 #00ff00",  # Темно-зеленый фон, яркий текст
    "menu-bar.selected-item": "bg:#00ff00 #000000",  # Выбранный элемент меню

    # Ошибки и предупреждения
    "error": "bg:#000000 #ff0000 bold",  # Красный текст для ошибок
    "warning": "bg:#000000 #ffff00 bold",  # Желтый текст для предупреждений

    # Активные элементы
    "focused": "bg:#00ff00 #000000",  # Черный текст, зеленый фон для активных элементов
})

cozy_warm_style = Style.from_dict({
    # Основной фон и текст
    "": "bg:#3e2c1c #f4e3c1",  # Тёплый коричневый фон, кремовый текст
    "dialog.body": "bg:#3e2c1c #f4e3c1",  # Тело диалога

    # Заголовки (например, для Frame)
    "frame.border": "bg:#3e2c1c #d8a67c",  # Светло-коричневая рамка
    "frame.title": "bold #f4e3c1",  # Жирный кремовый текст для заголовков

    # Кнопки
    "button": "bg:#d8a67c #3e2c1c",  # Светло-коричневый фон, тёмный текст
    "button.focused": "bg:#f4e3c1 #3e2c1c bold",  # Кремовый фон при фокусе

    # Метки (Label)
    "label": "bg:#3e2c1c #f4e3c1",  # Кремовый текст на тёплом коричневом фоне

    # Ввод текста
    "input-field": "bg:#d8a67c #3e2c1c",  # Светло-коричневый фон, тёмный текст
    "input-field.cursor": "bg:#f4e3c1 #3e2c1c",  # Кремовый фон для курсора

    # Прокрутка
    "scrollbar": "bg:#5a3f2e",  # Тёмно-коричневый фон
    "scrollbar.arrow": "bg:#d8a67c #3e2c1c",  # Светло-коричневый фон для стрелок
    "scrollbar.button": "bg:#d8a67c",  # Светло-коричневая кнопка

    # Выборы (Checkbox, Radio)
    "checkbox": "bg:#d8a67c #3e2c1c",  # Светло-коричневый фон
    "checkbox.focused": "bg:#f4e3c1 #3e2c1c bold",  # Кремовый фон при фокусе

    "radio": "bg:#d8a67c #3e2c1c",  # Радиокнопка
    "radio.focused": "bg:#f4e3c1 #3e2c1c bold",  # Кремовый фон при фокусе

    # Подсказки (Toolbars, Menus)
    "menu-bar": "bg:#5a3f2e #f4e3c1",  # Тёмно-коричневый фон, кремовый текст
    "menu-bar.selected-item": "bg:#f4e3c1 #3e2c1c",  # Кремовый фон для выбранного элемента

    # Ошибки и предупреждения
    "error": "bg:#3e2c1c #ff6f61 bold",  # Тёплый красноватый цвет для ошибок
    "warning": "bg:#3e2c1c #ffc107 bold",  # Тёплый жёлтый цвет для предупреждений

    # Активные элементы
    "focused": "bg:#f4e3c1 #3e2c1c bold",  # Кремовый фон для активных элементов
})
