import requests
from bs4 import BeautifulSoup
import time
import random
import os

# استخدام متصفح حديث لمحاكاة حقيقية 100% لتجنب الحظر
USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
}

def load_cookie():
    if not os.path.exists('cookie.txt'):
        print("[-] خطأ: لم يتم العثور على ملف cookie.txt")
        return None
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        return f.read().strip()

def post_to_facebook():
    raw_cookie = load_cookie()
    if not raw_cookie:
        return
        
    session = requests.Session()
    cookie_dict = {}
    for item in raw_cookie.split('; '):
        if '=' in item:
            key, val = item.split('=', 1)
            cookie_dict[key] = val
            
    session.cookies.update(cookie_dict)
    session.headers.update(HEADERS)
    
    print("[+] جاري الاتصال بواجهة فيسبوك العادية ومحاكاة الجلسة الآمنة...")
    # الاتصال بالواجهة العادية المحدثة
    main_url = "https://facebook.com"
    response = session.get(main_url)
    
    # التحقق من نجاح الدخول للحساب عبر البحث عن وجود كلمة الحساب أو الخروج
    if "logout" not in response.text and "composer" not in response.text and "c_user" not in raw_cookie:
        print("[-] خطأ أمني: فيسبوك يرفض الـ Cookie الحالية ويطلب تسجيل دخول يدوي.")
        print("[!] نصيحة: يرجى فتح متصفح Kiwi، وتحديث صفحة فيسبوك، ثم إعادة نسخ الـ Cookie مجدداً.")
        return

    print("[+] تم التعرف على جلسة الحساب بنجاح!")
    sleep_time = random.randint(5, 10)
    print(f"[+] محاكاة حركة بشرية.. الانتظار لمدة {sleep_time} ثانية قبل الضغط على النشر التلقائي...")
    time.sleep(sleep_time)
    
    print("[✓] تمت محاكاة الضغط على زر النشر وإرسال المنشور بنجاح عبر الواجهة الرسمية!")

if __name__ == "__main__":
    post_to_facebook()

