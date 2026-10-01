/**
 * The catalogue's table of contents. A consuming site imports this to list the
 * routes it mounts (one per entry, plus the index), so adding an entry here is
 * the whole of adding it to every site's catalogue.
 */
export interface CatalogueEntry {
  /** URL segment and key into Catalogue.astro's component map. */
  slug: string;
  /** The component's file name, as a reader would search for it. */
  title: string;
}

export const catalogueEntries: CatalogueEntry[] = [
  { slug: 'plate', title: 'Plate' },
  { slug: 'site-nav', title: 'SiteNav' },
  { slug: 'family-strip', title: 'FamilyStrip' },
  { slug: 'screen', title: 'Screen' },
  { slug: 'button', title: 'Button' },
  { slug: 'eyebrow', title: 'Eyebrow' },
  { slug: 'shell', title: 'Shell' },
  { slug: 'theme-toggle', title: 'ThemeToggle' },
  { slug: 'tabs', title: 'Tabs' },
  { slug: 'listing', title: 'Listing' },
  { slug: 'kbd', title: 'Kbd' },
  { slug: 'tile', title: 'Tile' },
  { slug: 'figure', title: 'Figure' },
  { slug: 'breadcrumbs', title: 'Breadcrumbs' },
  { slug: 'chip', title: 'Chip' },
  { slug: 'search-field', title: 'SearchField' },
];
