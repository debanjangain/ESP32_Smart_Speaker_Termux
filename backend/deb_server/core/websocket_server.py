import websockets
from core.connection_handler import handle_connection


async def start_server(host="0.0.0.0", port=8765):

    try:
        server = await websockets.serve(
            handle_connection,
            host,
            port
        )

        print(f"[CORE] WebSocket server running at ws://{host}:{port}")

        await server.wait_closed()

    except Exception as e:
        print(f"[CORE] Server error: {e}")
        raise
        
