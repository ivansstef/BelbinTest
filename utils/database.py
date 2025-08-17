"""
Модуль для роботи з базою даних
Використовує SQLAlchemy для збереження результатів тестів
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Створення базового класу для моделей
Base = declarative_base()

# Шлях до бази даних
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'belbin_results.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Створення engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestResult(Base):
    """Модель для збереження результатів тестів"""
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    test_date = Column(DateTime, default=datetime.utcnow)
    results_json = Column(Text, nullable=False)  # JSON з результатами
    primary_role = Column(String(50))  # Основна роль
    secondary_role = Column(String(50))  # Додаткова роль
    
    def __repr__(self):
        return f"<TestResult(user_name='{self.user_name}', test_date='{self.test_date}', primary_role='{self.primary_role}')>"


def init_database():
    """Ініціалізація бази даних"""
    try:
        # Створення директорії data, якщо вона не існує
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        # Створення всіх таблиць
        Base.metadata.create_all(bind=engine)
        
        return True
    except Exception as e:
        print(f"Помилка ініціалізації бази даних: {e}")
        return False


def save_test_result(user_name, results):
    """
    Зберігає результат тесту в базі даних
    
    Args:
        user_name (str): Ім'я користувача
        results (dict): Результати тесту
    
    Returns:
        bool: True якщо збереження успішне, False інакше
    """
    try:
        # Створення сесії
        db = SessionLocal()
        
        # Визначення основної та додаткової ролі
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        primary_role = sorted_results[0][0] if sorted_results[0][1] > 0 else None
        secondary_role = sorted_results[1][0] if len(sorted_results) > 1 and sorted_results[1][1] > 0 else None
        
        # Створення запису
        test_result = TestResult(
            user_name=user_name,
            results_json=json.dumps(results, ensure_ascii=False),
            primary_role=primary_role,
            secondary_role=secondary_role
        )
        
        # Додавання до сесії та збереження
        db.add(test_result)
        db.commit()
        
        # Також зберігаємо в JSON файл для резервного копіювання
        save_to_json_backup(user_name, results)
        
        return True
        
    except SQLAlchemyError as e:
        print(f"Помилка SQLAlchemy: {e}")
        db.rollback()
        return False
    except Exception as e:
        print(f"Загальна помилка збереження: {e}")
        return False
    finally:
        db.close()


def save_to_json_backup(user_name, results):
    """Зберігає результати в JSON файл як резервну копію"""
    try:
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'results.json')
        
        # Читання існуючих даних
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
        
        # Додавання нового результату
        new_result = {
            "user_name": user_name,
            "test_date": datetime.now().isoformat(),
            "results": results
        }
        data.append(new_result)
        
        # Збереження оновлених даних
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Помилка збереження JSON резервної копії: {e}")


def get_user_results(user_name):
    """
    Отримує всі результати тестів для конкретного користувача
    
    Args:
        user_name (str): Ім'я користувача
    
    Returns:
        list: Список результатів тестів
    """
    try:
        db = SessionLocal()
        results = db.query(TestResult).filter(TestResult.user_name == user_name).all()
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "user_name": result.user_name,
                "test_date": result.test_date,
                "results": json.loads(result.results_json),
                "primary_role": result.primary_role,
                "secondary_role": result.secondary_role
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"Помилка отримання результатів: {e}")
        return []
    finally:
        db.close()


def get_all_results():
    """
    Отримує всі результати тестів
    
    Returns:
        list: Список всіх результатів тестів
    """
    try:
        db = SessionLocal()
        results = db.query(TestResult).all()
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "user_name": result.user_name,
                "test_date": result.test_date,
                "results": json.loads(result.results_json),
                "primary_role": result.primary_role,
                "secondary_role": result.secondary_role
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"Помилка отримання всіх результатів: {e}")
        return []
    finally:
        db.close()


def delete_user_results(user_name):
    """
    Видаляє всі результати тестів для конкретного користувача
    
    Args:
        user_name (str): Ім'я користувача
    
    Returns:
        bool: True якщо видалення успішне, False інакше
    """
    try:
        db = SessionLocal()
        deleted_count = db.query(TestResult).filter(TestResult.user_name == user_name).delete()
        db.commit()
        
        return deleted_count > 0
        
    except Exception as e:
        print(f"Помилка видалення результатів: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def get_statistics():
    """
    Отримує статистику по всіх тестах
    
    Returns:
        dict: Словник зі статистикою
    """
    try:
        db = SessionLocal()
        
        total_tests = db.query(TestResult).count()
        unique_users = db.query(TestResult.user_name).distinct().count()
        
        # Підрахунок найпопулярніших ролей
        all_results = db.query(TestResult.primary_role).all()
        role_counts = {}
        for result in all_results:
            if result.primary_role:
                role_counts[result.primary_role] = role_counts.get(result.primary_role, 0) + 1
        
        return {
            "total_tests": total_tests,
            "unique_users": unique_users,
            "popular_roles": sorted(role_counts.items(), key=lambda x: x[1], reverse=True)
        }
        
    except Exception as e:
        print(f"Помилка отримання статистики: {e}")
        return {
            "total_tests": 0,
            "unique_users": 0,
            "popular_roles": []
        }
    finally:
        db.close()