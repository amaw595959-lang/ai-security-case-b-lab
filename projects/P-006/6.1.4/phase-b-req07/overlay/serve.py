"""Load the lab router in the native pinned Open WebUI process."""

import os
from pathlib import Path
from secrets import token_urlsafe

os.umask(0o077)
Path(os.environ["DATA_DIR"]).mkdir(mode=0o700, parents=True, exist_ok=True)
if not os.environ.get("WEBUI_SECRET_KEY"):
    os.environ["WEBUI_SECRET_KEY"] = token_urlsafe(32)

import uvicorn

from open_webui.main import app

from preview import initialize, router


initialize()
# FastAPI routes must precede Open WebUI's single-page app fallback mount.
fallback = next((route for route in app.router.routes if route.name == "spa-static-files"), None)
if fallback is not None:
    app.router.routes.remove(fallback)
app.include_router(router)
if fallback is not None:
    app.router.routes.append(fallback)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, access_log=False)
