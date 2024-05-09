import base64
import requests

class TutorClient:
    access_token = ""
    def __init__(self, *args, **kwargs):
        self.access_token = self.get_token()
        super(TutorClient, self).__init__(*args, **kwargs)
    



    def get_token(self):
        client_id = "oJ0HFkdCk25FUShF9R5L0FvxTyIy4rlIF1zwLSmN"
        client_secret = "XpvUrK1lYq24S5AOP6Mx5tmfBqEoDl0rQkokBSD9Hi7PXMcSakrXANucLnq4QgvzHskwtgrHGuYnx07xVfTZeLLemg988i3SVCUgS7GdwpJvYoksJgkQXbFbXjUYAgUs"

        credential = f"{client_id}:{client_secret}"
        encoded_credential = base64.b64encode(credential.encode("utf-8")).decode("utf-8")

        headers = {"Authorization": f"Basic {encoded_credential}", "Cache-Control": "no-cache"}
        data = {"grant_type": "client_credentials", "token_type": "jwt"}

        token_request = requests.post(
            "http://local.edly.io/oauth2/access_token", headers=headers, data=data
        )
        return token_request.json()["access_token"]


    def get_courses(self):
        enrollment_request = requests.get(
        "http://local.edly.io/api/courses/v1/courses/",
        headers={"Authorization": f"JWT {self.access_token}"},
    )