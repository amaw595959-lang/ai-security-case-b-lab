"""Use the Phase B app with the Phase C data-handling policy installed first."""

import os
from pathlib import Path
from secrets import token_urlsafe

os.umask(0o077)
Path(os.environ["DATA_DIR"]).mkdir(mode=0o700, parents=True, exist_ok=True)
if not os.environ.get("WEBUI_SECRET_KEY"):
    os.environ["WEBUI_SECRET_KEY"] = token_urlsafe(32)

import uvicorn
from capture import install_audit, install_events

install_events()
from serve import app

install_audit(app)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, access_log=False)
