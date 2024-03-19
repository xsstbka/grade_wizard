from openai import OpenAI
import re
from grading_criteria import GradingCriteria

client = OpenAI(api_key='replace the API key')

class GPT4Grader:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def grade(self, assignment, grading_criteria):
        prompt = self._create_prompt(assignment.content, grading_criteria)

        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
#            temperature=0.3
        )
        response = completion.choices[0].message.content

        # 使用_parse_response方法来处理响应
        initial_grade, feedback = self._parse_response(response)
        return initial_grade, feedback
  
    def regrade(self, assignment, grading_criteria):
        # 调用grade方法并返回其结果
        return self.grade(assignment, grading_criteria)

#    def _create_prompt(self, assignment_content, grading_criteria):
#        # 构建并返回用于评分的提示
#        criteria_text = "\n".join([c for c in grading_criteria])  # 假设grading_criteria是一个字符串列表
#        return f"Rate the following assignment based on criteria:\n{criteria_text}\nThe assignment content is:\n\n{assignment_content}\n\nPlease provide a score out of 100 and any feedback."

#    def _create_prompt(self, assignment_content, grading_criteria):
#        # Convert the grading criteria into a text format if it's not already
#        # This assumes grading_criteria is a list or similar structure that needs to be joined into a single string
#        criteria_text = "\n".join(grading_criteria) if isinstance(grading_criteria, (list, tuple)) else grading_criteria
#
#        prompt = (
#            "Rate the following assignment based on criteria:\n"
#            f"{criteria_text}\n\n"
#            "The assignment content is:\n\n"
#            f"{assignment_content}\n\n"
#            "Please provide a score out of 100 and any feedback."
#        )
#
#        return prompt



    def _create_prompt(self, assignment_content, grading_criteria):
        # Construct criteria text, handling both GradingCriteria objects and strings
        criteria_text_list = []
        for criteria in grading_criteria:
            if isinstance(criteria, GradingCriteria):
                criteria_text_list.append(criteria.criteria)
            elif isinstance(criteria, str):
                criteria_text_list.append(criteria)
            else:
                # Handle other types or raise an error
                raise TypeError("Unexpected type in grading criteria list")
        criteria_text = "\n".join(criteria_text_list)
        
  
        prompt = (
            "Mark the assignments strictly following the rubric in the criteria:\n. It's crucial to differentiate between exceptional, good, average, below average, and poor submissions."
            f"{criteria_text}\n\n"
            "The assignment content is:\n\n"
            f"{assignment_content}\n\n"
            "Calculate the total score accurately"
            "Show the total score separately, strictly following the Format: 'Total Score: [score]/[Total possible points]'."
            "Provide any additional feedback according to the rubric."
        )

        return prompt

    def _parse_response(self, response):
        feedback = response.strip()

        # Define regex patterns for the two specific score formats
        score_patterns = [
            r'Initial Grade:\s*(\d+)',  # "Initial Grade: "
            r'Total Score:\s*(\d+)',  # "Total Score: "
            r'Total Score:\s*\*+:\s*(\d+)',  # "Total Score*****: 100"
        ]

        initial_grade = None
        for pattern in score_patterns:
            score_match = re.search(pattern, response, re.IGNORECASE)
            if score_match:
                initial_grade = score_match.group(1).strip()
                break

        if not initial_grade:
            print("No specific score format found in the response. Manual verification might be necessary.")

        return initial_grade, feedback

