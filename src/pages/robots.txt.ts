import type { APIRoute } from 'astro';
export const GET: APIRoute = ({ site }) => {
  const allowed =
    import.meta.env.PUBLIC_ALLOW_INDEXING === 'true' &&
    site &&
    !['localhost', '127.0.0.1'].includes(site.hostname);
  return new Response(
    allowed
      ? `User-agent: *\nAllow: /\nSitemap: ${new URL('/sitemap.xml', site)}\n`
      : 'User-agent: *\nDisallow: /\n',
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
  );
};
