from providers.llm.llm_provider import LLMProvider

llm = LLMProvider()


async def process_llm(websocket, message):
    """
    Expected format:
    LLM:<query>
    """

    try:
        print(f"[LLM] Received: {message}")

        query = message.replace("LLM:", "", 1).strip()

        if not query:
            await websocket.send("LLM:ERROR: Empty query")
            return

        result = llm.ask(query)

        if result["status"] == "ok":
            await websocket.send(
                f"LLM:{result['provider']}:{result['reply']}"
            )
        else:
            await websocket.send(
                f"LLM:ERROR:{result['message']}"
            )

    except Exception as e:
        error_msg = f"LLM:ERROR:{e}"

        print(error_msg)

        await websocket.send(error_msg)
        
