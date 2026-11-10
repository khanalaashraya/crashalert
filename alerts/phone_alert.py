import json
import os
import socket
import sys

from dotenv import load_dotenv

load_dotenv()


def _dialf_socket_path() -> str:
    configured_path = os.getenv("DIALF_SOCKET_PATH")
    if configured_path:
        return os.path.expanduser(configured_path)

    candidates = []
    runtime_dir = os.getenv("XDG_RUNTIME_DIR")
    if runtime_dir:
        candidates.append(os.path.join(runtime_dir, "dialfd.sock"))

    user_id = os.getuid() if hasattr(os, "getuid") else 0
    candidates.append(f"/tmp/dialfd-{user_id}.sock")
    candidates.append(
        "/var/run/dialfd.sock" if sys.platform == "darwin" else "/run/dialf/dialfd.sock"
    )

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]


def send_alert_call() -> dict:
    if os.getenv("CRASHALERT_ENABLE_CALLS", "false").strip().lower() != "true":
        return {"call_placed": False, "call_reason": "Voice calls are disabled"}

    device = os.getenv("DIALF_DEVICE")
    to_number = os.getenv("CRASHALERT_CALL_TO")

    if not device or not to_number:
        return {"call_placed": False, "call_reason": "DialF call settings are incomplete"}

    try:
        request = {
            "id": "crashalert-call",
            "op": "call.dial",
            "device": device,
            "number": to_number,
        }
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(15)
            connection.connect(_dialf_socket_path())
            reader = connection.makefile("rb")
            connection.sendall((json.dumps(request) + "\n").encode("utf-8"))

            for line in reader:
                if not line.strip():
                    continue
                response = json.loads(line)
                if not response.get("done"):
                    continue
                if not response.get("ok"):
                    return {
                        "call_placed": False,
                        "call_reason": response.get("error", "DialF rejected the call"),
                    }
                return {"call_placed": True}

        return {"call_placed": False, "call_reason": "DialF closed the connection without a result"}
    except (OSError, json.JSONDecodeError) as error:
        print(f"Failed to place CrashAlert call through DialF: {error}")
        return {"call_placed": False, "call_reason": "Could not reach the DialF daemon"}