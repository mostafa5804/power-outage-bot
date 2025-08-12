import os
import time
import requests
import datetime
from persiantools.jdatetime import JalaliDate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# --- تنظیمات ---
URL = "https://khamooshi.maztozi.ir/"
CITY_VALUE = "990090345"
AREA_VALUE = "64"
HEADLESS = True

ADDRESS_ALIASES = {
    "خیابان ام آر ای": "خونه - خیابان mri",
    "ضلع شمالي کمربندي اميرکلا": "باغ - مقریکلا",
    "شهرک بهزاد": "خونه مائده - فارابی"
}
STREETS_TO_FILTER = list(ADDRESS_ALIASES.keys())

# خواندن اطلاعات از Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
# -----------------

def send_to_telegram(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        requests.post(api_url, json=payload)
    except Exception as e:
        print(f"❌ خطای اتصال به تلگرام: {e}")

def main():
    today_jalali = JalaliDate(datetime.date.today()).strftime("%Y/%m/%d")
    print(f"تاریخ جستجو (امروز): {today_jalali}")

    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # --- این خط کد، مشکل را حل می‌کند ---
    # آدرس صحیح مرورگر را به اسکریپت می‌دهیم
    options.binary_location = "/usr/bin/chromium-browser"
    # -----------------------------------
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # راه‌اندازی درایور بدون نیاز به Service یا Manager
    driver = webdriver.Chrome(options=options)
    
    wait = WebDriverWait(driver, 25)
    final_message = ""
    try:
        print("1. باز کردن سایت...")
        driver.get(URL)
        for attempt in range(3):
            try:
                if attempt > 0: print(f"--- تلاش مجدد شماره {attempt + 1} ---")
                wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_rbIsAddress"))).click()
                Select(wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlCity")))).select_by_value(CITY_VALUE)
                wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_ddlArea")))
                Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlArea")).select_by_value(AREA_VALUE)
                date_from = driver.find_element(By.ID, "ContentPlaceHolder1_txtPDateFrom")
                driver.execute_script("arguments[0].value = arguments[1];", date_from, today_jalali)
                wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnSearchOutage"))).click()
                break
            except StaleElementReferenceException:
                if attempt == 2: raise
                print(f"خطای Stale، تلاش مجدد...")
                time.sleep(2)
        print("... در حال جستجو و تحلیل نتایج ...")
        table = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdOutages")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        if len(rows) <= 1:
            final_message = f"💡 در تاریخ {today_jalali} خاموشی‌ای برای مناطق شما ثبت نشده است."
        else:
            all_data = [[c.text.strip() for c in r.find_elements(By.TAG_NAME, "td")] for r in rows[1:]]
            filtered_data = [row for row in all_data if any(normalize_text(street) in normalize_text(row[-1]) for street in STREETS_TO_FILTER)]
            if not filtered_data:
                final_message = f"✅ خاموشی‌ها برای {today_jalali} بررسی شد، اما موردی برای خیابان‌های شما یافت نشد."
            else:
                message_parts = [f"🚨 *برنامه قطعی برق برای مناطق شما* 🚨\n"]
                for row in filtered_data:
                    address_column = row[4]
                    display_address = next((alias for keyword, alias in ADDRESS_ALIASES.items() if normalize_text(keyword) in normalize_text(address_column)), address_column)
                    part = (f"🗓️ *تاریخ:* {row[0]}\n⏰ *از ساعت:* {row[1]} *تا ساعت:* {row[2]}\n📍 *مکان:* {display_address}\n---------------------------------------\n")
                    message_parts.append(part)
                final_message = "\n".join(message_parts)
                print("\n--- پیام نهایی آماده ارسال ---\n" + final_message)
    except TimeoutException:
        final_message = f"✅ در تاریخ {today_jalali} هیچ جدول خاموشی‌ای یافت نشد."
    except Exception as e:
        final_message = f"❌ یک خطای غیرمنتظره در ربات رخ داد: {e}"
    finally:
        if final_message:
            send_to_telegram(final_message)
        driver.quit()
        print("\n🚀 کار ربات تمام شد.")

def normalize_text(text):
    return text.replace('ي', 'ی').replace('ك', 'ک').strip()

if __name__ == "__main__":
    main()
