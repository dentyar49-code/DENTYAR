# DENTYAR — پروژه چندسکویی V23

این بسته، هسته وب DENTYAR V22 را برای بسته‌بندی چندسکویی آماده می‌کند.

## خروجی‌ها
- Android: APK / AAB با Capacitor
- iOS/iPadOS: پروژه Xcode
- Windows/macOS/Linux: می‌توان در مرحله بعد با پوسته دسکتاپ مناسب بسته‌بندی کرد.
- Web/PWA: پوشه `www`

## نکته
این بسته «سورس آماده ساخت» است؛ APK/EXE/IPA باینری داخل آن نیست، چون ساخت نهایی هر سیستم‌عامل به ابزار رسمی همان پلتفرم نیاز دارد.

## Android
روی Windows/macOS/Linux:
1. Node.js LTS و Android Studio نصب شود.
2. در ریشه پروژه:
   `npm install`
3. سپس:
   `npx cap add android`
   `npx cap sync android`
4. برای APK:
   `cd android`
   `gradlew assembleDebug`
5. فایل APK در `android/app/build/outputs/apk/debug/` ایجاد می‌شود.

## iOS
نیازمند macOS + Xcode و حساب/گواهی‌های اپل است:
`npx cap add ios`
`npx cap sync ios`

## نکته مهم داده‌ها
DENTYAR از ذخیره‌سازی محلی استفاده می‌کند. قبل از هر بروزرسانی نسخه، بکاپ داخل خود برنامه توصیه می‌شود.
