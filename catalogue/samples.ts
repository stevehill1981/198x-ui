/**
 * Captures the catalogue shows, by URL. The kit ships no images: these are
 * files a consuming site already serves, so the defaults below are paths on
 * code198x.com (Code198x/website `public/images/`). Another site passes its own
 * set to Catalogue's `samples` prop, or leaves the Screen entry showing broken
 * images, which says plainly what is missing.
 *
 * Each sample exists to prove one of Screen's rules, so pick replacements with
 * the same shape, not just any capture.
 */
export interface Sample {
  src: string;
  alt: string;
  /** Stored file size in px. */
  width: number;
  height: number;
}

export interface CatalogueSamples {
  /** A 352x296 Spectrum capture, stored at its true grid. */
  spectrum: Sample;
  /** A capture stored with every column doubled: wider than 1.8:1. */
  doubled: Sample;
  /** An Amiga capture stored at 640x512, twice its 320x256 grid. */
  amiga: Sample;
  /** A 256x240 NES capture, small enough to reach 2x on a desktop. */
  nes: Sample;
}

export const code198xSamples: CatalogueSamples = {
  spectrum: {
    src: '/images/sinclair-zx-spectrum/basic/meet-basic/unit-01/step-02-two-lines.png',
    alt: 'The Spectrum screen after RUN: Hello, then from the Spectrum, and the report 0 OK, 20:1.',
    width: 352,
    height: 296,
  },
  doubled: {
    src: '/images/systems/acorn-bbc-micro/poster.png',
    alt: 'The BBC Micro start-up screen, captured in our emulator.',
    width: 640,
    height: 256,
  },
  amiga: {
    src: '/images/commodore-amiga/assembly/signal/unit-13/screenshot.png',
    alt: 'Signal, from the 68000 assembly track, on an Amiga 500.',
    width: 640,
    height: 512,
  },
  nes: {
    src: '/images/nintendo-entertainment-system/assembly/dash/unit-13/screenshot.png',
    alt: 'Dash, from the 6502 assembly track, on an NTSC NES.',
    width: 256,
    height: 240,
  },
};
