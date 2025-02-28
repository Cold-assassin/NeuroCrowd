import google.generativeai as genai
from config.settings import Config
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

genai.configure(api_key=Config.GEMINI_API_KEY)

class PanicAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze(self, text: str) -> int:
        try:
            response = self.model.generate_content(
                f"Rate panic level 0-100 for: '{text}'. Reply only with number."
            )
            return int(response.text.strip())
        except:
            return min(100, text.lower().count('crowd') * 20)