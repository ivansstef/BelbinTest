#!/usr/bin/env python3
"""
Головний файл для запуску Тесту Белбіна
Belbin Test - психологічний тест для визначення командних ролей
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Додаємо шлях до модулів проєкту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.tkinter_interface import BelbinTestApp
from utils.database import init_database


def main():
    """Головна функція запуску програми"""
    try:
        # Ініціалізація бази даних
        init_database()
        
        # Створення та запуск Tkinter GUI
        root = tk.Tk()
        app = BelbinTestApp(root)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка під час запуску програми: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()