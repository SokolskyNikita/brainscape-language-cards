"""Run a card-workspace script with stable imports and working directory."""
from pathlib import Path
import os
import runpy
import sys


def main():
    root = Path(__file__).resolve().parent
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python cards/run.py WORKSPACE/SCRIPT.py [arguments ...]")
    script = (root / sys.argv[1]).resolve()
    if not script.is_relative_to(root) or not script.is_file() or script == Path(__file__).resolve():
        raise SystemExit("Choose a Python script inside cards/")
    sys.path[:0] = [str(script.parent), str(root), str(root.parent / "api-client")]
    os.chdir(root)
    sys.argv = [str(script), *sys.argv[2:]]
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
