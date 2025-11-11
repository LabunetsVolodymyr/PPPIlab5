import tkinter as tk

# ----------------------------------------------------------------------
# ЧАСТИНА 1: ЛОГІКА КАЛЬКУЛЯТОРА (МОДЕЛЬ) - за це відповідає Влад
# ----------------------------------------------------------------------

class Calculator:
    """
    Відповідає виключно за математичну логіку.
    Не має жодного уявлення про графічний інтерфейс.
    """
    def __init__(self):
        """Ініціалізує стан калькулятора."""
        self.current_expression = ""

    def process_input(self, value):
        """
        Обробляє одне натискання кнопки (наприклад, '5', '+', 'C', '=').
        Це головний метод, який викликає контролер.
        """
        if value == 'C':
            self.clear()
        elif value == '=':
            self._calculate()
        elif value == '←': # Додамо кнопку "стерти" для зручності
             self.current_expression = self.current_expression[:-1]
        else:
            # Просто додаємо символ до рядка
            self.current_expression += str(value)

    def _calculate(self):
        """
        Приватний метод для виконання фактичного обчислення
        виразу, що зберігається.
        """
        try:
            # eval() - це небезпечна функція для реальних програм (через
            # вразливості), але для простого калькулятора вона ідеальна.
            result = str(eval(self.current_expression))
            self.current_expression = result
        except ZeroDivisionError:
            self.current_expression = "Помилка (діл. 0)"
        except Exception:
            self.current_expression = "Помилка (вираз)"


    def clear(self):
        """
        Скидає поточний стан калькулятора.
        """
        self.current_expression = ""

    def get_display_value(self):
        """
        Повертає поточне значення, яке має відображатися на екрані.
        Якщо рядок порожній, показуємо "0".
        """
        return self.current_expression or "0"

# ----------------------------------------------------------------------
# ЧАСТИНА 2: ГРАФІЧНИЙ ІНТЕРФЕЙС (ВИГЛЯД) - за це відповідає Саша
# ----------------------------------------------------------------------

class CalculatorGUI:
    """
    Відповідає виключно за створення та розміщення віджетів.
    Нічого не знає про те, як виконувати обчислення.
    """
    def __init__(self, root, controller):
        """
        Налаштовує головне вікно та зберігає посилання на контролер,
        щоб мати можливість надсилати йому події (натискання кнопок).
        """
        self.controller = controller
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x470") # Задамо фіксований розмір
        self.root.resizable(False, False)
        
        # Спеціальна змінна tkinter для відстеження тексту на екрані
        self.display_var = tk.StringVar()
        
        self.setup_ui()
        self.update_display("0") # Початкове значення

    def setup_ui(self):
        """
        Створює всі необхідні віджети (екран, кнопки)
        і розміщує їх у вікні.
        """
        # Створення екрану (Entry widget)
        display_font = ('Arial', 24)
        display = tk.Entry(self.root, 
                             textvariable=self.display_var, 
                             font=display_font, 
                             bd=10, 
                             insertwidth=2, 
                             width=14, 
                             justify='right',
                             state='readonly') # 'readonly' - не можна писати з клавіатури
        display.pack(pady=10)

        # Створення контейнера (Frame) для кнопок
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        # Визначення кнопок (рядок за рядком)
        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('C', '0', '=', '+'),
            ('(', ')', '←', '.') # Додамо ще кнопок
        ]
        # Створення кнопок у циклі
        button_font = ('Arial', 18)
        for i, row in enumerate(buttons):
            for j, value in enumerate(row):
                # 'lambda' потрібна, щоб кожна кнопка "запам'ятала" своє значення 'value'
                cmd = lambda v=value: self._on_button_click(v)
                
                button = tk.Button(button_frame, 
                                   text=value, 
                                   font=button_font, 
                                   width=4, 
                                   height=2,
                                   command=cmd)
                button.grid(row=i, column=j, padx=2, pady=2)

    def _on_button_click(self, value):
        """
        Приватний метод, який викликається при натисканні будь-якої кнопки GUI.
        Він просто передає значення кнопки контролеру.
        """
        self.controller.handle_button_press(value)

    def update_display(self, text):
        """
        Публічний метод, який контролер може викликати,
        щоб оновити текст на екрані калькулятора.
        """
        self.display_var.set(text)
        
# ----------------------------------------------------------------------
# ЧАСТИНА 3: ЛОГІКА ПРОГРАМИ (КОНТРОЛЕР) - за це відповідає Влад
# ----------------------------------------------------------------------

class CalculatorApp:
    """
    З'єднує Логіку (Calculator) та GUI (CalculatorGUI).
    Керує потоком даних між ними.
    """
    def __init__(self, root):
        """
        Ініціалізує Модель (логіку) та Вигляд (GUI)
        і пов'язує їх.
        """
        self.model = Calculator()
        # Передаємо 'self' (тобто цей екземпляр CalculatorApp) як контролер
        self.view = CalculatorGUI(root, self)

    def handle_button_press(self, value):
        """
        Цей метод викликається з GUI, коли користувач натискає кнопку.
        """
        # 1. Надіслати ввід користувача в модель
        self.model.process_input(value)

        # 2. Отримати оновлене значення з моделі
        display_text = self.model.get_display_value()

        # 3. Надіслати нове значення для відображення у GUI
        self.view.update_display(display_text)


# ----------------------------------------------------------------------
# ТОЧКА ВХОДУ
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Створюємо головне вікно
    main_window = tk.Tk()

    # Запускаємо контролер програми
    app = CalculatorApp(main_window)

    # Запускаємо головний цикл програми
    main_window.mainloop()