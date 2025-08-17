#!/usr/bin/env python3
"""
Demo script to showcase the Belbin Test application functionality.
This script demonstrates the core features without requiring GUI interaction.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processing import BelbinTest, DatabaseManager


def demo_test_logic():
    """Demonstrate the test logic and scoring."""
    print("=" * 60)
    print("BELBIN TEST DEMO - Core Functionality")
    print("=" * 60)
    
    # Initialize test
    belbin_test = BelbinTest()
    
    print(f"\n📋 Available Team Roles ({len(belbin_test.ROLES)}):")
    for code, name in belbin_test.ROLES.items():
        print(f"  {code}: {name}")
    
    print(f"\n❓ Test Questions ({len(belbin_test.QUESTIONS)}):")
    for i, question in enumerate(belbin_test.QUESTIONS):
        print(f"\n{i+1}. {question['question']}")
        print(f"   Options: {len(question['options'])}")
    
    # Simulate test answers
    sample_answers = {
        0: {'a': 2, 'b': 1, 'c': 5, 'd': 1, 'e': 0, 'f': 0, 'g': 1, 'h': 0},  # Creative focus
        1: {'a': 1, 'b': 3, 'c': 2, 'd': 1, 'e': 0, 'f': 2, 'g': 1, 'h': 0},  # Teamwork focus
        2: {'a': 2, 'b': 1, 'c': 1, 'd': 4, 'e': 1, 'f': 1, 'g': 0, 'h': 0}   # Originality focus
    }
    
    print(f"\n🧮 Sample Test Answers:")
    for q_idx, answers in sample_answers.items():
        total_points = sum(answers.values())
        print(f"  Question {q_idx + 1}: {dict(answers)} (Total: {total_points} points)")
    
    # Calculate scores
    scores = belbin_test.calculate_scores(sample_answers)
    
    print(f"\n📊 Calculated Scores:")
    for role, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        role_name = belbin_test.ROLES[role]
        bar = "█" * (score // 2) if score > 0 else ""
        print(f"  {role}: {score:2d} points {bar} ({role_name})")
    
    # Get dominant roles
    top_roles = belbin_test.get_dominant_roles(scores, 3)
    
    print(f"\n🏆 Top 3 Team Roles:")
    for i, (role, score) in enumerate(top_roles):
        role_name = belbin_test.ROLES[role]
        print(f"  {i+1}. {role_name}: {score} points")


def demo_database():
    """Demonstrate database functionality."""
    print("\n" + "=" * 60)
    print("DATABASE DEMO - Data Persistence")
    print("=" * 60)
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Sample user data
    users_data = [
        ("Alice Johnson", {'PL': 15, 'RI': 12, 'CO': 8, 'SH': 5, 'ME': 3, 'TW': 2, 'IMP': 1, 'CF': 1, 'SP': 0}),
        ("Bob Smith", {'SH': 14, 'CO': 11, 'IMP': 10, 'PL': 6, 'ME': 4, 'RI': 2, 'TW': 0, 'CF': 0, 'SP': 0}),
        ("Carol Davis", {'TW': 16, 'CO': 13, 'ME': 9, 'RI': 7, 'PL': 2, 'SH': 0, 'IMP': 0, 'CF': 0, 'SP': 0})
    ]
    
    print(f"\n💾 Saving {len(users_data)} sample users to database...")
    
    # Save sample data
    for username, scores in users_data:
        result_id = db_manager.save_results(username, scores)
        print(f"  ✓ {username}: Saved with ID {result_id}")
    
    # Retrieve and display results
    print(f"\n📋 Retrieved Results:")
    all_results = db_manager.get_all_results()
    
    for result in all_results:
        username = result['username']
        timestamp = result['timestamp']
        
        # Get top role
        role_scores = {
            'PL': result['pl_score'], 'RI': result['ri_score'], 'CO': result['co_score'],
            'SH': result['sh_score'], 'ME': result['me_score'], 'TW': result['tw_score'],
            'IMP': result['imp_score'], 'CF': result['cf_score'], 'SP': result['sp_score']
        }
        
        top_role = max(role_scores.items(), key=lambda x: x[1])
        top_role_name = BelbinTest.ROLES[top_role[0]]
        
        print(f"  📊 {username} ({timestamp})")
        print(f"     Primary Role: {top_role_name} ({top_role[1]} points)")


def demo_visualization_data():
    """Show sample data that would be used for visualization."""
    print("\n" + "=" * 60)
    print("VISUALIZATION DEMO - Chart Data")
    print("=" * 60)
    
    # Sample user scores for visualization
    sample_user = "Demo User"
    sample_scores = {'PL': 12, 'RI': 8, 'CO': 6, 'SH': 10, 'ME': 4, 'TW': 7, 'IMP': 0, 'CF': 0, 'SP': 0}
    
    print(f"\n🎨 Sample Visualization Data for '{sample_user}':")
    
    # Filter non-zero scores for pie chart
    filtered_scores = {role: score for role, score in sample_scores.items() if score > 0}
    
    total_points = sum(filtered_scores.values())
    print(f"\n📈 Pie Chart Data (Total: {total_points} points):")
    
    for role, score in sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True):
        role_name = BelbinTest.ROLES[role]
        percentage = (score / total_points) * 100
        bar = "█" * int(percentage // 5)
        print(f"  {role_name:<25} {score:2d} points ({percentage:5.1f}%) {bar}")
    
    print(f"\n📊 This data would generate a colorful pie chart showing:")
    print(f"  - Role distribution as percentages")
    print(f"  - Visual representation of team role preferences")
    print(f"  - Interactive chart with save functionality")


def main():
    """Run the complete demo."""
    print("🎯 BELBIN TEAM ROLES TEST - FUNCTIONALITY DEMO")
    print("This demo showcases the core features of the application")
    
    try:
        demo_test_logic()
        demo_database()
        demo_visualization_data()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETE ✓")
        print("=" * 60)
        print("\n🚀 To run the full GUI application:")
        print("   python main.py")
        print("\n🧪 To run tests:")
        print("   python -m unittest discover tests/ -v")
        print("\n📖 For more information:")
        print("   See README.md")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())