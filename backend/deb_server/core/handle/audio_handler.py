async def process_audio(websocket, message):
    """
    Handle audio messages from ESP32.
    Expected format:
    AUDIO:<data>
    """

    try:
        print(f"[AUDIO] Received: {message[:100]}")

        await websocket.send("AUDIO:OK")

    except Exception as e:
        error_msg = f"[AUDIO] Error: {e}"

        print(error_msg)

        await websocket.send(error_msg)
        
