#!/usr/bin/env python3
"""Every @font-face in fonts.css must point at a real file that covers its script."""
import re, sys
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = {
    "latin": "AZaz09",
    "latin-ext": "ĄŁŠŽŻ",
    "greek": "ΑΒΓΩαβγ",
    "cyrillic": "ЭлектроникаБК",
}

def main() -> int:
    css = (ROOT / "fonts.css").read_text()
    failures = 0
    for url in re.findall(r"url\('/fonts/([^']+)'\)", css):
        path = ROOT / "fonts" / url
        subset = re.search(r"-(latin-ext|latin|greek|cyrillic)\.woff2$", url)
        if not path.exists():
            print(f"MISSING {url}"); failures += 1; continue
        if not subset:
            print(f"UNKNOWN SUBSET {url}"); failures += 1; continue
        cmap = TTFont(path).getBestCmap()
        missing = [c for c in SAMPLES[subset.group(1)] if ord(c) not in cmap]
        if missing:
            print(f"GAPS {url}: {''.join(missing)}"); failures += 1
        else:
            print(f"ok   {url}")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
