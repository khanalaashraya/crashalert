# Alert Notifications

CrashAlert can send email through Brevo and start a phone call through
[DialF](https://github.com/Agora-Build/DialF) when an accident is detected.
DialF is MIT-licensed software that controls an Android phone's SIM through a
local daemon. The call uses the phone's carrier plan; carrier charges may apply.

Install and pair DialF with an Android phone first. Run the CrashAlert backend on
the same machine as `dialfd`; DialF's control socket is local. Find the device
name with `dialf devices`, then set these variables in that machine's `.env`:

```env
CRASHALERT_ENABLE_CALLS=true
DIALF_DEVICE=your_connected_phone
CRASHALERT_CALL_TO=+15557654321
# Optional when DialF uses a non-default control socket:
DIALF_SOCKET_PATH=/run/dialf/dialfd.sock
```

Calls are disabled unless explicitly enabled, and only the configured number is
called. This integration starts the call but does not play a spoken alert.
Repeated positive `/analyze` requests can start repeated calls. It does not
contact emergency services; verify detections and add alert deduplication before
using it in a real deployment.
