# from config.config import LINKEDIN_ACCESS_TOKEN
from src.linkedin_client import LinkedInClient
from config.secrets import get_access_token

def main():
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    access_token = LINKEDIN_ACCESS_TOKEN

    client = LinkedInClient(access_token)
    message = "Nowy post na LinkedIn wrzucony przy udziale GitHub Actions!"
    client.create_post(message)

if __name__ == "__main__":
    main()