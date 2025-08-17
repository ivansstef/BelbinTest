"""
Модуль для генерації кругових діаграм результатів тесту Белбіна
Використовує matplotlib для створення візуалізацій
"""

import os
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

# Налаштування matplotlib для роботи без GUI
matplotlib.use('Agg')

# Налаштування шрифтів для підтримки української мови
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False


def generate_pie_chart(results, user_name, save_path=None):
    """
    Генерує кругову діаграму результатів тесту Белбіна
    
    Args:
        results (dict): Результати тесту у форматі {роль: бали}
        user_name (str): Ім'я користувача
        save_path (str, optional): Шлях для збереження файлу
    
    Returns:
        str: Шлях до збереженого файлу
    """
    # Фільтрація результатів з ненульовими значеннями
    filtered_results = {role: score for role, score in results.items() if score > 0}
    
    if not filtered_results:
        raise ValueError("Немає даних для побудови діаграми")
    
    # Назви ролей українською
    role_names_ua = {
        "plant": "Генератор ідей",
        "resource_investigator": "Дослідник ресурсів",
        "coordinator": "Координатор",
        "shaper": "Формувач",
        "monitor_evaluator": "Аналітик",
        "teamworker": "Командний гравець",
        "implementer": "Виконавець",
        "completer_finisher": "Фіналіст",
        "specialist": "Спеціаліст"
    }
    
    # Підготовка даних для діаграми
    labels = [role_names_ua.get(role, role) for role in filtered_results.keys()]
    sizes = list(filtered_results.values())
    
    # Кольори для діаграми
    colors = [
        '#FF6B6B',  # Червоний
        '#4ECDC4',  # Бірюзовий
        '#45B7D1',  # Синій
        '#96CEB4',  # Зелений
        '#FFEAA7',  # Жовтий
        '#DDA0DD',  # Фіолетовий
        '#98D8C8',  # М'ятний
        '#F7DC6F',  # Золотий
        '#BB8FCE'   # Лавандовий
    ]
    
    # Створення фігури та осей
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Створення кругової діаграми
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors[:len(labels)],
        autopct='%1.1f%%',
        startangle=90,
        explode=[0.05] * len(labels)  # Невелике розділення секторів
    )
    
    # Налаштування тексту
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    
    # Заголовок
    plt.title(
        f'Результати тесту Белбіна\n{user_name}',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    
    # Рівні пропорції
    ax.axis('equal')
    
    # Легенда з результатами
    legend_labels = [f'{label}: {size} балів' for label, size in zip(labels, sizes)]
    plt.legend(
        wedges, 
        legend_labels,
        title="Командні ролі:",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10
    )
    
    # Визначення шляху збереження
    if save_path is None:
        # Створення директорії для графіків, якщо вона не існує
        charts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        # Генерація імені файлу
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_user_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"belbin_chart_{safe_user_name}_{timestamp}.png"
        save_path = os.path.join(charts_dir, filename)
    
    # Збереження діаграми
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()  # Закриття фігури для звільнення пам'яті
    
    return save_path


def generate_comparison_chart(results_list, save_path=None):
    """
    Генерує діаграму порівняння результатів кількох користувачів
    
    Args:
        results_list (list): Список словників з результатами у форматі 
                           [{"user_name": str, "results": dict}, ...]
        save_path (str, optional): Шлях для збереження файлу
    
    Returns:
        str: Шлях до збереженого файлу
    """
    import numpy as np
    
    if not results_list:
        raise ValueError("Немає даних для порівняння")
    
    # Назви ролей українською
    role_names_ua = {
        "plant": "Генератор ідей",
        "resource_investigator": "Дослідник ресурсів",
        "coordinator": "Координатор",
        "shaper": "Формувач",
        "monitor_evaluator": "Аналітик",
        "teamworker": "Командний гравець",
        "implementer": "Виконавець",
        "completer_finisher": "Фіналіст",
        "specialist": "Спеціаліст"
    }
    
    # Всі можливі ролі
    all_roles = list(role_names_ua.keys())
    role_labels = [role_names_ua[role] for role in all_roles]
    
    # Підготовка даних
    user_names = [item["user_name"] for item in results_list]
    user_data = []
    
    for item in results_list:
        user_scores = [item["results"].get(role, 0) for role in all_roles]
        user_data.append(user_scores)
    
    # Створення фігури
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Позиції стовпців
    x = np.arange(len(role_labels))
    width = 0.8 / len(user_names)  # Ширина стовпців
    
    # Кольори для користувачів
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    # Створення стовпчастої діаграми
    for i, (user_name, scores) in enumerate(zip(user_names, user_data)):
        offset = (i - len(user_names)/2) * width + width/2
        ax.bar(x + offset, scores, width, label=user_name, 
               color=colors[i % len(colors)], alpha=0.8)
    
    # Налаштування осей
    ax.set_xlabel('Командні ролі', fontsize=12, fontweight='bold')
    ax.set_ylabel('Бали', fontsize=12, fontweight='bold')
    ax.set_title('Порівняння результатів тесту Белбіна', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(role_labels, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Визначення шляху збереження
    if save_path is None:
        charts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"belbin_comparison_{timestamp}.png"
        save_path = os.path.join(charts_dir, filename)
    
    # Збереження діаграми
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path


def generate_statistics_chart(statistics, save_path=None):
    """
    Генерує діаграму загальної статистики
    
    Args:
        statistics (dict): Статистика у форматі з функції get_statistics()
        save_path (str, optional): Шлях для збереження файлу
    
    Returns:
        str: Шлях до збереженого файлу
    """
    if not statistics.get("popular_roles"):
        raise ValueError("Немає даних для статистики")
    
    # Назви ролей українською
    role_names_ua = {
        "plant": "Генератор ідей",
        "resource_investigator": "Дослідник ресурсів",
        "coordinator": "Координатор",
        "shaper": "Формувач",
        "monitor_evaluator": "Аналітик",
        "teamworker": "Командний гравець",
        "implementer": "Виконавець",
        "completer_finisher": "Фіналіст",
        "specialist": "Спеціаліст"
    }
    
    # Підготовка даних
    roles = [role_names_ua.get(role, role) for role, _ in statistics["popular_roles"]]
    counts = [count for _, count in statistics["popular_roles"]]
    
    # Створення фігури
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Створення горизонтальної стовпчастої діаграми
    bars = ax.barh(roles, counts, color='#4ECDC4', alpha=0.8)
    
    # Додавання значень на стовпці
    for bar, count in zip(bars, counts):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{count}', ha='left', va='center', fontweight='bold')
    
    # Налаштування
    ax.set_xlabel('Кількість користувачів', fontsize=12, fontweight='bold')
    ax.set_title(f'Популярність командних ролей\n'
                f'Всього тестів: {statistics["total_tests"]}, '
                f'Унікальних користувачів: {statistics["unique_users"]}', 
                fontsize=14, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)
    
    # Визначення шляху збереження
    if save_path is None:
        charts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"belbin_statistics_{timestamp}.png"
        save_path = os.path.join(charts_dir, filename)
    
    # Збереження діаграми
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path