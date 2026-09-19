import feedparser

from config_loader import Config


class NewsPlugin:

    def __init__(self):

        self.feeds = Config.get(
            "apis.news_feeds",
            default=[]
        )

    def get_headlines(self, limit=10):

        if not self.feeds:
            return {
                "status": "error",
                "message": "No news feeds configured"
            }

        results = []

        for feed_url in self.feeds:

            try:

                feed = feedparser.parse(feed_url)

                headlines = []

                for entry in feed.entries[:limit]:

                    headlines.append({
                        "title":
                            entry.get(
                                "title",
                                "No title"
                            ),

                        "link":
                            entry.get(
                                "link",
                                ""
                            )
                    })

                results.append({
                    "feed": feed_url,
                    "headlines": headlines
                })

            except Exception as e:

                results.append({
                    "feed": feed_url,
                    "error": str(e)
                })

        return {
            "status": "ok",
            "feeds": results
        }


if __name__ == "__main__":

    news = NewsPlugin()

    data = news.get_headlines(limit=10)

    for feed in data.get("feeds", []):

        print(f"\nFeed: {feed['feed']}")

        for h in feed.get("headlines", []):

            print(" -", h["title"])
            
