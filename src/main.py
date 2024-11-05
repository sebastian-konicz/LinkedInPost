from config.config import LINKEDIN_ACCESS_TOKEN
from src.linkedin_client import LinkedInClient
from config.secrets import get_access_token

def main():
    access_token = LINKEDIN_ACCESS_TOKEN
    if not access_token:
        auth_code = input("Podaj kod autoryzacyjny LinkedIn: ")
        access_token = get_access_token(auth_code)
        print(f"Twój ACCESS_TOKEN: {access_token}")
        # W realnej aplikacji zapisz token do pliku .env lub bazy danych.

    client = LinkedInClient(access_token)
    message = "Nowy post na LinkedIn z LinkedIn API i Python!"
    client.create_post(message)

if __name__ == "__main__":
    main()