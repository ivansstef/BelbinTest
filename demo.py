#!/usr/bin/env python3
"""
Демонстраційний скрипт для тестування функціональності Тесту Белбіна
без GUI (для консольного режиму)
"""

import sys
import os

# Додаємо шлях до модулів проєкту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.belbin_test import BelbinTest
from utils.database import init_database, save_test_result, get_statistics
from utils.chart_generator import generate_pie_chart


def console_demo():
    """Демонстрація роботи тесту в консольному режимі"""
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ТЕСТУ БЕЛБІНА")
    print("=" * 60)
    
    # Ініціалізація
    print("\n1. Ініціалізація компонентів...")
    init_database()
    belbin_test = BelbinTest()
    print("✅ База даних ініціалізована")
    print("✅ Тест Белбіна готовий")
    
    # Показ інформації про тест
    print(f"\n2. Інформація про тест:")
    print(f"   Кількість питань: {len(belbin_test.questions)}")
    print(f"   Кількість ролей: {len(belbin_test.role_descriptions)}")
    
    # Показ ролей
    print(f"\n3. Командні ролі Белбіна:")
    for role, info in belbin_test.role_descriptions.items():
        print(f"   • {info['name']}")
        print(f"     {info['description']}")
    
    # Симуляція проходження тесту
    print(f"\n4. Симуляція проходження тесту...")
    user_name = "Демо Користувач"
    
    # Приклад відповідей (перші 3 питання)
    demo_answers = {
        0: "plant",  # Генератор ідей
        1: "coordinator",  # Координатор  
        2: "shaper",  # Формувач
        3: "plant",  # Знову генератор ідей
        4: "monitor_evaluator",  # Аналітик
        5: "coordinator",  # Знову координатор
        6: "teamworker"  # Командний гравець
    }
    
    print(f"   Відповіді користувача: {demo_answers}")
    
    # Розрахунок результатів
    results = belbin_test.calculate_results(demo_answers)
    print(f"\n5. Результати тесту:")
    
    # Показ результатів
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for role, score in sorted_results:
        if score > 0:
            role_name = belbin_test.role_descriptions[role]["name"]
            print(f"   {role_name}: {score} балів")
    
    # Збереження в базу даних
    print(f"\n6. Збереження результатів...")
    try:
        save_result = save_test_result(user_name, results)
        if save_result:
            print("✅ Результати збережено в базу даних")
        else:
            print("❌ Помилка збереження результатів")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    
    # Генерація діаграми
    print(f"\n7. Генерація діаграми...")
    try:
        chart_path = generate_pie_chart(results, user_name)
        print(f"✅ Діаграма збережена: {chart_path}")
    except Exception as e:
        print(f"❌ Помилка генерації діаграми: {e}")
    
    # Інтерпретація результатів
    print(f"\n8. Інтерпретація результатів:")
    interpretation = belbin_test.get_role_interpretation(results)
    print(interpretation)
    
    # Статистика
    print(f"\n9. Статистика:")
    try:
        stats = get_statistics()
        print(f"   Всього тестів: {stats['total_tests']}")
        print(f"   Унікальних користувачів: {stats['unique_users']}")
        if stats['popular_roles']:
            print("   Популярні ролі:")
            for role, count in stats['popular_roles'][:3]:
                role_name = belbin_test.role_descriptions.get(role, {}).get('name', role)
                print(f"     • {role_name}: {count} раз(и)")
    except Exception as e:
        print(f"   Помилка отримання статистики: {e}")
    
    print(f"\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("Запустіть 'python main.py' для роботи з GUI")
    print("=" * 60)


if __name__ == "__main__":
    console_demo()