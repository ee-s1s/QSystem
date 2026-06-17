from django.db import models
from django.contrib.auth.models import User

# --- 1. إعدادات النظام العامة ---
class SystemSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Q-System", verbose_name="اسم النظام")
    logo = models.ImageField(upload_to='settings/', null=True, blank=True, verbose_name="اللوجو")
    primary_color = models.CharField(max_length=7, default="#2C3E50", verbose_name="اللون الأساسي")
    secondary_color = models.CharField(max_length=7, default="#D35400", verbose_name="اللون الثانوي")
    background_image = models.ImageField(upload_to='settings/', null=True, blank=True, verbose_name="صورة الخلفية")
    announcement_text = models.TextField(max_length=1000, blank=True, verbose_name="نص الشريط (استخدم [time] للوقت و [date] للتاريخ)")

    enable_voice_alert = models.BooleanField(default=True, verbose_name="تفعيل التنبيه الصوتي")
    last_reset_date = models.DateField(auto_now=True)

    def get_formatted_text(self):
        text = self.announcement_text
        text = text.replace("[time]", timezone.now().strftime("%I:%M %p"))
        text = text.replace("[date]", timezone.now().strftime("%Y/%m/%d"))
        return text

    class Meta:
        verbose_name = "إعدادات النظام"
        verbose_name_plural = "إعدادات النظام"

    def __str__(self):
        return self.site_name

# --- 2. الخدمات ---
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الخدمة")
    prefix = models.CharField(max_length=2, verbose_name="حرف التذكرة (مثل A)")
    avg_service_time = models.PositiveIntegerField(default=5, verbose_name="متوسط وقت الخدمة (دقائق)")
    is_active = models.BooleanField(default=True, verbose_name="نشطة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الخدمة")

    class Meta:
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"

    def __str__(self):
        return f"{self.name} ({self.prefix})"

# --- 3. الشبابيك (Counters) ---
class Counter(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="رقم الشباك")
    services = models.ManyToManyField(Service, related_name='counters', verbose_name="الخدمات التي يقدمها")
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الموظف")
    is_active = models.BooleanField(default=True, verbose_name="يعمل حالياً")


    def __str__(self):
        return f"شباك رقم {self.number}"

    class Meta:
        verbose_name = "شباك"
        verbose_name_plural = "الشبابيك"

# --- 4. التذاكر ---
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'في الانتظار'),
        ('calling', 'جاري النداء'),
        ('serving', 'قيد الخدمة'),
        ('completed', 'مكتملة'),
        ('skipped', 'تم التخطي'),
    ]

    number = models.PositiveIntegerField(verbose_name="رقم التذكرة")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="الخدمة")
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الشباك المستدعي")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name="الحالة")
    
    # التوقيتات
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت قطع التذكرة")
    called_at = models.DateTimeField(null=True, blank=True, verbose_name="وقت النداء")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="وقت بدء الخدمة")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="وقت الانتهاء")

    class Meta:
        ordering = ['created_at']
        verbose_name = "تذكرة"
        verbose_name_plural = "التذاكر"

    def __str__(self):
        return f"{self.service.prefix}-{self.number}"

    @property
    def ticket_code(self):
        return f"{self.service.prefix}{self.number:03d}"

    @property
    def wait_time(self):
        if self.called_at:
            delta = self.called_at - self.created_at
            return int(delta.total_seconds() / 60)
        return None

# --- 5. الإعلانات ---
class DisplayAd(models.Model):
    title = models.CharField(max_length=100, verbose_name="العنوان")
    media = models.FileField(upload_to='ads/', verbose_name="فيديو أو صورة")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "إعلان"
        verbose_name_plural = "الإعلانات"

    def __str__(self):
        return self.title

