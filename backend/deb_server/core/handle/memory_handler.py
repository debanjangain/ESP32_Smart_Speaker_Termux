from database.sqlite_db import remember_fact, recall_fact, forget_fact

async def process_memory(websocket, message):
    """
    Handle memory commands.
    Expected format:
      MEM:REMEMBER:<key>:<value>
      MEM:RECALL:<key>
      MEM:FORGET:<key>
    """
    try:
        parts = message.split(":")
        if len(parts) < 3:
            await websocket.send("[MEM] Invalid format")
            return

        action = parts[1].upper()
        key = parts[2]

        if action == "REMEMBER":
            value = parts[3] if len(parts) > 3 else ""
            remember_fact(key, value)
            await websocket.send(f"[MEM] Remembered {key} = {value}")

        elif action == "RECALL":
            value = recall_fact(key)
            if value:
                await websocket.send(f"[MEM] {key} = {value}")
            else:
                await websocket.send(f"[MEM] No memory found for {key}")

        elif action == "FORGET":
            forget_fact(key)
            await websocket.send(f"[MEM] Forgotten {key}")

        else:
            await websocket.send("[MEM] Unknown action")

    except Exception as e:
        await websocket.send(f"[MEM] Error: {str(e)}")
