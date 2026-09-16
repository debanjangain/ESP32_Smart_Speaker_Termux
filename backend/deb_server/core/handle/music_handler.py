import json

from plugins.music_search import MusicSearch
from plugins.playlist_manager import PlaylistManager
from plugins.youtube_music import YouTubeMusic


music_search = MusicSearch()
playlist = PlaylistManager()
youtube = YouTubeMusic()


async def process_music(websocket, message):

    try:
        print(f"[MUSIC] Received: {message}")

        parts = message.split(":")

        if len(parts) < 2:
            await websocket.send("MUSIC:ERROR:Invalid format")
            return

        action = parts[1].upper()

        if action == "SEARCH":

            query = ":".join(parts[2:])

            results = music_search.search_all(
                query,
                limit=3
            )

            await websocket.send(
                json.dumps(results)
            )

        elif action == "PLAYLIST":

            if len(parts) < 3:
                await websocket.send(
                    "MUSIC:ERROR:Missing playlist command"
                )
                return

            sub_action = parts[2].upper()

            if sub_action == "ADD":

                source = parts[3]
                title = parts[4]
                url = ":".join(parts[5:])

                result = playlist.add_item(
                    source,
                    title,
                    url
                )

                await websocket.send(
                    json.dumps(result)
                )

            elif sub_action == "LIST":

                await websocket.send(
                    json.dumps(
                        playlist.list_items()
                    )
                )

            elif sub_action == "CLEAR":

                await websocket.send(
                    json.dumps(
                        playlist.clear()
                    )
                )

            else:

                await websocket.send(
                    "MUSIC:ERROR:Invalid playlist command"
                )

        elif action == "YOUTUBE":

            query = ":".join(parts[2:])

            result = youtube.play(query)

            await websocket.send(
                json.dumps(result)
            )

        else:

            await websocket.send(
                "MUSIC:ERROR:Unknown action"
            )

    except Exception as e:

        print(f"[MUSIC] Error: {e}")

        await websocket.send(
            f"MUSIC:ERROR:{e}"
        )
        
