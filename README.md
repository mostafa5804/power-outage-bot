<div dir="rtl" align="center">

# 🤖 ربات اطلاع‌رسانی قطعی برق 🤖

<p>
  <a href="https://github.com/YourUsername/YourRepo/actions/workflows/run-bot.yml">
    <img src="https://github.com/YourUsername/YourRepo/actions/workflows/run-bot.yml/badge.svg" alt="GitHub Actions Status" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/Library-Selenium-green.svg" alt="Library" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
</p>

</div>

---

<div dir="rtl">

این یک ربات پایتون است که به صورت روزانه برنامه قطعی برق را از وب‌سایت توزیع برق مازندران استخراج کرده و اطلاعات مربوط به مناطق مشخص شده را پس از فیلتر و خلاصه‌سازی، به یک گروه یا کانال تلگرام ارسال می‌کند.

## ✨ ویژگی‌ها

* استخراج اطلاعات از وب‌سایت‌های داینامیک (ASP.NET) با استفاده از Selenium.
* قابلیت فیلتر کردن نتایج بر اساس کلمات کلیدی مشخص در آدرس.
* جایگزینی آدرس‌های طولانی با نام‌های مستعار دلخواه برای خوانایی بیشتر.
* ارسال پیام‌های فرمت‌بندی شده و زیبا به تلگرام.
* اجرای کاملاً خودکار و روزانه با استفاده از **GitHub Actions**.

## ⚙️ راه‌اندازی و پیکربندی

برای اجرای این ربات، مراحل زیر نیاز است:

#### ۱. تنظیمات کد

در فایل `bot.py`، بخش تنظیمات را با اطلاعات دلخواه خود ویرایش کنید:
```python
# --- دیکشنری نام‌های مستعار (تنها منبع اطلاعات) ---
ADDRESS_ALIASES = {
    
}
