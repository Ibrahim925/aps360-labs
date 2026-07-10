#!/usr/bin/env python3
"""Print the cells of a Jupyter notebook with indices, types, and content.

Reading a raw .ipynb with the plain Read tool buries the code in JSON. This
dumps cells cleanly so the tutor can see the student's work at a glance.

Usage:
    python show_cells.py "path/to/lab.ipynb"                # all cells
    python show_cells.py "path/to/lab.ipynb" 40 60          # cells 40..60
    python show_cells.py "path/to/lab.ipynb" --code         # code cells only
    python show_cells.py "path/to/lab.ipynb" --map          # one-line-per-cell overview
"""
import json
import sys


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        sys.exit(1)

    path = args[0]
    code_only = "--code" in args
    overview = "--map" in args
    nums = [int(a) for a in args[1:] if a.lstrip("-").isdigit()]
    lo, hi = (nums[0], nums[1]) if len(nums) >= 2 else (0, 10**9)

    nb = json.load(open(path))
    for i, c in enumerate(nb["cells"]):
        if not (lo <= i <= hi):
            continue
        if code_only and c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if overview:
            first = src.strip().split("\n")[0] if src.strip() else "(empty)"
            print(f"cell {i:>3} [{c['cell_type'][:2]}] {first[:80]}")
        else:
            body = src if src.strip() else "(EMPTY)"
            print(f"=== cell {i} [{c['cell_type']}] ===")
            print(body)
            print()


if __name__ == "__main__":
    main()
