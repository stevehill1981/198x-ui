/**
 * What each machine showed while it was busy loading, as data for Loading.astro.
 *
 * Governed by 198x/decisions/family-visual-identity.md §7: "A loading state
 * shows what that machine showed while it was busy, quoted from a source, never
 * borrowed from another machine." So every value here sits next to the source
 * it was taken from, and a machine with no entry has no look: Loading refuses
 * to build rather than lend it another machine's.
 *
 * Paths are relative to the family umbrella, ~/Projects/198x/. "LOH" is Logan
 * and O'Hara, *The Complete Spectrum ROM Disassembly*. Line numbers are in the
 * text extracts under reference/. The research that gathered them, with the
 * gaps it found, is "Code198x Loading component research, 2026-10-01".
 *
 * To add a machine: find what its stock loader put on screen in a primary
 * source (a ROM listing, the maker's manual) or an Emu198x capture of an
 * official ROM, write the entry with its citations, and add it to `looks`.
 * Anything the machine printed is a capture of a program named GAME, made
 * the way the ones below were, with its script in loading-captures/source/.
 * Common belief is not a source; leave a fact out rather than guess it.
 *
 * Units: positions and sizes are source pixels (lines, for heights) on the
 * machine's own grid, so the component can draw them proportionally at any
 * scale. Times are seconds from the moment Loading appears.
 *
 * Captures. Where the machine printed a message, the frame is a real Emu198x
 * capture in loading-captures/, never text set in a font: the machine's
 * characters came from its character ROM, and only a capture shows them as
 * they were. Every capture is of a program named GAME, so that is the only
 * name Loading can show. How each was made is under its machine below, and
 * the scripts and media that make them are in loading-captures/source/.
 *
 * The capture PNGs are screenshots of the machines, not code of ours, and the
 * MIT grant in LICENSE does not cover them. They are output, as the lesson
 * screenshots on the family sites are (198x/decisions/system-rom-sourcing.md):
 * no ROM, character set or font is embedded here or drawn from.
 */

/** A real frame from Emu198x, stored in loading-captures/ at the emulator's
 *  native size, border included, so Loading can show it at whole multiples. */
export interface Capture {
  /** File name in loading-captures/. */
  file: string;
  /** Stored size in pixels: the machine's grid, as Emu198x writes it. */
  width: number;
  height: number;
  /** What it shows, for the source notes. */
  shows: string;
}

/** A border band pattern: one colour per tape pulse, alternating. */
export interface Stripes {
  /** The two colours, in the order the pulses alternate them. */
  colours: [string, string];
  /** Each band's height in source lines, one per pulse. Repeats. */
  bands: number[];
}

/** One state of the screen. Each holds until the next one's `at`. A frame is
 *  exactly one of: a capture, a flat field, or border stripes. */
export type Frame =
  | {
      /** Seconds from start when this state appears. The first is 0. */
      at: number;
      /** The whole screen is this capture, as the machine showed it. */
      capture: Capture;
    }
  | {
      at: number;
      /** The whole screen is one colour: a blanked C64, an Amiga's COLOR00. */
      fill: string;
    }
  | {
      at: number;
      /** The border is drawn as this stripe pattern (keyed into `stripes`),
       *  because it changed faster than any capture can show. */
      stripes: 'pilot' | 'data';
      /** The paper, shown from this capture's own pixels, unaltered. The
       *  machine did not touch the paper while the border striped. */
      paper: Capture;
    };

export interface LoadingLook {
  kind: 'look';
  /** The machine's id, as in machines.json. */
  machine: string;
  /** The medium this look is for, where the machine had more than one. */
  media: string;
  /** How Loading names it to a screen reader: "ZX Spectrum, tape". */
  title: string;
  /** The machine's screen, in source pixels. */
  grid: { w: number; h: number };
  /** Where the paper sits on that grid, in source pixels: the part of a
   *  capture a stripes frame shows. */
  paper?: { x: number; y: number; w: number; h: number };
  /** Border stripe patterns, for frames that use them. */
  stripes?: { pilot?: Stripes; data?: Stripes };
  /** Border stripe drift, in source lines per second, upwards. See the
   *  Spectrum entry for why this is not the machine's own rate. */
  drift?: number;
  /** A drive light lit from `from` seconds onwards. */
  led?: { colour: string; from: number; note: string };
  frames: Frame[];
  /** Where every value above came from. */
  sources: string[];
}

/** A machine with nothing to load: the program is in the machine already. */
export interface NoLoad {
  kind: 'none';
  machine: string;
  title: string;
  why: string;
  sources: string[];
}

/* ---- ZX Spectrum 48K, the ROM tape loader ---------------------------------
 *
 * LD-BYTES at 0556 changes the border at every tape edge (LOH:1427, "A new 'edge' has
 * been found ... So change the border colour"; the OUT at LOH:1434-1435 is
 * commented "Change the border colour (RED/CYAN or BLUE/YELLOW)"). The pilot
 * alternates red (2) and cyan (5), LOH:1250-1264; after the sync, XOR +03 turns
 * them into blue (1) and yellow (6) for the data, LOH:1305-1306. The paper is
 * not touched: LD-BYTES never writes the display file. On finding a header,
 * BASIC prints its type and name, "Program:" for a program (LOH:1760; message
 * table LOH:2264-2267), at the top-left of the paper (Emu198x capture below).
 *
 * Band heights: each colour lasts one pulse. A pilot pulse is 2,168 T-states
 * (LOH:1070), a 0 bit two pulses of 855 and a 1 bit two "exactly twice as
 * long", 1,710 (LOH:1190-1191),
 * and a 48K line is 224 T-states (reference/by-system/sinclair-zx-spectrum/
 * ula-timing-expanded.md:59-60). So 9.68 lines per pilot band, 3.82 per 0-bit
 * band, 7.63 per 1-bit band. An Emu198x capture of the 48K ROM loading a TAP,
 * 2026-10-01, measured pilot bands of 9 to 10 lines and data bands of 3 to 4
 * and 7 to 8 (held with the research).
 *
 * Geometry: Emu198x's Spectrum capture is 352x296 with the 256x192 paper at
 * (48, 48), measured from the captures below. Colours are Emu198x's normal
 * (not BRIGHT) palette, Emu198x/emu198x/crates/common-sinclair-zx-spectrum/
 * src/palette.rs:107-125; the border never uses BRIGHT.
 *
 * Drift: the pilot pattern rises because 2 x 2,168 does not divide the
 * 69,888-T frame; it moves 512/224 = 2.29 lines a frame, 114 lines a second
 * at 50 Hz ("red and cyan stripes moving slowly upwards", +2 manual,
 * reference/by-system/sinclair-zx-spectrum/sinclair-zx-spectrum-plus-2-manual.txt:4626-4637).
 * At that rate every point of the border flips red to cyan about twelve times
 * a second across most of the screen, which fails WCAG 2.3.1 (three flashes)
 * and its red-flash rule. So the stripes drift at 15 lines a second: the band
 * heights, colours, order and direction are the machine's; the speed is
 * slowed by 7.6 times so no point flashes more than twice a second.
 *
 * Captures: Emu198x f9f6c77a (2026-10-01), 48K variant, the official ROM
 * (~/.emu198x/roms/sinclair-zx-spectrum-48k/48.rom, SHA1
 * 5ea7c2b824672e914525d1d5c419d71b84a426a2). The tape, loading-captures/
 * source/zx-game.tap, is `10 PRINT "HELLO"` saved as GAME by the ROM's own
 * SAVE inside Emu198x (source/zx-save.mcp.json, over MCP). The frames come from
 * `emu198x-spectrum --script source/zx-tape.json`, run from source/: it types
 * LOAD "" and starts the tape, and the shots are 278 and 330 frames after
 * that. Once the header is read, "Program: GAME" is on the paper and the border
 * is back to white for 50 frames, then cyan for 50 more while LD-BYTES waits
 * for the data block's leader (counted frame by frame from the same run).
 *
 * Phases, all from that run: white for 1.0 s, cyan for 1.0 s, then the data
 * block's leader for about two seconds (LOH:1053-1059; the +2 manual's "two
 * seconds", :4630), then the data. The machine leaves the paper alone the
 * whole time, so the stripe frames show the paper from the white capture,
 * pixel for pixel, inside drawn stripes. (Both captures' papers are identical;
 * the white one's border is the paper's own #C2C2C2, so where a browser
 * softens the clip's edge at a fractional scale it softens into paper, not
 * into a cyan line.) The data stripes are the real data
 * block of zx-game.tap, flag byte first, repeated so the pattern's seam is off
 * screen; the real block is that short.
 */
const SPECTRUM_LINE_T = 224;
const band = (t: number) => Math.round((t / SPECTRUM_LINE_T) * 100) / 100;

/** The data block of loading-captures/source/zx-game.tap: flag, the program
 *  `10 PRINT "HELLO"`, checksum. */
const ZX_GAME_DATA = [
  0xff, 0x00, 0x0a, 0x09, 0x00, 0xf5, 0x22, 0x48, 0x45, 0x4c, 0x4c, 0x4f, 0x22, 0x0d, 0x46,
];

/** Data bands for the Spectrum: each byte, most significant bit first, as two
 *  pulses per bit (LOH:1190-1191), repeated until the pattern is at least `min`
 *  lines tall so its repeat is off screen. */
function spectrumDataBands(bytes: number[], min = 600): Stripes {
  const zero = band(855);
  const one = band(1710);
  const bands: number[] = [];
  let total = 0;
  while (total < min) {
    for (const byte of bytes) {
      for (let bit = 7; bit >= 0; bit--) {
        const h = (byte >> bit) & 1 ? one : zero;
        bands.push(h, h);
        total += 2 * h;
      }
    }
  }
  return { colours: ['#0000C2', '#C2C200'], bands };
}

const zxHeader: Capture = {
  file: 'zx-header.png',
  width: 352,
  height: 296,
  shows: 'Program: GAME on the paper, white border: the header read, before the data block',
};
const zxHeaderWait: Capture = {
  file: 'zx-header-wait.png',
  width: 352,
  height: 296,
  shows: 'Program: GAME on the paper, cyan border: LD-BYTES waiting for the data leader',
};

const spectrum: LoadingLook = {
  kind: 'look',
  machine: 'sinclair-zx-spectrum',
  media: 'tape',
  title: 'ZX Spectrum, tape',
  grid: { w: 352, h: 296 },
  paper: { x: 48, y: 48, w: 256, h: 192 },
  stripes: {
    pilot: { colours: ['#C20000', '#00C2C2'], bands: [band(2168), band(2168)] },
    data: spectrumDataBands(ZX_GAME_DATA),
  },
  drift: 15,
  frames: [
    { at: 0, capture: zxHeader },
    { at: 1, capture: zxHeaderWait },
    { at: 2, stripes: 'pilot', paper: zxHeader },
    { at: 4, stripes: 'data', paper: zxHeader },
  ],
  sources: [
    "LOH: reference/by-system/sinclair-zx-spectrum/the-complete-spectrum-rom-disassembly-dr-ian-logan-dr-frank-o-hara.txt, lines 1053-1059, 1070-1076, 1190-1191, 1250-1264, 1305-1306, 1427-1435, 1760, 2264-2267",
    'reference/by-system/sinclair-zx-spectrum/ula-timing-expanded.md:59-60',
    'reference/by-system/sinclair-zx-spectrum/sinclair-zx-spectrum-plus-2-manual.txt:4626-4637',
    'Emu198x/emu198x/crates/common-sinclair-zx-spectrum/src/palette.rs:107-125',
    'Emu198x capture of the 48K ROM loading a TAP, 2026-10-01: pilot runs of 9-10 lines, data runs of 3-4 and 7-8',
    'loading-captures/zx-header.png, zx-header-wait.png: Emu198x f9f6c77a, 48.rom SHA1 5ea7c2b8, source/zx-tape.json',
  ],
};

/* ---- Commodore 64, the KERNAL tape and disk loaders -----------------------
 *
 * Sources: Commodore 64 Programmer's Reference Guide (PRG),
 * reference/by-system/commodore-c64/1983-commodore-64-programmers-reference-guide.txt;
 * Commodore 64 User's Guide (UG), .../1982-commodore-64-users-guide.txt;
 * COMPUTE!'s Mapping the Commodore 64 (MAP), .../compute-s-mapping-the-commodore-64.txt.
 *
 * Tape. The transcript is the PRG's own example (PRG:3012-3014): LOAD "STAR
 * TREK", PRESS PLAY ON TAPE, FOUND STAR TREK, LOADING, READY. "The Commodore
 * 64 will blank the screen to the border color after the PLAY key is pressed.
 * When the program is found, the screen clears to the background color and
 * the FOUND message is displayed" (PRG:2964-2974); pressing the Commodore key,
 * "the screen will again turn the border color while the program is LOADed"
 * (UG:933-950). Blanking fills "the entire screen" with the border colour
 * (MAP:8023-8027), so the busy state is one unbroken field: no stripes, which
 * belong to commercial turbo loaders that nothing held documents. The tape
 * look plays the sequence once and holds the blanked field; the timings
 * between messages are ours (the real ones depend on the tape).
 *
 * Disk (1541). LOAD "FUN",8, SEARCHING FOR FUN, LOADING, READY. (PRG:3021-3031).
 * The screen is not blanked. The drive's red light is "DRIVE INDICATOR ...
 * ACTIVE" (reference/by-system/commodore-1541/commodore-1541-disk-drive-users-
 * guide-1982-09-commodore.txt:300-315). The source names it red; the hex is a
 * rendering choice, not a quoted value.
 *
 * Colours: default border 14, light blue (MAP:8023-8033), which is what a
 * blanked screen shows; #7868C0 from Emu198x's VIC-II palette,
 * Emu198x/emu198x/crates/mos-vic-ii/src/palette.rs:7-22, and the colour of
 * every pixel of the blanked frames in the run below.
 *
 * Captures: Emu198x f9f6c77a (2026-10-01), PAL C64 with the stock ROMs in
 * ~/.emu198x/roms/commodore-c64/: KERNAL SHA1 1d503e56df85a62fee696e7618dc5b4e781df1bb,
 * BASIC 79015323128650c742a3694c9429aa91f355905e, character ROM
 * adc7c31e18c7c7413d54802ef2f4193da14711aa, 1541 DOS
 * d3b78c3dbac55f5199f33f3fe0036439811f7fb3. All four message frames are 416x312,
 * border included, and are each one frame of these runs, unaltered:
 *
 * - Tape: `emu198x-c64 --script source/c64-tape.json`, run from source/. The
 *   tape, source/c64-game.tap, is `10 PRINT "HELLO"` saved as GAME by the
 *   KERNAL inside Emu198x (source/c64-save.mcp.json, over MCP). Emu198x
 *   f9f6c77a records SAVE half a wave out of phase, so its raw recording
 *   (source/c64-game.recorded.tap) does not load; source/c64-tap-rephase.py
 *   recovers the pulses, and the KERNAL loading the result, checksums and all,
 *   then listing the program, is the check (emu198x/emu198x#1565). In the run,
 *   PRESS PLAY ON TAPE shows until the tape starts; the screen is blanked for
 *   730 frames while it searches; FOUND GAME shows for 565 frames (the KERNAL
 *   waits for the Commodore key or a timeout); then LOADING is printed and the
 *   screen blanked on the same frame, and it stays blanked until READY. So
 *   the machine never shows LOADING while it loads from tape, and neither does
 *   Loading. Its times are shorter than the machine's, and are ours.
 * - Disk: `emu198x-c64 --script source/c64-disk.json`. The disk,
 *   source/c64-game.d64, holds the same program as GAME, built with VICE 3.10's
 *   petcat and c1541 from source/game.bas. SEARCHING FOR GAME is 40 frames
 *   after RETURN, LOADING 84. A one-line program loads in two frames; the
 *   look holds LOADING, the state a longer program would stay in.
 */
const C64_LIGHT_BLUE = '#7868C0';
const c64Common = {
  kind: 'look' as const,
  machine: 'commodore-64',
  grid: { w: 416, h: 312 },
};
const c64Sources = [
  'PRG: reference/by-system/commodore-c64/1983-commodore-64-programmers-reference-guide.txt:2964-2974, 3012-3031',
  'UG: reference/by-system/commodore-c64/1982-commodore-64-users-guide.txt:925-950',
  'MAP: reference/by-system/commodore-c64/compute-s-mapping-the-commodore-64.txt:8023-8033',
  'Emu198x/emu198x/crates/mos-vic-ii/src/palette.rs:7-22',
];
const c64Capture = (file: string, shows: string): Capture => ({ file, width: 416, height: 312, shows });

const c64Tape: LoadingLook = {
  ...c64Common,
  media: 'tape',
  title: 'Commodore 64, tape',
  frames: [
    { at: 0, capture: c64Capture('c64-tape-press-play.png', 'LOAD "GAME", PRESS PLAY ON TAPE') },
    { at: 1.5, fill: C64_LIGHT_BLUE },
    { at: 4, capture: c64Capture('c64-tape-found.png', 'OK, SEARCHING FOR GAME, FOUND GAME: the header read') },
    { at: 5.5, fill: C64_LIGHT_BLUE },
  ],
  sources: [
    ...c64Sources,
    'loading-captures/c64-tape-press-play.png, c64-tape-found.png: Emu198x f9f6c77a, KERNAL SHA1 1d503e56, source/c64-tape.json',
  ],
};

const c64Disk: LoadingLook = {
  ...c64Common,
  media: 'disk',
  title: 'Commodore 64, 1541 disk',
  led: { colour: '#E8291C', from: 0, note: "1541 drive light: red, named by Commodore's 1541 user's guide; the hex is ours" },
  frames: [
    { at: 0, capture: c64Capture('c64-disk-searching.png', 'LOAD "GAME",8, SEARCHING FOR GAME') },
    { at: 1.5, capture: c64Capture('c64-disk-loading.png', 'LOAD "GAME",8, SEARCHING FOR GAME, LOADING') },
  ],
  sources: [
    ...c64Sources,
    'reference/by-system/commodore-1541/commodore-1541-disk-drive-users-guide-1982-09-commodore.txt:300-315',
    'loading-captures/c64-disk-searching.png, c64-disk-loading.png: Emu198x f9f6c77a, KERNAL SHA1 1d503e56, 1541 DOS SHA1 d3b78c3d, source/c64-disk.json',
  ],
};

/* ---- Commodore Amiga 500, Kickstart 1.3 ------------------------------------
 *
 * The colour milestones are named in "Amiga Startup Routine" (Roy Frisque,
 * Amiga Transactor), reference/by-system/commodore-amiga/amiga-startup-routine.docling/
 * amiga-startup-routine.md:29-39 ("DARK GRAY ... LIGHT GRAY ... WHITE"), and in
 * Commodore's A500 service manual (.../a500-service-manual-pn-314981-04-oct-1990-text.txt:1505-1515).
 * The values are the COLOR00 writes the official 1.3 ROM makes itself, logged
 * under Emu198x on 2026-10-01: $444 at $FC0138, $888 at $FC0260, $FFF at
 * $FCAED4 (reference/by-system/commodore-amiga/amiga-boot-sequence.md:109-124).
 * With no bitplanes on, COLOR00 is the whole screen, so each step is one field.
 *
 * After white comes the insert-disk screen: a still picture (frames 150 apart
 * are identical under 1.3) of a hand holding a disk, on the same white ground
 * (amiga-boot-sequence.md:604-610). It is Commodore's artwork and is not
 * reproduced here: Loading holds the white field, which is that screen's
 * ground, rather than drawing an imitation of the picture.
 *
 * Timing from an Emu198x capture of the same ROM at 50 Hz: dark grey by frame
 * 30, white by frame 100 (held with the research); the light
 * grey fell between captures, so its 0.8 seconds here is ours.
 *
 * The drive light: "while the disk drive is working, the disk drive light ...
 * is on" (reference/by-system/commodore-amiga/1987-introduction-to-the-amiga-500.txt:990-1004).
 * Its colour, green, is given by a third-party book (1988-amiga-for-beginners.txt:391-394);
 * Commodore's own manual names no colour. The hex is ours. It is lit with the
 * white field, when Kickstart turns to the disk.
 */
const amiga: LoadingLook = {
  kind: 'look',
  machine: 'commodore-amiga',
  media: 'disk',
  title: 'Amiga 500, Kickstart 1.3',
  grid: { w: 320, h: 256 },
  led: { colour: '#3BD45A', from: 1.4, note: 'A500 drive light: green per Amiga for Beginners (third-party); the hex is ours' },
  frames: [
    { at: 0, fill: '#444444' },
    { at: 0.6, fill: '#888888' },
    { at: 1.4, fill: '#FFFFFF' },
  ],
  sources: [
    'reference/by-system/commodore-amiga/amiga-startup-routine.docling/amiga-startup-routine.md:29-39',
    'reference/by-system/commodore-amiga/a500-service-manual-pn-314981-04-oct-1990-text.txt:1505-1515',
    'reference/by-system/commodore-amiga/amiga-boot-sequence.md:109-124, 604-610 (COLOR00 writes logged from kick13.rom 34.5 under Emu198x, 2026-10-01)',
    'reference/by-system/commodore-amiga/1987-introduction-to-the-amiga-500.txt:990-1004',
    'reference/by-system/commodore-amiga/1988-amiga-for-beginners.txt:391-394',
    'Emu198x capture of Kickstart 1.3 power-up, 2026-10-01, frames 30, 100, 300',
  ],
};

/* ---- Cartridge machines: nothing to load ---------------------------------- */
const nes: NoLoad = {
  kind: 'none',
  machine: 'nintendo-entertainment-system',
  title: 'NES',
  why:
    'The cartridge is mapped straight into the CPU\'s address space ($4020-$FFFF) and power-on enters through the reset vector, so nothing is transferred and there is no loading phase.',
  sources: [
    'reference/by-system/nintendo-nes/nintendo-nes-reference.md:140-152',
    'reference/by-system/nintendo-nes/memory-map.md:262-282',
  ],
};

const masterSystem: NoLoad = {
  kind: 'none',
  machine: 'sega-master-system',
  title: 'Master System',
  why: 'The cartridge or card is mapped straight in; the game runs with no load step.',
  sources: ['reference/by-system/sega-master-system/sms-reference.md:85, 537 (a distilled reference, not a primary source)'],
};

/** Every machine with a sourced look, keyed by machine id. The first look for a
 *  machine is its default medium. */
export const looks: Record<string, (LoadingLook | NoLoad)[]> = {
  'sinclair-zx-spectrum': [spectrum],
  'commodore-64': [c64Tape, c64Disk],
  'commodore-amiga': [amiga],
  'nintendo-entertainment-system': [nes],
  'sega-master-system': [masterSystem],
};

/** The look for a machine and medium, or a clear error. Never a fallback. */
export function loadingLook(machine: string, media?: string): LoadingLook | NoLoad {
  const set = looks[machine];
  if (!set) {
    throw new Error(
      `[198x-ui] Loading: no sourced loading look for "${machine}". A loading state shows what ` +
        'that machine showed, quoted from a source, never borrowed from another machine (§7). ' +
        `Add one to components/loading-looks.ts with its citations. Sourced: ${Object.keys(looks).join(', ')}.`,
    );
  }
  if (media === undefined) return set[0];
  const look = set.find((l) => l.kind === 'none' || l.media === media);
  if (!look) {
    const have = set.map((l) => (l.kind === 'look' ? l.media : 'none')).join(', ');
    throw new Error(`[198x-ui] Loading: "${machine}" has no sourced look for media="${media}". Sourced: ${have}.`);
  }
  return look;
}
