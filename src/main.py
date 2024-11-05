import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import LINKEDIN_ACCESS_TOKEN
from src.linkedin_client import LinkedInClient
from config.secrets import get_access_token

def main():
    access_token = LINKEDIN_ACCESS_TOKEN

    client = LinkedInClient(access_token)
    message = "Nowy post na LinkedIn wrzucony przy udziale GitHub Actions!"
    client.create_post(message)

if __name__ == "__main__":
    main()