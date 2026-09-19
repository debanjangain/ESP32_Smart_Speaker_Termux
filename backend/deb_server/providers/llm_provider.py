import requests

from config_loader import Config


class LLMProvider:

    def __init__(self):

        # Gemini
        self.gemini_provider = Config.get(
            "models.gemini.provider",
            default="Gemini"
        )
        self.gemini_key = Config.get(
            "models.gemini.api_key",
            default=None
        )

        # ChatGPT
        self.chatgpt_provider = Config.get(
            "models.chatgpt.provider",
            default="ChatGPT"
        )
        self.chatgpt_key = Config.get(
            "models.chatgpt.api_key",
            default=None
        )

        # Qwen
        self.qwen_provider = Config.get(
            "models.qwen.provider",
            default="Qwen"
        )
        self.qwen_key = Config.get(
            "models.qwen.api_key",
            default=None
        )

        self.base_urls = {
            "Gemini":
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",

            "ChatGPT":
                "https://api.openai.com/v1/chat/completions",

            "Qwen":
                "https://api.qwen.ai/v1/chat/completions"
        }

    def query_llm(self, text, provider, key):
        """
        Query a specific LLM provider.
        """

        if not key or str(key).startswith("YOUR_"):
            return {
                "status": "error",
                "provider": provider,
                "message": "API key not configured"
            }

        try:

            url = self.base_urls.get(provider)

            if not url:
                return {
                    "status": "error",
                    "provider": provider,
                    "message": "Unknown provider"
                }

            headers = {
                "Content-Type": "application/json"
            }

            payload = {}

            if provider == "Gemini":

                url = f"{url}?key={key}"

                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": text
                                }
                            ]
                        }
                    ]
                }

            elif provider == "ChatGPT":

                headers["Authorization"] = (
                    f"Bearer {key}"
                )

                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": text
                        }
                    ]
                }

            elif provider == "Qwen":

                headers["Authorization"] = (
                    f"Bearer {key}"
                )

                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": text
                        }
                    ]
                }

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:

                return {
                    "status": "error",
                    "provider": provider,
                    "message": response.text
                }

            data = response.json()

            if provider == "Gemini":

                reply = (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )

            elif provider == "ChatGPT":

                reply = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )

            else:   # Qwen

                reply = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )

            return {
                "status": "ok",
                "provider": provider,
                "reply": reply
            }

        except Exception as e:

            return {
                "status": "error",
                "provider": provider,
                "message": str(e)
            }

    def ask(self, text):
        """
        Fallback chain:
        Gemini -> ChatGPT -> Qwen
        """

        result = self.query_llm(
            text,
            self.gemini_provider,
            self.gemini_key
        )

        if result["status"] == "ok":
            return result

        result = self.query_llm(
            text,
            self.chatgpt_provider,
            self.chatgpt_key
        )

        if result["status"] == "ok":
            return result

        return self.query_llm(
            text,
            self.qwen_provider,
            self.qwen_key
        )


if __name__ == "__main__":

    llm = LLMProvider()

    response = llm.ask(
        "Explain ESP32 smart speaker pipeline."
    )

    print(response)
    
