"""
Data processing module for Belbin Test application.
Handles test questions, scoring logic, and database operations.
"""

import sqlite3
import os
from typing import Dict, List, Tuple


class BelbinTest:
    """Handles Belbin test logic and scoring."""
    
    # Belbin team roles
    ROLES = {
        'PL': 'Plant (Creative)',
        'RI': 'Resource Investigator', 
        'CO': 'Coordinator',
        'SH': 'Shaper',
        'ME': 'Monitor Evaluator',
        'TW': 'Teamworker',
        'IMP': 'Implementer',
        'CF': 'Completer Finisher',
        'SP': 'Specialist'
    }
    
    # Test questions with role mappings
    QUESTIONS = [
        {
            'question': 'What I believe I can contribute to a team:',
            'options': {
                'a': ('I think I can quickly spot and take advantage of new opportunities', 'RI'),
                'b': ('I can work well with a very wide range of people', 'TW'),
                'c': ('Producing ideas is one of my natural assets', 'PL'),
                'd': ('My ability rests in being able to draw people out whenever I detect they have something of value to contribute', 'CO'),
                'e': ('My capacity to follow through has much to do with my personal effectiveness', 'IMP'),
                'f': ('I am ready to face temporary unpopularity if it leads to worthwhile results in the end', 'SH'),
                'g': ('I can usually sense what is realistic and likely to work', 'ME'),
                'h': ('I can offer a reasoned case for alternative courses of action without introducing bias or prejudice', 'ME')
            }
        },
        {
            'question': 'If I have a possible shortcoming in teamwork, it could be that:',
            'options': {
                'a': ('I am not at ease unless meetings are well structured and controlled and generally well conducted', 'CO'),
                'b': ('I am inclined to be too generous towards others who have a valid viewpoint that has not been given a proper airing', 'TW'),
                'c': ('I have a tendency to talk too much once the group gets on to new ideas', 'PL'),
                'd': ('My objective outlook makes it difficult for me to join in readily and enthusiastically with colleagues', 'ME'),
                'e': ('I am sometimes seen as forceful and authoritarian if there is a need to get something done', 'SH'),
                'f': ('I find it difficult to lead from the front, perhaps because I am over-responsive to group atmosphere', 'TW'),
                'g': ('I am apt to get caught up in ideas that occur to me and so lose track of what is happening', 'PL'),
                'h': ('My colleagues tend to see me as worrying unnecessarily over detail and the possibility that things may go wrong', 'CF')
            }
        },
        {
            'question': 'When involved in a project with other people:',
            'options': {
                'a': ('I have an aptitude for influencing people without pressurizing them', 'CO'),
                'b': ('My general vigilance prevents careless mistakes and omissions being made', 'CF'),
                'c': ('I am ready to press for action to make sure that the meeting does not waste time or lose sight of the main objective', 'SH'),
                'd': ('I can be counted on to contribute something original', 'PL'),
                'e': ('I am always ready to back a good suggestion in the common interest', 'TW'),
                'f': ('I am keen to look for the latest in new ideas and developments', 'RI'),
                'g': ('I believe my capacity for cool judgement is appreciated by others', 'ME'),
                'h': ('I can be relied upon to see that all essential work is organized', 'IMP')
            }
        }
    ]
    
    @classmethod
    def calculate_scores(cls, answers: Dict[int, Dict[str, int]]) -> Dict[str, int]:
        """Calculate Belbin role scores based on user answers."""
        scores = {role: 0 for role in cls.ROLES.keys()}
        
        for question_idx, question_answers in answers.items():
            question = cls.QUESTIONS[question_idx]
            for option, points in question_answers.items():
                if option in question['options']:
                    role = question['options'][option][1]
                    scores[role] += points
        
        return scores
    
    @classmethod
    def get_dominant_roles(cls, scores: Dict[str, int], top_n: int = 3) -> List[Tuple[str, int]]:
        """Get the top N dominant roles."""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_n]


class DatabaseManager:
    """Handles database operations for storing test results."""
    
    def __init__(self, db_path: str = 'data/results.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    pl_score INTEGER DEFAULT 0,
                    ri_score INTEGER DEFAULT 0,
                    co_score INTEGER DEFAULT 0,
                    sh_score INTEGER DEFAULT 0,
                    me_score INTEGER DEFAULT 0,
                    tw_score INTEGER DEFAULT 0,
                    imp_score INTEGER DEFAULT 0,
                    cf_score INTEGER DEFAULT 0,
                    sp_score INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
    
    def save_results(self, username: str, scores: Dict[str, int]) -> int:
        """Save test results to database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO test_results 
                (username, pl_score, ri_score, co_score, sh_score, me_score, 
                 tw_score, imp_score, cf_score, sp_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                username,
                scores.get('PL', 0),
                scores.get('RI', 0),
                scores.get('CO', 0),
                scores.get('SH', 0),
                scores.get('ME', 0),
                scores.get('TW', 0),
                scores.get('IMP', 0),
                scores.get('CF', 0),
                scores.get('SP', 0)
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_results(self, username: str) -> List[Dict]:
        """Get all results for a specific user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM test_results WHERE username = ? 
                ORDER BY timestamp DESC
            ''', (username,))
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_all_results(self) -> List[Dict]:
        """Get all test results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM test_results ORDER BY timestamp DESC')
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]