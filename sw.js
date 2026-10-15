// Thali offline cache: serves the app and food database from the phone, refreshes them in the background when online.
const CACHE = 'thali-v1-3-1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-192.png', './icon-512.png',
  './data/db-version.json', './data/foods-thali.json', './data/foods-indb.json', './data/foods-usda.json',
  './lib/zxing-reader.js', './lib/zxing_reader.wasm'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  const fresh = e.request.cache === 'no-store';
  const net = () => fetch(e.request, fresh ? { cache: 'no-store' } : undefined).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(new URL(e.request.url).pathname, copy)); }
    return res;
  });
  if (fresh) { e.respondWith(net().catch(() => caches.match(e.request, { ignoreSearch: true }))); return; }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => {
    const n = net().catch(() => hit);
    return hit || n;
  }));
});
