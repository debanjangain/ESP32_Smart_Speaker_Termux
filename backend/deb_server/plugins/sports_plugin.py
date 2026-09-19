import requests

from config_loader import Config


class SportsPlugin:

    def __init__(self):

        self.api_key = Config.get(
            "apis.sports_key"
        )

        self.base_url = (
            "https://api.cricapi.com/v1/currentMatches"
        )

    def get_scores(self, limit=5):

        try:

            if (
                not self.api_key or
                str(self.api_key).startswith("YOUR_")
            ):
                return {
                    "status": "error",
                    "message":
                        "Sports API key not configured"
                }

            response = requests.get(
                self.base_url,
                params={
                    "apikey": self.api_key
                },
                timeout=20
            )

            if response.status_code != 200:

                return {
                    "status": "error",
                    "message": response.text
                }

            data = response.json()

            matches = []

            for match in data.get("data", [])[:limit]:

                matches.append(
                    {
                        "name":
                            match.get("name"),

                        "status":
                            match.get("status"),

                        "score":
                            match.get("score", [])
                    }
                )

            return {
                "status": "ok",
                "matches": matches
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }


if __name__ == "__main__":

    sp = SportsPlugin()

    print(
        sp.get_scores(limit=5)
    )
    
