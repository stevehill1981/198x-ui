"""Recover the KERNAL's pulses from an Emu198x SAVE recording that is offset by half a wave.

Emu198x (f9f6c77a) records the write line from the middle of one pulse to the middle
of the next, so each recorded interval r_i is (p_i + p_{i+1}) / 2. Starting from the
leader (all short pulses), p_{i+1} = 2 r_i - p_i, snapped to the KERNAL's three pulse
classes. The tape is proven by the KERNAL itself loading it: header and data blocks
carry checksums, and LOAD reports no error.
"""
import struct, sys
src, dst = sys.argv[1], sys.argv[2]
d = open(src, 'rb').read()
assert d[:12] == b'C64-TAPE-RAW' and d[12] == 1
rec = d[20:]
CLASSES = [0x30, 0x42, 0x56]  # short, medium, long, in TAP units (8 cycles)
snap = lambda v: min(CLASSES, key=lambda c: abs(c - v))
out = []
p = rec[0]
out.append(snap(p))
bad = 0
for r in rec[:-1]:
    if r < 20:  # stray edge at start/end of the recording
        continue
    nxt = 2 * r - p
    s = snap(nxt)
    if abs(s - nxt) > 6: bad += 1
    out.append(s)
    p = s
body = bytes(out)
open(dst, 'wb').write(b'C64-TAPE-RAW' + bytes([1, 0, 0, 0]) + struct.pack('<I', len(body)) + body)
print(f'{len(rec)} recorded -> {len(body)} pulses; {bad} snapped by more than 6')
