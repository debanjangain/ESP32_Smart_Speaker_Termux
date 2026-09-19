class PlaylistManager:

    def __init__(self):

        self.playlist = []

    def add_item(self, source, title, url):

        self.playlist.append(
            {
                "source": source,
                "title": title,
                "url": url
            }
        )

        return {
            "status": "ok",
            "message": f"Added {title} from {source}"
        }

    def remove_item(self, index):

        try:

            removed = self.playlist.pop(index)

            return {
                "status": "ok",
                "message": f"Removed {removed['title']}"
            }

        except (IndexError, TypeError):

            return {
                "status": "error",
                "message": "Invalid index"
            }

    def list_items(self):

        return {
            "status": "ok",
            "playlist": self.playlist
        }

    def clear(self):

        self.playlist.clear()

        return {
            "status": "ok",
            "message": "Playlist cleared"
        }
        
