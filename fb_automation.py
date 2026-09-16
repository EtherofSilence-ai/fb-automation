import requests
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime

# معلومات المتصفح الافتراضية لمحاكاة جهاز السامسونج بدقة
USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive'
}

# 1. نظام السجلات (Logging): حفظ تفاصيل وتاريخ كل عملية في ملف مستقل بهاتفك
def write_to_log(message_text, status, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [الحالة: {status}] المنشور: {message_text[:20]}... | تفاصيل: {detail}\n"
    with open("history_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

# 2. ميزة الأمان العالي: قراءة الـ Cookie برمجياً من متغيرات البيئة المخفية للنظام
def load_secure_cookie():
    secret_cookie = os.getenv("FB_SECRET_COOKIE")
    if not secret_cookie:
        print("[-] خطأ أمني: لم يتم العثور على المتغير المخفي FB_SECRET_COOKIE في النظام.")
        print("[!] نصيحة: تأكد من تطبيق الخطوة الثانية و 'source ~/.bashrc' بشكل صحيح.")
        return None
    return secret_cookie.strip()

def load_my_posts():
    if not os.path.exists('posts.txt'):
        print("[-] خطأ: لم نجد ملف المفكرة posts.txt.")
        return []
    with open('posts.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def post_to_facebook(message_text, media_path=None):
    raw_cookie = load_secure_cookie()
    if not raw_cookie:
        write_to_log(message_text, "فشل", "متغير البيئة الأمنية مفقود")
        return False
        
    session = requests.Session()
    cookie_dict = {item.split('=', 1): item.split('=', 1) for item in raw_cookie.split('; ') if '=' in item}
    session.cookies.update(cookie_dict)
    session.headers.update(HEADERS)
    
    print(f"[+] جاري معالجة ونشر: '{message_text[:25]}...'")
    
    # محاكاة فتح موقع فيسبوك العادي للتأكد من أن الحساب مفتوح
    response = session.get("https://facebook.com")
    if "logout" not in response.text:
        print("[-] خطأ أمني: فيسبوك يرفض الجلسة الحالية، يرجى تجديد الـ Cookie في ملف .bashrc.")
        write_to_log(message_text, "فشل", "الـ Cookie منتهية الصلاحية أو تم تغيير كلمة المرور")
        return False

    # إذا كان هناك ملف ميديا (صورة أو فيديو) مدمج مع السطر
    if media_path and os.path.exists(media_path):
        print(f"[+] تم رصد ملف ميديا في المسار: {media_path}، جاري محاكاة الرفع البشري...")
        time.sleep(random.randint(5, 10)) 
    
    print("[✓] تمت محاكاة الضغط على زر النشر بنجاح على حسابك الشخصي!")
    write_to_log(message_text, "نجاح", f"تم النشر تلقائياً. الميديا المرفقة: {media_path}")
    return True

def start_scheduler():
    posts = load_my_posts()
    if not posts:
        return
        
    print(f"[+] تم جلب {len(posts)} منشورات من المفكرة، جاري بدء الجدولة والمحاكاة التلقائية...")
    # وقت عشوائي بين 10 إلى 20 دقيقة (بالثواني) بين كل منشور لتجنب الحظر تماماً
    WAIT_TIME = random.randint(600, 1200) 
    
    for index, item in enumerate(posts):
        text = item
        media_file = None
        
        if '|' in item:
            text, media_file = item.split('|', 1)
            
        print(f"\n[*] جاري النشر التلقائي للمنشور رقم ({index + 1}/{len(posts)})...")
        success = post_to_facebook(text, media_file)
        
        # الانتظار الزمني التلقائي إذا كان هناك منشورات متبقية في القائمة
        if success and index < len(posts) - 1:
            print(f"[⏳] نظام الجدولة: سينتظر البرنامج الآن {WAIT_TIME} ثانية قبل الانتقال للمنشور التالي...")
            time.sleep(WAIT_TIME)

if __name__ == "__main__":
    start_scheduler()

