import os
import sys
from backend import create_app

app = create_app()


def _env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except Exception:
        return int(default)


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = _env_int('PORT', 5000)
    try:
        app.run(host=host, port=port)
    except OSError as e:
        # more friendly message when port is in use
        print(f"Failed to start server on {host}:{port}: {e}")
        print("Check which process is using the port and stop it, or start with a different port:")
        print(f"  lsof -i :{port}")
        print(f"  kill <PID>")
        print(f"Or run with another port: PORT=8000 python run.py")
        sys.exit(1)
