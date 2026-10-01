/**
 * The whole-multiple rule for a screen, shared by Screen and Loading so the two
 * cannot drift apart. family-visual-identity.md §7: a capture renders at a
 * whole multiple of its true grid, never a fraction; only a cell narrower than
 * the grid at 1x (a phone) may scale it down, and then it fits the cell.
 *
 * `fitToGrid` sizes `el` to k x the grid, where k is a whole number from 1 to
 * `data-max-scale`, and sets the scanline variables Screen's CRT look reads.
 * It runs in the browser; the element's own cell decides the space it has.
 */
export function fitToGrid(el: HTMLElement, w: number, h: number): number {
  if (!el.parentElement) return 0;
  /* Measure the space this element's own cell gives it, not its parent's. */
  el.style.width = 'auto';
  el.style.justifySelf = 'stretch';
  el.style.alignSelf = 'start';
  let avail = el.getBoundingClientRect().width;
  /* A flex row gives an auto-width box no size of its own; fall back to the
     parent's content box, less this element's margins. */
  if (!avail) {
    const cs = getComputedStyle(el);
    const pcs = getComputedStyle(el.parentElement);
    avail = el.parentElement.clientWidth
      - parseFloat(pcs.paddingLeft) - parseFloat(pcs.paddingRight)
      - parseFloat(cs.marginLeft) - parseFloat(cs.marginRight);
  }
  el.style.justifySelf = '';
  el.style.alignSelf = '';
  const max = Math.max(1, Math.floor(Number(el.dataset.maxScale) || 1));
  const k = avail >= w ? Math.min(max, Math.floor(avail / w)) : avail / w;
  el.style.width = `${w * k}px`;
  el.style.aspectRatio = `${w} / ${h}`;
  el.style.setProperty('--lines', String(h));
  // Scanlines in device pixels: a source line covers k * dpr of them.
  const dpr = window.devicePixelRatio || 1;
  const linePx = k * dpr;
  if (Number.isInteger(k) && linePx >= 2) {
    el.style.setProperty('--line-px', `${k}px`);
    el.style.setProperty('--scan-dark', `${Math.max(1, Math.floor(linePx / 2)) / dpr}px`);
    el.dataset.scan = 'on';
  } else {
    el.style.removeProperty('--line-px');
    el.style.removeProperty('--scan-dark');
    el.dataset.scan = 'off';
  }
  el.dataset.scale = String(k);
  return k;
}

/** Call `refit` again on resize, and when devicePixelRatio changes (page zoom,
 *  moving between displays), which changes how many device pixels a line covers. */
export function refitOnChange(refit: () => void): void {
  let t: ReturnType<typeof setTimeout>;
  addEventListener('resize', () => {
    clearTimeout(t);
    t = setTimeout(refit, 100);
  });
  const watchDpr = () => {
    const mq = matchMedia(`(resolution: ${window.devicePixelRatio || 1}dppx)`);
    mq.addEventListener('change', () => { refit(); watchDpr(); }, { once: true });
  };
  watchDpr();
}
