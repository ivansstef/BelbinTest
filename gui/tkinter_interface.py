"""
Tkinter GUI interface for Belbin Test application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from typing import Dict, Callable, Optional
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.data_processing import BelbinTest, DatabaseManager


class BelbinTestGUI:
    """Main GUI class for the Belbin Test application."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Belbin Team Roles Test")
        self.root.geometry("800x600")
        
        # Initialize components
        self.belbin_test = BelbinTest()
        self.db_manager = DatabaseManager()
        
        # Test state
        self.username = ""
        self.current_question = 0
        self.answers = {}
        self.test_completed = False
        
        # Create main interface
        self.setup_styles()
        self.create_welcome_screen()
    
    def setup_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Question.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Option.TLabel', font=('Arial', 10))
        style.configure('Big.TButton', font=('Arial', 12))
    
    def clear_frame(self):
        """Clear all widgets from the main frame."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_welcome_screen(self):
        """Create the welcome screen for username input."""
        self.clear_frame()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Belbin Team Roles Test", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        desc_text = ("Welcome to the Belbin Team Roles Test!\n\n"
                    "This test will help you identify your preferred team roles.\n"
                    "You'll be presented with several scenarios and asked to\n"
                    "distribute 10 points among different response options.\n\n"
                    "Please enter your name to begin:")
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username input
        ttk.Label(main_frame, text="Your Name:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.username_entry = ttk.Entry(main_frame, font=('Arial', 12), width=30)
        self.username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.username_entry.bind('<Return>', lambda e: self.start_test())
        
        # Start button
        start_button = ttk.Button(main_frame, text="Start Test", 
                                 command=self.start_test, style='Big.TButton')
        start_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Focus on entry
        self.username_entry.focus()
    
    def start_test(self):
        """Start the test after validating username."""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter your name to continue.")
            return
        
        self.username = username
        self.current_question = 0
        self.answers = {}
        self.create_question_screen()
    
    def create_question_screen(self):
        """Create the question screen."""
        self.clear_frame()
        
        if self.current_question >= len(self.belbin_test.QUESTIONS):
            self.process_results()
            return
        
        question_data = self.belbin_test.QUESTIONS[self.current_question]
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Progress info
        progress_text = f"Question {self.current_question + 1} of {len(self.belbin_test.QUESTIONS)}"
        progress_label = ttk.Label(main_frame, text=progress_text, font=('Arial', 10))
        progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Question text
        question_label = ttk.Label(main_frame, text=question_data['question'], 
                                  style='Question.TLabel', wraplength=700)
        question_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Instructions
        instructions = ("Distribute 10 points among the options below.\n"
                       "Give more points to options that best describe you.")
        instr_label = ttk.Label(main_frame, text=instructions, font=('Arial', 10, 'italic'))
        instr_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 15))
        
        # Options frame
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        options_frame.columnconfigure(1, weight=1)
        
        # Store spinboxes for validation
        self.option_spinboxes = {}
        
        # Create options
        for i, (key, (text, _)) in enumerate(question_data['options'].items()):
            # Option letter
            ttk.Label(options_frame, text=f"{key})", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=(0, 10), pady=2
            )
            
            # Option text
            ttk.Label(options_frame, text=text, style='Option.TLabel', 
                     wraplength=500).grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
            
            # Points spinbox
            spinbox = tk.Spinbox(options_frame, from_=0, to=10, width=5, 
                               font=('Arial', 10), validate='key',
                               validatecommand=(self.root.register(self.validate_points), '%P'))
            spinbox.grid(row=i, column=2, padx=(10, 0), pady=2)
            spinbox.delete(0, tk.END)
            spinbox.insert(0, '0')
            self.option_spinboxes[key] = spinbox
        
        # Points counter
        self.points_label = ttk.Label(main_frame, text="Points used: 0/10", 
                                     font=('Arial', 10, 'bold'))
        self.points_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        
        # Update points display
        for spinbox in self.option_spinboxes.values():
            spinbox.config(command=self.update_points_display)
            spinbox.bind('<KeyRelease>', lambda e: self.update_points_display())
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=20)
        
        if self.current_question > 0:
            ttk.Button(nav_frame, text="← Previous", command=self.previous_question).pack(side=tk.LEFT)
        
        ttk.Button(nav_frame, text="Next →" if self.current_question < len(self.belbin_test.QUESTIONS) - 1 else "Finish Test", 
                  command=self.next_question).pack(side=tk.RIGHT)
        
        self.update_points_display()
    
    def validate_points(self, value):
        """Validate that points are numeric and within range."""
        if value == "":
            return True
        try:
            points = int(value)
            return 0 <= points <= 10
        except ValueError:
            return False
    
    def update_points_display(self):
        """Update the points counter display."""
        total_points = 0
        for spinbox in self.option_spinboxes.values():
            try:
                points = int(spinbox.get() or '0')
                total_points += points
            except ValueError:
                continue
        
        self.points_label.config(text=f"Points used: {total_points}/10")
        
        # Change color based on total
        if total_points == 10:
            self.points_label.config(foreground='green')
        elif total_points > 10:
            self.points_label.config(foreground='red')
        else:
            self.points_label.config(foreground='black')
    
    def next_question(self):
        """Move to the next question or finish the test."""
        # Validate points total
        total_points = sum(int(spinbox.get() or '0') for spinbox in self.option_spinboxes.values())
        if total_points != 10:
            messagebox.showerror("Error", f"You must distribute exactly 10 points. Current total: {total_points}")
            return
        
        # Save answers
        question_answers = {}
        for key, spinbox in self.option_spinboxes.items():
            question_answers[key] = int(spinbox.get() or '0')
        
        self.answers[self.current_question] = question_answers
        
        # Move to next question
        self.current_question += 1
        self.create_question_screen()
    
    def previous_question(self):
        """Move to the previous question."""
        if self.current_question > 0:
            self.current_question -= 1
            self.create_question_screen()
            
            # Restore previous answers if they exist
            if self.current_question in self.answers:
                prev_answers = self.answers[self.current_question]
                for key, points in prev_answers.items():
                    if key in self.option_spinboxes:
                        spinbox = self.option_spinboxes[key]
                        spinbox.delete(0, tk.END)
                        spinbox.insert(0, str(points))
                self.update_points_display()
    
    def process_results(self):
        """Process test results and show results screen."""
        # Calculate scores
        scores = self.belbin_test.calculate_scores(self.answers)
        
        # Save to database
        try:
            self.db_manager.save_results(self.username, scores)
        except Exception as e:
            print(f"Error saving results: {e}")
        
        # Show results screen
        self.show_results(scores)
    
    def show_results(self, scores: Dict[str, int]):
        """Display the test results with visualization."""
        self.clear_frame()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_text = f"Test Results for {self.username}"
        title_label = ttk.Label(main_frame, text=title_text, style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results tab
        results_frame = ttk.Frame(notebook, padding="10")
        notebook.add(results_frame, text="Detailed Results")
        
        # Chart tab
        chart_frame = ttk.Frame(notebook, padding="10")
        notebook.add(chart_frame, text="Visualization")
        
        # Populate results tab
        self.create_results_tab(results_frame, scores)
        
        # Populate chart tab
        self.create_chart_tab(chart_frame, scores)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=20)
        
        ttk.Button(button_frame, text="Take Test Again", 
                  command=self.create_welcome_screen).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT)
    
    def create_results_tab(self, parent: ttk.Frame, scores: Dict[str, int]):
        """Create the detailed results tab."""
        # Get dominant roles
        dominant_roles = self.belbin_test.get_dominant_roles(scores)
        
        # Dominant roles section
        dom_label = ttk.Label(parent, text="Your Top 3 Team Roles:", style='Question.TLabel')
        dom_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        for i, (role, score) in enumerate(dominant_roles):
            role_name = self.belbin_test.ROLES[role]
            role_text = f"{i+1}. {role_name}: {score} points"
            ttk.Label(parent, text=role_text, font=('Arial', 11)).grid(
                row=i+1, column=0, sticky=tk.W, padx=(20, 0), pady=2
            )
        
        # All scores section
        all_scores_label = ttk.Label(parent, text="All Role Scores:", style='Question.TLabel')
        all_scores_label.grid(row=5, column=0, sticky=tk.W, pady=(20, 10))
        
        # Create treeview for all scores
        columns = ('Role', 'Score')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=9)
        tree.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configure columns
        tree.heading('Role', text='Team Role')
        tree.heading('Score', text='Score')
        tree.column('Role', width=300)
        tree.column('Score', width=100)
        
        # Populate treeview
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for role, score in sorted_scores:
            role_name = self.belbin_test.ROLES[role]
            tree.insert('', tk.END, values=(role_name, score))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=6, column=1, sticky=(tk.N, tk.S))
        tree.configure(yscroll=scrollbar.set)
        
        parent.columnconfigure(0, weight=1)
    
    def create_chart_tab(self, parent: ttk.Frame, scores: Dict[str, int]):
        """Create the visualization tab with pie chart."""
        # Filter out zero scores for cleaner chart
        filtered_scores = {role: score for role, score in scores.items() if score > 0}
        
        if not filtered_scores:
            ttk.Label(parent, text="No scores to display", style='Question.TLabel').pack(expand=True)
            return
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Prepare data
        labels = [self.belbin_test.ROLES[role] for role in filtered_scores.keys()]
        sizes = list(filtered_scores.values())
        colors = plt.cm.Set3(range(len(labels)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90)
        
        # Customize text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        for text in texts:
            text.set_fontsize(9)
        
        ax.set_title(f'Belbin Team Role Profile - {self.username}', fontsize=14, fontweight='bold')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X)
        
        # Save button
        ttk.Button(toolbar_frame, text="Save Chart", 
                  command=lambda: self.save_chart(fig)).pack(side=tk.LEFT, padx=5)
    
    def save_chart(self, fig):
        """Save the chart as an image file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Chart saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save chart: {e}")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = BelbinTestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()