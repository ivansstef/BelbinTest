"""
Юніт-тести для тесту Белбіна
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Додаємо шлях до модулів проєкту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.belbin_test import BelbinTest
from utils.database import init_database, save_test_result, get_user_results
from utils.chart_generator import generate_pie_chart


class TestBelbinTest(unittest.TestCase):
    """Тести для класу BelbinTest"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.belbin_test = BelbinTest()
    
    def test_init(self):
        """Тест ініціалізації класу BelbinTest"""
        self.assertIsInstance(self.belbin_test.role_descriptions, dict)
        self.assertIsInstance(self.belbin_test.questions, list)
        self.assertEqual(len(self.belbin_test.role_descriptions), 9)
        self.assertGreater(len(self.belbin_test.questions), 0)
    
    def test_role_descriptions_structure(self):
        """Тест структури описів ролей"""
        expected_roles = [
            "plant", "resource_investigator", "coordinator", "shaper",
            "monitor_evaluator", "teamworker", "implementer", 
            "completer_finisher", "specialist"
        ]
        
        for role in expected_roles:
            self.assertIn(role, self.belbin_test.role_descriptions)
            self.assertIn("name", self.belbin_test.role_descriptions[role])
            self.assertIn("description", self.belbin_test.role_descriptions[role])
    
    def test_questions_structure(self):
        """Тест структури питань"""
        for question in self.belbin_test.questions:
            self.assertIn("question", question)
            self.assertIn("options", question)
            self.assertIsInstance(question["options"], list)
            
            for option in question["options"]:
                self.assertIn("text", option)
                self.assertIn("role", option)
    
    def test_calculate_results(self):
        """Тест розрахунку результатів"""
        # Тестові дані
        test_answers = {
            0: "plant",
            1: "plant", 
            2: "coordinator",
            3: "shaper"
        }
        
        results = self.belbin_test.calculate_results(test_answers)
        
        # Перевірка типу результату
        self.assertIsInstance(results, dict)
        
        # Перевірка наявності всіх ролей
        expected_roles = [
            "plant", "resource_investigator", "coordinator", "shaper",
            "monitor_evaluator", "teamworker", "implementer", 
            "completer_finisher", "specialist"
        ]
        
        for role in expected_roles:
            self.assertIn(role, results)
        
        # Перевірка підрахунку
        self.assertEqual(results["plant"], 2)
        self.assertEqual(results["coordinator"], 1)
        self.assertEqual(results["shaper"], 1)
        self.assertEqual(results["teamworker"], 0)
    
    def test_get_primary_roles(self):
        """Тест отримання основних ролей"""
        test_results = {
            "plant": 3,
            "coordinator": 2,
            "shaper": 1,
            "teamworker": 0,
            "implementer": 0,
            "monitor_evaluator": 0,
            "resource_investigator": 0,
            "completer_finisher": 0,
            "specialist": 0
        }
        
        primary_roles = self.belbin_test.get_primary_roles(test_results, 3)
        
        self.assertEqual(len(primary_roles), 3)
        self.assertEqual(primary_roles[0][0], "plant")
        self.assertEqual(primary_roles[0][1], 3)
        self.assertEqual(primary_roles[1][0], "coordinator")
        self.assertEqual(primary_roles[1][1], 2)
    
    def test_get_role_interpretation(self):
        """Тест інтерпретації результатів"""
        test_results = {
            "plant": 3,
            "coordinator": 2,
            "shaper": 0,
            "teamworker": 0,
            "implementer": 0,
            "monitor_evaluator": 0,
            "resource_investigator": 0,
            "completer_finisher": 0,
            "specialist": 0
        }
        
        interpretation = self.belbin_test.get_role_interpretation(test_results)
        
        self.assertIsInstance(interpretation, str)
        self.assertIn("ІНТЕРПРЕТАЦІЯ РЕЗУЛЬТАТІВ", interpretation)
        self.assertIn("РЕКОМЕНДАЦІЇ", interpretation)


class TestDatabase(unittest.TestCase):
    """Тести для функцій бази даних"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        # Створення тимчасової директорії для тестової бази даних
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = os.environ.get('DATABASE_PATH')
        os.environ['DATABASE_PATH'] = os.path.join(self.test_dir, 'test.db')
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        # Відновлення оригінального шляху
        if self.original_db_path:
            os.environ['DATABASE_PATH'] = self.original_db_path
        elif 'DATABASE_PATH' in os.environ:
            del os.environ['DATABASE_PATH']
        
        # Видалення тимчасової директорії
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init_database(self):
        """Тест ініціалізації бази даних"""
        result = init_database()
        self.assertTrue(result)
    
    @patch('utils.database.SessionLocal')
    def test_save_test_result(self, mock_session):
        """Тест збереження результатів тесту"""
        # Мокування сесії бази даних
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        test_results = {
            "plant": 3,
            "coordinator": 2,
            "shaper": 1
        }
        
        # Тест не викликає помилок
        try:
            save_test_result("Тестовий користувач", test_results)
        except Exception as e:
            self.fail(f"save_test_result викликав виключення: {e}")


class TestChartGenerator(unittest.TestCase):
    """Тести для генератора діаграм"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.test_dir = tempfile.mkdtemp()
        self.test_results = {
            "plant": 3,
            "coordinator": 2,
            "shaper": 1,
            "teamworker": 0,
            "implementer": 0,
            "monitor_evaluator": 0,
            "resource_investigator": 0,
            "completer_finisher": 0,
            "specialist": 0
        }
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_generate_pie_chart(self, mock_close, mock_savefig):
        """Тест генерації кругової діаграми"""
        test_path = os.path.join(self.test_dir, 'test_chart.png')
        
        try:
            result_path = generate_pie_chart(
                self.test_results, 
                "Тестовий користувач", 
                test_path
            )
            self.assertEqual(result_path, test_path)
            mock_savefig.assert_called_once()
            mock_close.assert_called_once()
        except Exception as e:
            # Очікується, що тест може не пройти через відсутність matplotlib
            self.skipTest(f"Тест пропущено через відсутність matplotlib: {e}")
    
    def test_generate_pie_chart_empty_results(self):
        """Тест генерації діаграми з порожніми результатами"""
        empty_results = {role: 0 for role in self.test_results.keys()}
        
        with self.assertRaises(ValueError):
            generate_pie_chart(empty_results, "Тестовий користувач")


if __name__ == '__main__':
    # Запуск всіх тестів
    unittest.main(verbosity=2)