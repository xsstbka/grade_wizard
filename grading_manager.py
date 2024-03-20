from grading_criteria import GradingCriteria
from assignment import Assignment
from gpt4_grader import GPT4Grader
from user_interface import UserInterface
from grade_report import GradeReport
import os
import os
from bs4 import BeautifulSoup  # For parsing HTML
from PyPDF2 import PdfReader  # For parsing PDF



class GradingManager:
    def __init__(self):
        self.criteria_path = "replace the fold of the criteria"
        self.assignments_path = "replace the fold of the assignments"
        self.grading_criteria = ['A', 'B', 'C']
        self.assignments = []
        self.grader = GPT4Grader(api_key="replace the API key")
        
        self.ui = UserInterface()
        self.grade_report = GradeReport()

    def load_criteria(self):
        for filename in os.listdir(self.criteria_path):
            file_path = os.path.join(self.criteria_path, filename)
            if filename.endswith('.txt'):
                criteria = GradingCriteria.from_text(file_path)
                self.grading_criteria.append(criteria)


    def load_assignments(self):
        for filename in os.listdir(self.assignments_path):
            file_path = os.path.join(self.assignments_path, filename)
            file_name = os.path.basename(file_path)
            
            if filename.endswith('.pdf'):
                self.assignments.append(Assignment.from_pdf(file_path))
            elif filename.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text = soup.get_text()
                    self.assignments.append(Assignment.from_text(text, file_name))
            elif filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.assignments.append(Assignment.from_text(text, file_name))


    def initial_grading(self):
        for assignment in self.assignments:
            initial_grade, feedback = self.grader.grade(assignment, self.grading_criteria)
            assignment.set_initial_grade(initial_grade)
            assignment.initial_feedback = feedback  


    def review_grades(self):
        for assignment in self.assignments:
            self.ui.review_assignment(assignment)
            if self.ui.needs_regrading(assignment):
                grade = self.grader.regrade(assignment, self.grading_criteria)
                assignment.set_final_grade(grade)

    def final_grading(self):
        for assignment in self.assignments:
            if not assignment.is_final_grade_set():
                assignment.set_final_grade(assignment.initial_grade)

    def export_grade_reports(self):
        self.grade_report.generate(self.assignments)
        self.grade_report.export()
