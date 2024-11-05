import requests

class LinkedInClient:
    def __init__(self, access_token):
        self.api_url = "https://api.linkedin.com/v2/"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def get_linkedin_profile_id(self):
        """Pobiera ID użytkownika, które jest potrzebne do publikacji."""
        try:
            response = requests.get(f"{self.api_url}userinfo", headers=self.headers)
            if response.status_code == 200:
                return response.json()["sub"]
                # return response.json()
            else:
                error_info = response.json() if response.content else {}
                raise Exception(
                    f"Błąd podczas pobierania ID profilu LinkedIn: "
                    f"Status Code: {response.status_code}, "
                    f"Response: {error_info.get('message', 'Brak szczegółów błędu')}"
                )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Błąd w żądaniu HTTP: {e}")

    def create_post(self, message):
        # print(message)
        """Tworzy post na LinkedIn."""
        try:
            # https://learn.microsoft.com/en-us/linkedin/compliance/integrations/shares/ugc-post-api?tabs=http
            profile_id = self.get_linkedin_profile_id()
            post_data = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": message
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            response = requests.post(
                f"{self.api_url}ugcPosts",
                headers=self.headers,
                json=post_data
            )
            if response.status_code != 201:
                raise Exception(f"Błąd podczas tworzenia postu: {response.content}")
            print("Post został pomyślnie opublikowany.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")