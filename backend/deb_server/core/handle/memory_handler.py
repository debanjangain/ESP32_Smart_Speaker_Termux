from database.sqlite_db import (
    remember_fact,
    recall_fact,
    forget_fact
)


async def process_memory(websocket, message):

    try:
        parts = message.split(":")

        if len(parts) < 3:
            await websocket.send("MEM:ERROR:Invalid format")
            return

        action = parts[1].upper()
        key = parts[2].strip()

        if not key:
            await websocket.send("MEM:ERROR:Invalid key")
            return

        if action == "REMEMBER":

            value = ":".join(parts[3:])

            remember_fact(key, value)

            await websocket.send("MEM:OK")

        elif action == "RECALL":

            value = recall_fact(key)

            if value is not None:
                await websocket.send(
                    f"MEM:VALUE:{key}:{value}"
                )
            else:
                await websocket.send(
                    "MEM:ERROR:Not found"
                )

        elif action == "FORGET":

            forget_fact(key)

            await websocket.send("MEM:OK")

        else:
            await websocket.send(
                "MEM:ERROR:Unknown action"
            )

    except Exception as e:

        await websocket.send(
            f"MEM:ERROR:{e}"
        )
        
