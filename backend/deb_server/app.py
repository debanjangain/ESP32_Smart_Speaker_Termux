import asyncio
from pathlib import Path

from config_loader import load_config
from core.websocket_server import start_server
from database.sqlite_db import init_db

CONFIG_FILE = Path(__file__).parent / "config_master.yaml"


def main():
    init_db()

    config = load_config(CONFIG_FILE)

    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8765)

    print(f"[APP] Backend starting at ws://{host}:{port}")

    try:
        asyncio.run(start_server(host=host, port=port))
    except KeyboardInterrupt:
        print("[APP] Server stopped")
    except Exception as e:
        print(f"[APP] Startup failed: {e}")


if __name__ == "__main__":
    main()
    
