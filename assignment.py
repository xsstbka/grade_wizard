from PyPDF2 import PdfReader
import os

class Assignment:
    def __init__(self, content, file_name):
        self.content = content
        self.file_name = file_name
        self.initial_grade = None
        self.initial_feedback = None
        self.final_grade = None
        self.final_feedback = None

    @classmethod
    def from_text(cls, text, file_name):
        return cls(text, file_name)

    @staticmethod
    def from_pdf(file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            content = ""
            for page in range(len(reader.pages)):
                content += reader.pages[page].extract_text()
        return Assignment(content, file_name)

    @staticmethod
    def from_txt(file_path):
        file_name = os.path.basename(file_path)  
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return Assignment(content, file_name)

    def set_initial_grade(self, grade):
        self.initial_grade = grade

    def set_final_grade(self, grade):
        self.final_grade = grade

    def is_final_grade_set(self):
        return self.final_grade is not None

