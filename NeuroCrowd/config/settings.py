import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GRID_WIDTH = 50
    GRID_HEIGHT = 50
    INITIAL_AGENTS = 2000  # Number of agents