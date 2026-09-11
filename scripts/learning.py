#!/usr/bin/env python3
"""Compatibility entrypoint for the active Owner-first MVP runtime."""

from scripts import learning_v3 as _impl

for _name in dir(_impl):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_impl, _name)

if __name__ == "__main__":
    raise SystemExit(_impl.main())
