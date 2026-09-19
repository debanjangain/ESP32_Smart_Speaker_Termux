import requests

from config_loader import Config


class PodcastPlugin:

    def __init__(self):

        self.base_url = Config.get(
            "apis.podcast_url",
            default="https://api.podcastindex.org"
        )

        self.api_key = Config.get(
            "apis.podcast_key",
            default=None
        )

        self.api_secret = Config.get(
            "apis.podcast_secret",
            default=None
        )

    def search_podcast(self, query, limit=5):

        try:

            headers = {}

            if self.api_key and self.api_secret:

                headers = {
                    "X-API-Key": self.api_key,
                    "X-API-Secret": self.api_secret
                }

            response = requests.get(
                f"{self.base_url}/api/1.0/search/byterm",
                params={"q": query},
                headers=headers,
                timeout=20
            )

            if response.status_code != 200:

                return {
                    "status": "error",
                    "message": response.text
                }

            data = response.json()

            results = []

            for feed in data.get("feeds", [])[:limit]:

                results.append(
                    {
                        "title":
                            feed.get("title"),

                        "url":
                            feed.get("url"),

                        "description":
                            feed.get(
                                "description",
                                ""
                            )[:300]
                    }
                )

            return {
                "status": "ok",
                "podcasts": results
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
        }
            
