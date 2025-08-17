#!/usr/bin/env python3
"""
Приклад використання API Тесту Белбіна
Демонструє, як використовувати модулі програми програмно
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.belbin_test import BelbinTest
from utils.database import (
    init_database, save_test_result, get_user_results, 
    get_all_results, get_statistics
)
from utils.chart_generator import (
    generate_pie_chart, generate_comparison_chart, 
    generate_statistics_chart
)


def example_api_usage():
    """Приклад використання API"""
    print("Приклад використання API Тесту Белбіна\n")
    
    # 1. Ініціалізація
    init_database()
    belbin_test = BelbinTest()
    
    # 2. Створення тестових користувачів
    test_users = [
        {
            "name": "Олександр Менеджер",
            "answers": {0: "coordinator", 1: "shaper", 2: "coordinator", 3: "shaper", 4: "coordinator", 5: "implementer", 6: "coordinator"}
        },
        {
            "name": "Марія Креативна", 
            "answers": {0: "plant", 1: "plant", 2: "plant", 3: "resource_investigator", 4: "plant", 5: "plant", 6: "specialist"}
        },
        {
            "name": "Андрій Аналітик",
            "answers": {0: "monitor_evaluator", 1: "implementer", 2: "monitor_evaluator", 3: "monitor_evaluator", 4: "monitor_evaluator", 5: "completer_finisher", 6: "implementer"}
        }
    ]
    
    results_list = []
    
    # 3. Обробка кожного користувача
    for user in test_users:
        print(f"Обробка користувача: {user['name']}")
        
        # Розрахунок результатів
        results = belbin_test.calculate_results(user['answers'])
        results_list.append({"user_name": user['name'], "results": results})
        
        # Збереження в БД
        save_test_result(user['name'], results)
        
        # Отримання основних ролей
        primary_roles = belbin_test.get_primary_roles(results, 2)
        print(f"  Основні ролі: {primary_roles}")
        
        # Генерація індивідуальної діаграми
        try:
            chart_path = generate_pie_chart(results, user['name'])
            print(f"  Діаграма: {os.path.basename(chart_path)}")
        except Exception as e:
            print(f"  Помилка діаграми: {e}")
    
    print("\n" + "="*50)
    
    # 4. Аналіз всіх результатів
    print("Аналіз результатів:")
    
    all_results = get_all_results()
    print(f"Всього результатів в БД: {len(all_results)}")
    
    # 5. Статистика
    stats = get_statistics()
    print(f"\nСтатистика:")
    print(f"  Всього тестів: {stats['total_tests']}")
    print(f"  Унікальних користувачів: {stats['unique_users']}")
    print("  Популярні ролі:")
    for role, count in stats['popular_roles'][:5]:
        role_name = belbin_test.role_descriptions.get(role, {}).get('name', role)
        print(f"    {role_name}: {count}")
    
    # 6. Порівняльна діаграма
    try:
        comparison_path = generate_comparison_chart(results_list)
        print(f"\nПорівняльна діаграма: {os.path.basename(comparison_path)}")
    except Exception as e:
        print(f"Помилка порівняльної діаграми: {e}")
    
    # 7. Діаграма статистики
    try:
        stats_path = generate_statistics_chart(stats)
        print(f"Діаграма статистики: {os.path.basename(stats_path)}")
    except Exception as e:
        print(f"Помилка діаграми статистики: {e}")
    
    # 8. Приклад отримання результатів користувача
    print(f"\nІсторія користувача 'Олександр Менеджер':")
    user_history = get_user_results("Олександр Менеджер")
    for result in user_history:
        print(f"  Дата: {result['test_date']}")
        print(f"  Основна роль: {result['primary_role']}")
        print(f"  Додаткова роль: {result['secondary_role']}")
    
    print(f"\nУсі файли збережено в директорії data/charts/")


if __name__ == "__main__":
    example_api_usage()