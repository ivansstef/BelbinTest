"""
Графічний інтерфейс для Тесту Белбіна
Використовує Tkinter для створення GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
from utils.belbin_test import BelbinTest
from utils.database import save_test_result
from utils.chart_generator import generate_pie_chart


class BelbinTestApp:
    """Основний клас GUI програми"""
    
    def __init__(self, root):
        """Ініціалізація додатку"""
        self.root = root
        self.root.title("Тест Белбіна - Визначення командних ролей")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')
        
        # Ініціалізація тесту Белбіна
        self.belbin_test = BelbinTest()
        
        # Змінні для збереження даних
        self.user_name = tk.StringVar()
        self.current_question = 0
        self.answers = {}
        
        # Створення головного фрейму
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Налаштування сітки
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Запуск з екрану введення імені
        self.show_name_input()
    
    def show_name_input(self):
        """Показує екран введення імені користувача"""
        # Очищення фрейму
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Заголовок
        title_label = ttk.Label(
            self.main_frame, 
            text="Тест Белбіна", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Підзаголовок
        subtitle_label = ttk.Label(
            self.main_frame, 
            text="Визначення ваших командних ролей", 
            font=("Arial", 14)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Поле введення імені
        name_label = ttk.Label(self.main_frame, text="Введіть ваше ім'я:")
        name_label.grid(row=2, column=0, pady=(0, 10))
        
        name_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.user_name, 
            font=("Arial", 12),
            width=30
        )
        name_entry.grid(row=3, column=0, pady=(0, 20))
        name_entry.focus()
        
        # Кнопка початку тесту
        start_button = ttk.Button(
            self.main_frame, 
            text="Почати тест", 
            command=self.start_test
        )
        start_button.grid(row=4, column=0)
        
        # Обробка Enter
        name_entry.bind('<Return>', lambda event: self.start_test())
    
    def start_test(self):
        """Починає тест після введення імені"""
        if not self.user_name.get().strip():
            messagebox.showwarning("Попередження", "Будь ласка, введіть ваше ім'я")
            return
        
        self.current_question = 0
        self.answers = {}
        self.show_question()
    
    def show_question(self):
        """Показує поточне питання тесту"""
        if self.current_question >= len(self.belbin_test.questions):
            self.show_results()
            return
        
        # Очищення фрейму
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        question_data = self.belbin_test.questions[self.current_question]
        
        # Прогрес-бар
        progress_label = ttk.Label(
            self.main_frame, 
            text=f"Питання {self.current_question + 1} з {len(self.belbin_test.questions)}"
        )
        progress_label.grid(row=0, column=0, pady=(0, 10))
        
        # Питання
        question_label = ttk.Label(
            self.main_frame, 
            text=question_data["question"], 
            font=("Arial", 12),
            wraplength=600
        )
        question_label.grid(row=1, column=0, pady=(0, 20))
        
        # Варіанти відповідей
        self.answer_var = tk.StringVar()
        
        for i, option in enumerate(question_data["options"]):
            radio_button = ttk.Radiobutton(
                self.main_frame,
                text=option["text"],
                variable=self.answer_var,
                value=option["role"]
            )
            radio_button.grid(row=2+i, column=0, sticky=tk.W, pady=2)
        
        # Кнопки навігації
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2+len(question_data["options"]), column=0, pady=20)
        
        if self.current_question > 0:
            back_button = ttk.Button(
                button_frame, 
                text="Назад", 
                command=self.previous_question
            )
            back_button.grid(row=0, column=0, padx=(0, 10))
        
        next_button = ttk.Button(
            button_frame, 
            text="Далі", 
            command=self.next_question
        )
        next_button.grid(row=0, column=1)
    
    def next_question(self):
        """Переходить до наступного питання"""
        if not self.answer_var.get():
            messagebox.showwarning("Попередження", "Будь ласка, оберіть відповідь")
            return
        
        self.answers[self.current_question] = self.answer_var.get()
        self.current_question += 1
        self.show_question()
    
    def previous_question(self):
        """Повертається до попереднього питання"""
        self.current_question -= 1
        self.show_question()
    
    def show_results(self):
        """Показує результати тесту"""
        # Розрахунок результатів
        results = self.belbin_test.calculate_results(self.answers)
        
        # Збереження в базу даних
        try:
            save_test_result(self.user_name.get(), results)
        except Exception as e:
            messagebox.showwarning("Попередження", f"Не вдалося зберегти результати: {str(e)}")
        
        # Очищення фрейму
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Заголовок результатів
        title_label = ttk.Label(
            self.main_frame, 
            text=f"Результати тесту для {self.user_name.get()}", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Створення скрольованого тексту для результатів
        results_text = scrolledtext.ScrolledText(
            self.main_frame, 
            width=80, 
            height=20,
            wrap=tk.WORD
        )
        results_text.grid(row=1, column=0, pady=(0, 20))
        
        # Додавання результатів
        results_text.insert(tk.END, "ВАШІ КОМАНДНІ РОЛІ:\n\n")
        
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        for role, score in sorted_results:
            role_name = self.belbin_test.role_descriptions[role]["name"]
            description = self.belbin_test.role_descriptions[role]["description"]
            results_text.insert(tk.END, f"{role_name}: {score} балів\n")
            results_text.insert(tk.END, f"Опис: {description}\n\n")
        
        results_text.config(state=tk.DISABLED)
        
        # Кнопки
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0)
        
        chart_button = ttk.Button(
            button_frame, 
            text="Показати діаграму", 
            command=lambda: self.show_chart(results)
        )
        chart_button.grid(row=0, column=0, padx=(0, 10))
        
        restart_button = ttk.Button(
            button_frame, 
            text="Пройти тест заново", 
            command=self.show_name_input
        )
        restart_button.grid(row=0, column=1)
    
    def show_chart(self, results):
        """Показує кругову діаграму результатів"""
        try:
            chart_path = generate_pie_chart(results, self.user_name.get())
            messagebox.showinfo("Діаграма", f"Діаграма збережена як: {chart_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося створити діаграму: {str(e)}")