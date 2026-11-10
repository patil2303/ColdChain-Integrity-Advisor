import os
import sys

# Ensure server directory is in sys.path
server_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server")
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

from server.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
