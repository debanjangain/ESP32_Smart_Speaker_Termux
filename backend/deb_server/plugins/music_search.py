import json
import subprocess
from urllib.parse import quote_plus

from config_loader import Config


class MusicSearch:

    def __init__(self):

        self.youtube_enabled = (
            Config.get("apis.youtube", "disabled")
            == "yt-dlp"
        )

        self.jiosaavn_enabled = (
            Config.get("apis.jiosaavn", "disabled")
            == "enabled"
        )

        self.gaana_enabled = (
            Config.get("apis.gaana", "disabled")
            == "enabled"
        )

    def search_youtube(self, query, limit=5):

        if not self.youtube_enabled:
            return []

        cmd = [
            "yt-dlp",
            f"ytsearch{limit}:{query}",
            "--dump-json"
        ]

        results = []

        try:

            output = subprocess.check_output(
                cmd,
                text=True
            )

            for line in output.strip().splitlines():

                data = json.loads(line)

                results.append(
                    {
                        "title":
                            data.get("title"),

                        "url":
                            data.get("webpage_url")
                    }
                )

            return results

        except Exception as e:

            return [
                {
                    "error": str(e)
                }
            ]

    def search_jiosaavn(self, query, limit=5):

        if not self.jiosaavn_enabled:
            return []

        return [
            {
                "status": "not_implemented",
                "provider": "jiosaavn"
            }
        ]

    def search_gaana(self, query, limit=5):

        if not self.gaana_enabled:
            return []

        return [
            {
                "status": "not_implemented",
                "provider": "gaana"
            }
        ]

    def search_all(self, query, limit=5):

        results = {}

        if self.youtube_enabled:
            results["youtube"] = (
                self.search_youtube(query, limit)
            )

        if self.jiosaavn_enabled:
            results["jiosaavn"] = (
                self.search_jiosaavn(query, limit)
            )

        if self.gaana_enabled:
            results["gaana"] = (
                self.search_gaana(query, limit)
            )

        return {
            "status": "ok",
            "results": results
            }
        
