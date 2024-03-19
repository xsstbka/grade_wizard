from grading_manager import GradingManager

def main():
    grading_manager = GradingManager()
    grading_manager.load_criteria()
    grading_manager.load_assignments()
    grading_manager.initial_grading()
    grading_manager.review_grades()
    grading_manager.final_grading()
    grading_manager.export_grade_reports()

if __name__ == "__main__":
    main()
