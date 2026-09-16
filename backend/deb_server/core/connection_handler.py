from core.handle.audio_handler import process_audio
from core.handle.music_handler import process_music
from core.handle.llm_handler import process_llm
from core.handle.memory_handler import process_memory


async def handle_connection(websocket, path):

    print("[CORE] Client connected")

    try:
        async for message in websocket:

            print(f"[CORE] Received: {message}")

            if message.startswith("AUDIO:"):
                await process_audio(websocket, message)

            elif message.startswith("MUSIC:"):
                await process_music(websocket, message)

            elif message.startswith("LLM:"):
                await process_llm(websocket, message)

            elif message.startswith("MEM:"):
                await process_memory(websocket, message)

            else:
                await websocket.send("[CORE] Unknown request type")

    except Exception as e:
        print(f"[CORE] Error: {e}")

    finally:
        print("[CORE] Client disconnected")
        
