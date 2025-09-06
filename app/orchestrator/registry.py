"""Registry of test modules in execution order.

Each module must expose:
 - bp: a Flask Blueprint (name == slug)
 - MODULE_META: {"slug": str, "name": str}
"""

from app.modules.wmc import bp as wmc_bp, MODULE_META as wmc_meta

# Placeholder imports for future modules (add real ones when ready)
try:
    from app.modules.ira import bp as ira_bp, MODULE_META as ira_meta  # type: ignore
except Exception:  # pragma: no cover
    ira_bp = None
    ira_meta = {"slug": "ira", "name": "IRA"}

try:
    from app.modules.att import bp as att_bp, MODULE_META as att_meta  # type: ignore
except Exception:  # pragma: no cover
    att_bp = None
    att_meta = {"slug": "att", "name": "ATT"}

try:
    from app.modules.meta import bp as meta_bp, MODULE_META as meta_meta  # type: ignore
except Exception:  # pragma: no cover
    meta_bp = None
    meta_meta = {"slug": "meta", "name": "META"}

try:
    from app.modules.ips import bp as ips_bp, MODULE_META as ips_meta  # type: ignore
except Exception:  # pragma: no cover
    ips_bp = None
    ips_meta = {"slug": "ips", "name": "IPS"}

try:
    from app.modules.als import bp as als_bp, MODULE_META as als_meta  # type: ignore
except Exception:  # pragma: no cover
    als_bp = None
    als_meta = {"slug": "als", "name": "ALS"}


MODULES = [
    {"bp": wmc_bp, "meta": wmc_meta},
]

# Include placeholders if available (so routes exist for early testing)
if ira_bp:
    MODULES.append({"bp": ira_bp, "meta": ira_meta})
if att_bp:
    MODULES.append({"bp": att_bp, "meta": att_meta})
if meta_bp:
    MODULES.append({"bp": meta_bp, "meta": meta_meta})
if ips_bp:
    MODULES.append({"bp": ips_bp, "meta": ips_meta})
if als_bp:
    MODULES.append({"bp": als_bp, "meta": als_meta})


ORDER = [m["meta"]["slug"] for m in MODULES]

