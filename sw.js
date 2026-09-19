const CACHE_NAME='dentyar-v32-pwa';
const APP_SHELL=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png','./icon-192-maskable.png','./icon-512-maskable.png'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(APP_SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('dentyar-')&&k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('message',event=>{if(event.data&&event.data.type==='SKIP_WAITING') self.skipWaiting();});
/* استراتژی network-first برای index.html: همیشه ابتدا نسخه‌ی تازه از سرور خواسته می‌شود تا
   بعد از هر بروزرسانی (مثلاً آپلود مجدد در Netlify)، کاربر بلافاصله نسخه‌ی جدید را ببیند؛
   فقط وقتی اتصال اینترنت قطع باشد، نسخه‌ی کش‌شده به‌عنوان پشتیبان استفاده می‌شود. */
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  const isNavigationOrHtml = event.request.mode==='navigate' || event.request.url.endsWith('index.html') || event.request.url.endsWith('/');
  if(isNavigationOrHtml){
    event.respondWith(
      fetch(event.request).then(response=>{
        if(response && response.ok){ const copy=response.clone(); caches.open(CACHE_NAME).then(c=>c.put(event.request,copy)); }
        return response;
      }).catch(()=> caches.match(event.request).then(cached=>cached||caches.match('./index.html')))
    );
    return;
  }
  event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request).then(response=>{if(response&&response.ok&&new URL(event.request.url).origin===self.location.origin){const copy=response.clone();caches.open(CACHE_NAME).then(c=>c.put(event.request,copy));}return response;}).catch(()=>caches.match('./index.html'))));
});
