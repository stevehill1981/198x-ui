/**
 * Frame crops its content to fill a box, and a capture is never cropped just
 * to fill one (decisions/family-visual-identity.md §7); a deliberate detail
 * view is not a Frame. The kit's capture components carry the classes below;
 * a site's own capture components mark their root with `data-capture`.
 * Rendered content holding either is refused.
 */
const CAPTURE_CLASSES = ['h-screen', 'h-figure-capture'];
const CLASS_ATTRIBUTE = /\sclass\s*=\s*(?:"([^"]*)"|'([^']*)')/g;
const CAPTURE_ATTRIBUTE = /<[a-zA-Z][^>]*\sdata-capture(?:[\s=>/])/;

export function refuseCaptures(html: string): void {
  let found: string | undefined;
  for (const match of html.matchAll(CLASS_ATTRIBUTE)) {
    found = (match[1] ?? match[2] ?? '').split(/\s+/).find(name => CAPTURE_CLASSES.includes(name));
    if (found) break;
  }
  if (!found && CAPTURE_ATTRIBUTE.test(html)) found = 'data-capture';
  if (found) {
    throw new Error(`Frame crops its content to fill a box, so it cannot hold a capture (found "${found}"). Show a capture with Screen or Figure; see decisions/family-visual-identity.md §7.`);
  }
}
