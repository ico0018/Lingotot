import openai

class UserSession:
    def __init__(self):
        openai.api_key = "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"

    def __enter__(self):
        return openai

    def __exit__(self, exc_type, exc_value, traceback):
        openai.api_key = None  # Replace with actual method to close the instance
