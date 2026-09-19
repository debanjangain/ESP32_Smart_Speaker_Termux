import subprocess

from config_loader import Config


class YouTubeMusic:

    def __init__(self):

        self.tool = Config.get(
            "apis.youtube",
            default="yt-dlp"
        )

        self.runtime = Config.get(
            "apis.youtube_runtime",
            default="quickjs"
        )

    def stream(self, query):

        try:

            cmd = [
                self.tool,
                "--js-runtime",
                self.runtime,
                "-f",
                "bestaudio",
                "--get-url",
                f"ytsearch:{query}"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": result.stderr.strip()
                }

            url = result.stdout.strip()

            if not url:
                return {
                    "status": "error",
                    "message": "No stream URL found"
                }

            return {
                "status": "ok",
                "title": query,
                "stream_url": url
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

    def fallback_download(self, query):

        try:

            output_template = "last_song.%(ext)s"

            cmd = [
                self.tool,
                "--js-runtime",
                self.runtime,
                "-f",
                "bestaudio",
                "-o",
                output_template,
                f"ytsearch:{query}"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": result.stderr.strip()
                }

            return {
                "status": "ok",
                "file_template": output_template
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

    def play(self, query):

        stream_result = self.stream(query)

        if stream_result["status"] == "ok":
            return stream_result

        return self.fallback_download(query)
        
