# 🚀 نظام إدارة الطوابير والانتظار الرقمي الذكي

### 🌟 Smart Queue Management System (SQMS)

نظام رقمي ذكي ومتكامل لإدارة صفوف الانتظار وسحب التذاكر، مصمم بهندسة برمجية تدعم **تعدد الشركات والفروع (Multi-Company & Multi-Branch)**. يتميز بالنطق الصوتي التلقائي والتحديث اللحظي للشاشات لتقديم تجربة مستخدم فائقة السلاسة.

---

## ✨ أبرز المميزات الذكية (Core Features)

* **🎨 هوية بصرية ديناميكية:** واجهات عصرية بتأثير الـ **Glassmorphism** تتغير ألوانها وشعاراتها تلقائياً بناءً على ألوان الشركة المستضيفة المحددة في قاعدة البيانات.
* **⚡ كشك سحب تذاكر ذكي (Interactive Kiosk):** يعمل بنظام الخطوات المتتالية (Steps) السريعة لملائمة شاشات اللمس، مع محاكاة حية لطابعة التذاكر تختفي تلقائياً بعد 4 ثوانٍ.
* **📺 شاشة عرض مرنة (Dynamic TV Display):** شاشة منقسمة للإعلانات وقائمة التذاكر. في حال عدم وجود إعلانات نشطة، تتمدد شاشة الأرقام تلقائياً لتأخذ المساحة الكاملة (`col-md-12`) ويتم الفحص ذكياً كل 3 ثوانٍ عبر تقنية `DOMParser` بدون إعادة تحميل الصفحة.
* **🗣️ نداء صوتي ذكي (AI Voice Call):** ينطق النظام التذاكر المستدعاة فوراً باللغة العربية الفصحى بصوت هادئ ومفهوم بالاعتماد على الـ `Web Speech API`.
* **📜 شريط تنويهات معزز بـ (GPU):** شريط سفلي متحرك (Marquee) يعتمد بالكامل على معالجة كرت الشاشة لضمان سلاسة الحركة، ويقوم باستبدال ذكي للأكواد مثل `[time]` و `[date]` بالوقت والتاريخ الفعليين.

---

## 🏗️ البنية البرمجية ونظام البيانات (Database Architecture)

يحتوي النظام على 5 موديلات أساسية مترابطة بشكل وثيق لمنع أي تكرار أو أخطاء في البيانات:

| الموديل (Model) | الوظيفة الأساسية (Responsibility) |
| --- | --- |
| **`Company`** | إدارة الشركات، اللوجوهات، والألوان الهوية الأساسية والثانوية. |
| **`Branch`** | الفروع التابعة لكل شركة مع ربطها ديناميكياً بجدول الشركة. |
| **`Service`** | الخدمات المتاحة داخل الفرع (تضم الحرف المميز مثل `A, B` وعداد الأرقام). |
| **`Ticket`** | النواة الأساسية؛ تولد المعرف (`A-101`) تلقائياً عبر دالة `save()` وتدير حالات التذكرة. |
| **`Counter`** | لوحة تحكم الشبابيك والموظفين لتحديد الخدمة المربوطة وحالة الانشغال `is_busy`. |

---

## 📂 هيكل المجلدات الرئيسي (Project Tree)

```text
📁 QS/                     # مجلد إعدادات المشروع الرئيسي
📁 QSapp1/                 # تطبيق إدارة الطوابير الذكي (الأكواد والمنطق)
 ├── 📁 migrations/       # ملفات هجرة وتحديثات قاعدة البيانات
 ├── 📄 admin.py          # لوحة تحكم الإدارة وسجلات النظام
 ├── 📄 models.py         # بنية قاعدة البيانات (Company, Ticket, Counter...)
 ├── 📄 views.py          # منطق السيرفر والـ Fetch APIs
 └── 📄 urls.py           # مسارات التطبيق الذكية
📁 templates/              # قوالب العرض الأمامية (UI/UX)
 ├── 📄 base.html         # القالب الأساسي (Glassmorphism + GPU Marquee)
 ├── 📄 kiosk.html        # واجهة الكشك التفاعلية
 ├── 📄 display.html      # شاشة العرض الكبيرة (النداء الصوتي + DOMParser)
 ├── 📄 ticket.html       # قالب محاكاة طباعة التذكرة
 └── 📄 counter.html      # لوحة تحكم موظف الشباك
📄 manage.py               # أداة التحكم والتنفيذ الخاصة بـ Django
📄 requirements.txt        # المكتبات والاعتمادات اللازمة للتشغيل

```

---

## 🚀 طريقة التثبيت والتشغيل المحلي (Setup & Installation)

تأكد من تثبيت **Python 3.10+** على جهازك، ثم اتبع الخطوات التالية:

1. **استنساخ المشروع (Clone the Repository):**
```bash

```



git clone https://github.com/your-username/smart-queue-system.git
cd smart-queue-system

```

2. **إنشاء وتفعيل البيئة الافتراضية (Virtual Environment):**
   ```bash
python -m venv venv
# لنظام ويندوز:
venv\Scripts\activate
# لنظام ماك / لينكس:
source venv/bin/activate

```

3. **تثبيت المكتبات الاعتمادية (Install Dependencies):**
```bash

```



pip install -r requirements.txt

```

4. **تجهيز قاعدة البيانات (Database Migrations):**
   ```bash
python manage.py makemigrations
python manage.py migrate

```

5. **إنشاء حساب المسؤول/الآدمن (Superuser):**
```bash

```



python manage.py createsuperuser

```

6. **إطلاق السيرفر (Run Server):**
   ```bash
python manage.py runserver

```

> 🌐 افتح المتصفح وتوجه إلى الرابط: `[http://127.0.0.1:8000](http://127.0.0.1:8000)`

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

* **Backend:** Python, Django Framework (جلسات مخصصة ودوال حفظ أوتوماتيكية).
* **Frontend:** Bootstrap 5, Custom CSS3 (Glassmorphism Effects).
* **Asynchronous Logic:** JavaScript (Fetch API, DOMParser, Web Speech API).
* **Database:** SQLite (يمكن ترقيتها بسهولة إلى PostgreSQL أو MySQL).

---

## 📜 رخصة المشروع (License)

هذا المشروع مرخص بموجب رخصة **MIT** - راجع ملف [LICENSE](https://www.google.com/search?q=LICENSE) لمعرفة التفاصيل.
