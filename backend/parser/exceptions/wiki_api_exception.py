import json


class WikiApiException(BaseException):
    def __init__(self, description, error_data):
        self.message = description + "\n" + json.dumps(error_data, indent=4)