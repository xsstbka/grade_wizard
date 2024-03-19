
import csv

class GradeReport:
    def __init__(self):
        self.report_data = []

    def generate(self, assignments):
        for assignment in assignments:
            # Extract the number before the first '_' in file_name
            file_number = assignment.file_name.split('_', 1)[0]
            self.report_data.append({
                'file_number': file_number,  # Use the extracted number
                'initial_grade': assignment.initial_grade,
                'feedback': assignment.initial_feedback,
            })

    def export(self, file_path='grade_report.csv'):
        with open(file_path, 'w', newline='') as file:
            # Update fieldnames to match the new data structure
            fieldnames = ['file_number', 'initial_grade', 'feedback']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in self.report_data:
                writer.writerow(data)


