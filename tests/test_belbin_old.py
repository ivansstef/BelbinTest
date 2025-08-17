"""
Unit tests for the Belbin Test application.
"""

import unittest
import tempfile
import os
import sys

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.data_processing import BelbinTest, DatabaseManager


class TestBelbinTest(unittest.TestCase):
    """Test cases for BelbinTest class."""
    
    def test_roles_definition(self):
        """Test that all required roles are defined."""
        expected_roles = ['PL', 'RI', 'CO', 'SH', 'ME', 'TW', 'IMP', 'CF', 'SP']
        self.assertEqual(set(BelbinTest.ROLES.keys()), set(expected_roles))
    
    def test_questions_structure(self):
        """Test that questions are properly structured."""
        self.assertGreater(len(BelbinTest.QUESTIONS), 0)
        
        for question in BelbinTest.QUESTIONS:
            self.assertIn('question', question)
            self.assertIn('options', question)
            self.assertIsInstance(question['options'], dict)
            
            # Check that each option has text and role mapping
            for option_key, option_data in question['options'].items():
                self.assertIsInstance(option_data, tuple)
                self.assertEqual(len(option_data), 2)
                text, role = option_data
                self.assertIsInstance(text, str)
                self.assertIn(role, BelbinTest.ROLES.keys())
    
    def test_calculate_scores_empty(self):
        """Test score calculation with empty answers."""
        scores = BelbinTest.calculate_scores({})
        
        # Should return all roles with 0 scores
        self.assertEqual(len(scores), len(BelbinTest.ROLES))
        for role in BelbinTest.ROLES.keys():
            self.assertIn(role, scores)
            self.assertEqual(scores[role], 0)
    
    def test_calculate_scores_sample(self):
        """Test score calculation with sample answers."""
        # Sample answers for first question
        sample_answers = {
            0: {
                'a': 3,  # RI
                'b': 2,  # TW
                'c': 5,  # PL
                'd': 0,  # CO
                'e': 0,  # IMP
                'f': 0,  # SH
                'g': 0,  # ME
                'h': 0   # ME
            }
        }
        
        scores = BelbinTest.calculate_scores(sample_answers)
        
        self.assertEqual(scores['RI'], 3)
        self.assertEqual(scores['TW'], 2)
        self.assertEqual(scores['PL'], 5)
        self.assertEqual(scores['CO'], 0)
    
    def test_get_dominant_roles(self):
        """Test getting dominant roles."""
        scores = {
            'PL': 15,
            'RI': 12,
            'CO': 8,
            'SH': 5,
            'ME': 3,
            'TW': 2,
            'IMP': 1,
            'CF': 1,
            'SP': 0
        }
        
        top_3 = BelbinTest.get_dominant_roles(scores, 3)
        
        self.assertEqual(len(top_3), 3)
        self.assertEqual(top_3[0], ('PL', 15))
        self.assertEqual(top_3[1], ('RI', 12))
        self.assertEqual(top_3[2], ('CO', 8))


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager class."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_results.db')
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_database_initialization(self):
        """Test that database is properly initialized."""
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_save_and_retrieve_results(self):
        """Test saving and retrieving results."""
        username = "test_user"
        scores = {
            'PL': 10,
            'RI': 8,
            'CO': 6,
            'SH': 4,
            'ME': 2,
            'TW': 1,
            'IMP': 1,
            'CF': 1,
            'SP': 0
        }
        
        # Save results
        result_id = self.db_manager.save_results(username, scores)
        self.assertIsInstance(result_id, int)
        self.assertGreater(result_id, 0)
        
        # Retrieve results
        user_results = self.db_manager.get_user_results(username)
        self.assertEqual(len(user_results), 1)
        
        result = user_results[0]
        self.assertEqual(result['username'], username)
        self.assertEqual(result['pl_score'], 10)
        self.assertEqual(result['ri_score'], 8)
        self.assertEqual(result['co_score'], 6)
    
    def test_get_all_results(self):
        """Test retrieving all results."""
        # Save multiple results
        self.db_manager.save_results("user1", {'PL': 10, 'RI': 5, 'CO': 0, 'SH': 0, 'ME': 0, 'TW': 0, 'IMP': 0, 'CF': 0, 'SP': 0})
        self.db_manager.save_results("user2", {'PL': 5, 'RI': 10, 'CO': 0, 'SH': 0, 'ME': 0, 'TW': 0, 'IMP': 0, 'CF': 0, 'SP': 0})
        
        all_results = self.db_manager.get_all_results()
        self.assertEqual(len(all_results), 2)
    
    def test_empty_database(self):
        """Test operations on empty database."""
        user_results = self.db_manager.get_user_results("nonexistent_user")
        self.assertEqual(len(user_results), 0)
        
        all_results = self.db_manager.get_all_results()
        self.assertEqual(len(all_results), 0)


if __name__ == '__main__':
    unittest.main()