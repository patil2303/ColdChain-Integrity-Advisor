import os
import sys

# Ensure server and root directory are in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
server_dir = os.path.join(root_dir, "server")
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from server.main import app
