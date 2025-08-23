# نظام حجوزات مجموعات الدروس (Django + DRF)

مشروع بسيط يتيح للطلاب تسجيل بياناتهم، استعراض المجموعات المتاحة، والحجز فيها تلقائيًا طالما السعة لم تكتمل. المدرّس/الأدمن يقدر يضيف مجموعات جديدة، يحدد مواعيدها وسعتها، ويراقب الحجوزات. كل ده من خلال API يمكن اختبارها على Postman، بدون الحاجة لتطبيق موبايل.

---

## ✨ المزايا الرئيسية

* تسجيل الطلاب وإدارة بياناتهم.
* إنشاء مجموعات بمسمّى ثابت، يوم/موعد أسبوعي، وسعة محددة.
* الحجز الذاتي: الطالب يحجز لنفسه إذا كان هناك أماكن شاغرة.
* قفل المجموعة تلقائيًا عند اكتمال السعة.
* لوحة إدارة Django Admin لمراجعة الكيانات.
* REST API كاملة يمكن تجربتها عبر Postman.

---

## 🧱 بنية المشروع (Apps)

* `users/` — CRUD بسيط للمستخدمين (اختياري للتجارب).
* `students/` — بيانات الطلاب.
* `groups/` — بيانات المجموعات (الاسم، السعة، المواعيد، الأيام، والطلاب المرتبطين).
* `bookings/` — حجز الطالب في مجموعة (مع قواعد منع التكرار واحترام السعة).

قاعدة البيانات الافتراضية: **SQLite** (ملف `db.sqlite3`).

---

## 🚀 التشغيل المحلي

> الأوامر التالية تعمل على Windows / macOS / Linux

1. **تفعيل بيئة عمل افتراضية (اختياري لكن مستحب):**

```bash
# إنشاء بيئة
python -m venv venv

# تفعيلها
# Windows PowerShell
venv\Scripts\Activate.ps1
# أو CMD
venv\Scripts\activate.bat
# macOS/Linux
source venv/bin/activate
```

2. **تنصيب الاعتمادات (packages):**

> لو عندك `requirements.txt`:

```bash
pip install -r requirements.txt
```

> وإلا ثبّت الأساسيات (كمثال):

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

3. **تجهيز قاعدة البيانات:**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **إنشاء مستخدم أدمن للـ Admin (اختياري):**

```bash
python manage.py createsuperuser
```

5. **تشغيل السيرفر:**

```bash
python manage.py runserver
```

> سيفتح على: `http://127.0.0.1:8000/`

---

## 🔐 الصلاحيات (Permissions) أثناء التطوير

للتجارب السريعة على Postman، يمكنك جعل الـ API مفتوحة مؤقتًا بوضع التالي في `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
```

لاحقًا للإنتاج، بدّل `AllowAny` بـ `IsAuthenticated`، واستخدم JWT (`djangorestframework-simplejwt`).

### تمكين JWT (اختياري):

```python
INSTALLED_APPS += [
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

Endpoints JWT:

* `POST /api/token/`  (ترجع access/refresh)
* `POST /api/token/refresh/`

ضع في Postman Header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 🧩 الموديلات (مختصر)

* **Student** (`students/models.py`):

  * `full_name`, `email` (Unique CI), `phone` (Unique), `stage` (سادس/إعدادي), إلخ.
* **Group** (`groups/models.py`):

  * `name` (Unique), `capacity`, `schedule`, `days`, وعلاقة `ManyToMany` مع `Student` عبر الحقول `students`.
* **Booking** (`bookings/models.py`):

  * `student` ⇄ `group` + `created_at`.
  * `unique_together = (student, group)` لمنع الحجز المكرر.
  * عبر **signals**: عند إنشاء Booking جديد يُضاف الطالب تلقائيًا إلى `group.students`.
  * **التحقق من السعة** قبل الحجز (لا حجز إذا اكتملت المجموعة).

---

## 🌐 نقاط النهاية (Endpoints)

> المسارات أدناه تفترض أن `backend/urls.py` يضم:
>
> ```py
> path('api/students/', include('students.urls', namespace='students'))
> path('api/groups/',   include('groups.urls',   namespace='groups'))
> path('api/bookings/', include('bookings.urls', namespace='bookings'))
> ```

### 👨‍🎓 Students

* **GET** `/api/students/` — قائمة الطلاب
* **POST** `/api/students/create/` — إنشاء طالب جديد
* **GET/PUT/DELETE** `/api/students/<id>/` — قراءة/تحديث/حذف طالب

**مثال إنشاء (Postman / cURL):**

```bash
curl -X POST http://127.0.0.1:8000/api/students/create/ \
 -H "Content-Type: application/json" \
 -d '{
       "full_name": "Mohamed Ali",
       "email": "mohamed@example.com",
       "phone": "01012345678",
       "stage": "PREP"
     }'
```

### 👥 Groups

* **GET/POST** `/api/groups/` — عرض/إنشاء مجموعة
* **GET/PUT/DELETE** `/api/groups/<id>/` — تفاصيل/تعديل/حذف
* **POST** `/api/groups/<id>/add-students/` — (اختياري) إضافة طلاب مباشرة

**ملاحظات:**

* الحجز الصحيح يمر عبر `bookings/`؛ إضافة الطلاب مباشرة للمجموعة يفضل أن تكون قراءة فقط في الإنتاج.

### 🧾 Bookings

* **GET/POST** `/api/bookings/` — عرض الحجوزات / إنشاء حجز
* **GET/DELETE** `/api/bookings/<id>/` — تفاصيل/إلغاء حجز

**مثال إنشاء حجز:**

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
 -H "Content-Type: application/json" \
 -d '{
       "student": 1,
       "group": 2
     }'
```

النتيجة المتوقعة:

* لو المجموعة ممتلئة → **400** مع رسالة خطأ مناسبة.
* لو نفس الطالب حجز قبل كده في نفس المجموعة → **400** (فشل بسبب `unique_together`).
* عند نجاح الحجز → يُضاف الطالب تلقائيًا إلى `group.students`.

---

## 🧪 الاختبارات (Tests)

تشغيل اختبارات **bookings** فقط:

```bash
python manage.py test bookings
```

محتوى نموذجي في `bookings/tests.py` يشمل:

* نجاح الحجز وإضافة الطالب للجروب.
* منع الحجز المكرر لنفس الطالب.
* منع الحجز بعد اكتمال السعة.

---

## 🛠️ إدارة عبر الـ Admin

* ادخل إلى: `http://127.0.0.1:8000/admin/`
* راجع/أنشئ `Students`، `Groups`، وراقب `Bookings`.
* يفضّل جعل حقل `students` في `GroupAdmin` **قراءة فقط** والاعتماد على الحجوزات لإضافة الطلاب.

---

## 🧯 استكشاف الأخطاء الشائعة

* **`ModuleNotFoundError: No module named 'django'`**

  * لم يتم تثبيت الحزم داخل الـ venv.
  * الحل: فعّل البيئة ثم `pip install django djangorestframework`.

* **`ImproperlyConfigured: namespace ... without app_name`**

  * استخدمت `include(..., namespace="bookings")` بدون `app_name` داخل `bookings/urls.py`.
  * الحل: أضف أعلى الملف: `app_name = "bookings"`.

* **`403 Forbidden` أو `Authentication credentials were not provided.`**

  * الـ permissions تتطلب مصادقة.
  * الحل: أثناء التطوير استخدم `AllowAny` في `settings.py` أو أضف `@permission_classes([AllowAny])` على الـ views.

* **مشكلة CRLF/LF في Git** (تحذير فقط):

  * أضف `.gitattributes` لضبط الترميز أو تجاهل التحذير.

---

## 🌱 خطوات تجربة سريعة (Postman)

1. **أنشئ طالب** عبر `POST /api/students/create/`.
2. **أنشئ مجموعة** عبر `POST /api/groups/` (مثال: سعة 10، أيام: "سبت، تلات").
3. **احجز** عبر `POST /api/bookings/` بإرسال `student` و `group`.
4. جرّب تحجز لنفس الطالب مرة ثانية في نفس المجموعة → يجب أن تفشل.
5. املأ المجموعة لحد الـ capacity ثم جرّب حجز طالب جديد → يجب أن تفشل.

---

## 🔀 Git (اختياري)

إنشاء فرع للميزة:

```bash
git checkout -b feature/bookings
# بعد التعديلات
git add -A
git commit -m "Add bookings app"
git push -u origin feature/bookings
```

---

## 📄 رخصة

مشروع تعليمي/عملي بسيط — يمكن التصرّف فيه بحرية داخل نطاق الاستخدام الشخصي أو التعليمي.

---

## ❓دعم

لو حابة نزود واجهة ويب بسيطة (Templates) للطلاب عشان يحجزوا من لينك مباشر بدل Postman، قوليلي وهنضيف صفحات جاهزة للعرض والحجز. 💙
