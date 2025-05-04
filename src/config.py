import os
from dotenv import load_dotenv

class Config:
    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)

        self.API_KEY = os.getenv("API_KEY")
        self.MODEL_NAME = 'gemini-2.0-flash'

    def __str__(self):
        return f"Config(API_KEY={self.API_KEY}, DEBUG={self.DEBUG}, DB_URL={self.DB_URL})"
