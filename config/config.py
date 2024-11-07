import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z .env
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Opcjonalnie: Rzucaj wyjątkiem, jeśli klucz nie jest ustawiony
if not all([LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI, LINKEDIN_ACCESS_TOKEN, OPENAI_API_KEY]):
    raise ValueError("Brakuje danych uwierzytelniających LinkedIn i OpenAI. Sprawdź plik .env.")