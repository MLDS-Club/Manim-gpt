#!/usr/bin/env python3
"""
Combine contents of all files in this script's directory into ALL_FILES.txt
(Non-recursive; always runs on the folder containing this file.)
"""

from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    out_path = root / "ALL_FILES.txt"
    self_path = Path(__file__).resolve()

    # Collect all regular files in the same directory, excluding this script and the output
    files = sorted(
        p for p in root.iterdir()
        if p.is_file() and p.resolve() not in {self_path, out_path.resolve()}
    )

    with out_path.open("w", encoding="utf-8", errors="replace") as out:
        for p in files:
            header = f"\n===== FILE: {p.name} ({p.stat().st_size} bytes) =====\n"
            out.write(header)
            try:
                with p.open("r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        out.write(line)
            except Exception as e:
                out.write(f"\n[Could not read file due to error: {e}]\n")

    print(f"Wrote {len(files)} files into {out_path}")

if __name__ == "__main__":
    main()
