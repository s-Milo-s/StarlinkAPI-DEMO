import json
from pathlib import Path

# TODO: change to wherever your FastAPI app is
from app.main import app

OUT = Path("openapi/openapi.json")

spec = app.openapi()
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
print(f"Wrote {OUT}")
