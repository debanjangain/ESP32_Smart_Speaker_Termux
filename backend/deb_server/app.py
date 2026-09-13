import asyncio
from config_loader import load_config
from core.websocket_server import start_server

# SQLite memory imports
from database.sqlite_db import init_db, remember_fact, recall_fact, forget_fact
from database.models import MemoryKeys

def main():
    # Initialize SQLite memory
    init_db()

    # Load master config
    config = load_config("config_master.yaml")

    # Server settings
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8765)

    print(f"[APP] Backend starting at ws://{host}:{port}")

    # Start WebSocket server
    asyncio.run(start_server(host=host, port=port))

if __name__ == "__main__":
    main()
