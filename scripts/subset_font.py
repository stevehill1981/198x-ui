#!/usr/bin/env python3
"""Split an upstream font into the kit's four subsets: scripts/subset_font.py SRC NAME WEIGHT STYLE."""
import subprocess, sys
from pathlib import Path

RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latin-ext": "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
    "greek": "U+0370-03FF",
    "cyrillic": "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116",
}

def main(src: str, name: str, weight: str, style: str) -> None:
    out = Path(__file__).resolve().parent.parent / "fonts"
    suffix = f"{weight}-italic" if style == "italic" else weight
    for subset, unicodes in RANGES.items():
        target = out / f"{name}-{suffix}-{subset}.woff2"
        subprocess.run(["pyftsubset", src, f"--unicodes={unicodes}", "--flavor=woff2",
                        "--layout-features=*", f"--output-file={target}"], check=True)
        print(target.name)

if __name__ == "__main__":
    main(*sys.argv[1:5])
