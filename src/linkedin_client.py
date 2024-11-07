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
            else:
                error_info = response.json() if response.content else {}
                raise Exception(
                    f"Błąd podczas pobierania ID profilu LinkedIn: "
                    f"Status Code: {response.status_code}, "
                    f"Response: {error_info.get('message', 'Brak szczegółów błędu')}"
                )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Błąd w żądaniu HTTP: {e}")

    def upload_image(self, file_path):
        """Przesyła obraz i zwraca identyfikator assetu do wykorzystania w poście."""
        register_url = f"{self.api_url}assets?action=registerUpload"
        upload_request_data = {
            "registerUploadRequest": {
                "owner": f"urn:li:person:{self.get_linkedin_profile_id()}",
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [
                    {
                        "identifier": "urn:li:userGeneratedContent",
                        "relationshipType": "OWNER"
                    }
                ],
                "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
            }
        }

        # Wysyłanie żądania do zarejestrowania przesyłania obrazu
        response = requests.post(register_url, headers=self.headers, json=upload_request_data)
        response_data = response.json()

        # Pobieranie URL przesyłania i identyfikatora assetu
        upload_url = \
        response_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"][
            "uploadUrl"]
        asset = response_data["value"]["asset"]

        # Przesyłanie obrazu na uzyskany URL
        with open(file_path, "rb") as file:
            upload_response = requests.put(upload_url, headers={"Authorization": self.headers["Authorization"]},
                                           data=file)

        if upload_response.status_code == 201:
            print("Obraz został przesłany.")
            return asset
        else:
            raise Exception(f"Błąd podczas przesyłania obrazu: {upload_response.text}")

    def create_post(self, message, image_path=None):
        """Tworzy post na LinkedIn z opcjonalnym załączonym obrazem."""
        try:
            profile_id = self.get_linkedin_profile_id()
            post_data = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": message
                        },
                        "shareMediaCategory": "IMAGE" if image_path else "NONE",
                        "media": []
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Jeśli podano ścieżkę obrazu, dołącz go do posta
            if image_path:
                asset = self.upload_image(image_path)
                post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"].append({
                    "status": "READY",
                    "description": {
                        "text": "Image description here."
                    },
                    "media": asset,
                    "title": {
                        "text": "Sample Image Title"
                    }
                })

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
