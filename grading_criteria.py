#import json
#
#class GradingCriteria:
#    def __init__(self, criteria):
#        self.criteria = criteria
#
#    @staticmethod
#    def from_json(file_path):
#        with open(file_path, 'r') as file:
#            criteria = json.load(file)
#        return GradingCriteria(criteria)

class GradingCriteria:
    def __init__(self, criteria):
        self.criteria = criteria

    @staticmethod
    def from_text(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            criteria_text = file.read()
        return GradingCriteria(criteria_text)
