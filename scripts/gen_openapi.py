import sys
from pathlib import Path
import json

# add repo root (Backend/) to import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app  # <-- because main.py is in Backend/

OUT = Path("openapi/openapi.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

spec = app.openapi()
OUT.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
print(f"Wrote {OUT}")