class UserInterface:
    def review_assignment(self, assignment):
        print(f"Initial Grade: {assignment.initial_grade}")
        print(f"Feedback: {assignment.initial_feedback}")
        # Additional UI logic for reviewing the assignment

    def needs_regrading(self, assignment):
        # Logic to determine if an assignment needs regrading based on user input
        return False  # Placeholder for actual user input logic