import requests

from config_loader import Config


class WeatherPlugin:

    def __init__(self):

        self.api_key = Config.get(
            "apis.openweather_key"
        )

        self.base_url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

    def get_weather(self, city):

        try:

            if (
                not self.api_key or
                str(self.api_key).startswith("YOUR_")
            ):
                return {
                    "status": "error",
                    "message":
                        "Weather API key not configured"
                }

            response = requests.get(
                self.base_url,
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=20
            )

            if response.status_code != 200:

                data = response.json()

                return {
                    "status": "error",
                    "message":
                        data.get(
                            "message",
                            "Unknown error"
                        )
                }

            data = response.json()

            return {
                "status": "ok",
                "city": city,
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"]
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }


if __name__ == "__main__":

    wp = WeatherPlugin()

    print(
        wp.get_weather("Delhi")
    )

    print(
        wp.get_weather("Kolkata")
    )

    print(
        wp.get_weather("Kanpur")
    )
    
