# وضعیت تبدیل DENTYAR به نسخه آنلاین چندکاربره

### آنچه در نسخه فعلی وجود دارد
- منبع داده فعلی: localStorage
- IndexedDB: فقط آینه غیرهمزمان
- هیچ Firebase/Firestore/Supabase/REST backend در پروژه وجود ندارد.
- هیچ API key یا projectId ابری در سورس فعلی وجود ندارد.

### نتیجه فنی
برای استفاده همزمان 2 تا 3 نفر روی چند دستگاه، یک Backend/Cloud Database ضروری است. «بدون خرید یا مدیریت سرور» شدنی است؛ «بدون هیچ سرویس سمت سرور» برای داده مشترک چندکاربره شدنی نیست.

### مسیر پیشنهادی
Firebase Authentication + Cloud Firestore، با حفظ local cache برای حالت آفلاین.

UI فعلی نباید بازطراحی شود. تغییرات باید فقط در لایه‌های زیر انجام شود:
1. Authentication
2. Cloud data adapter
3. Sync queue / conflict handling
4. Local cache
5. Backup/export

تا زمانی که پروژه ابری متعلق به مالک سامانه ایجاد و تنظیمات آن در اختیار توسعه قرار نگیرد، فعال‌کردن واقعی این بخش امکان‌پذیر نیست.
