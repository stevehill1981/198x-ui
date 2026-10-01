#!/usr/bin/env python3
"""Every @font-face in fonts.css must point at a real file that covers its script."""
import re, sys
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = {
    "latin": "AZaz09",
    "latin-ext": "ĄŁŠŽŻ",
    "greek": "ΑΒΓΔΩαβγ",
    "cyrillic": "ЭлектроникаБК",
}

# Gaps we know about and have chosen to live with: file -> (missing chars, reason).
# A listed gap the font now covers fails as STALE, so the entry gets removed.
KNOWN_GAPS = {
    "nebula-sans-400-italic-greek.woff2": ("Δ", "absent from the kit's subset of Nebula Sans 1.010 italic"),
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
        known, reason = KNOWN_GAPS.get(url, ("", ""))
        stale = [c for c in known if c not in missing]
        unexpected = [c for c in missing if c not in known]
        accepted = [c for c in missing if c in known]
        if stale:
            print(f"STALE KNOWN GAP {url}: {''.join(stale)}"); failures += 1
        if unexpected:
            print(f"GAPS {url}: {''.join(unexpected)}"); failures += 1
        if accepted:
            print(f"KNOWN GAP {url}: {''.join(accepted)} ({reason})")
        if not (stale or unexpected or accepted):
            print(f"ok   {url}")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
