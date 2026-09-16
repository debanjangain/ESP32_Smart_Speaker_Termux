import asyncio
from config_loader import load_config
from core.websocket_server import start_server

from database.sqlite_db import init_db


def main():
    init_db()

    config = load_config("config_master.yaml")

    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8765)

    print(f"[APP] Backend starting at ws://{host}:{port}")

    try:
        asyncio.run(start_server(host=host, port=port))
    except KeyboardInterrupt:
        print("[APP] Server stopped")


if __name__ == "__main__":
    main()
    
