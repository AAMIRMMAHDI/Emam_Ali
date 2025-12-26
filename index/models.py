from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_summernote.fields import SummernoteTextField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون (مثلاً 📐)")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام نویسنده")
    bio = models.TextField(verbose_name="بیوگرافی نویسنده")
    avatar = models.ImageField(upload_to='authors/', verbose_name="تصویر پروفایل نویسنده")

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=350, unique=True, blank=True, verbose_name="اسلاگ")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نویسنده")
    content = SummernoteTextField(verbose_name="محتوای مقاله")
    featured_image = models.ImageField(upload_to='articles/', verbose_name="تصویر اصلی مقاله")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    reading_time = models.PositiveIntegerField(default=5, verbose_name="زمان خواندن (دقیقه)")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    tags = models.CharField(max_length=500, blank=True, verbose_name="تگ‌ها")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            num = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان دوره")
    slug = models.SlugField(max_length=350, unique=True, blank=True, verbose_name="اسلاگ")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    description = SummernoteTextField(verbose_name="توضیحات دوره")
    image = models.ImageField(upload_to='courses/', verbose_name="تصویر دوره")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    duration = models.CharField(max_length=100, verbose_name="مدت زمان")
    features = models.TextField(verbose_name="ویژگی‌ها (هر خط یکی)")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "دوره آموزشی"
        verbose_name_plural = "دوره‌های آموزشی"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            num = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان اطلاعیه")
    description = SummernoteTextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='announcements/', verbose_name="تصویر")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    features = models.TextField(verbose_name="ویژگی‌ها (هر خط یکی)")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "اطلاعیه دوره"
        verbose_name_plural = "اطلاعیه‌های دوره"

    def feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    role = models.CharField(max_length=100, verbose_name="سمت/دوره")
    text = models.TextField(verbose_name="متن نظر")
    avatar = models.ImageField(upload_to='testimonials/', verbose_name="تصویر")
    date = models.DateField(verbose_name="تاریخ")

    class Meta:
        ordering = ['-date']
        verbose_name = "نظر کاربر"
        verbose_name_plural = "نظرات کاربران"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class AboutStat(models.Model):
    years_experience = models.PositiveIntegerField(default=25, verbose_name="سال‌های تجربه")
    graduates = models.PositiveIntegerField(default=5000, verbose_name="دانش‌آموزان فارغ‌التحصیل")
    courses = models.PositiveIntegerField(default=50, verbose_name="دوره‌های آموزشی")
    teachers = models.PositiveIntegerField(default=30, verbose_name="اساتید مجرب")

    class Meta:
        verbose_name = "آمار درباره ما"
        verbose_name_plural = "آمارهای درباره ما"

    def __str__(self):
        return "آمار درباره ما"


class AboutContent(models.Model):
    title = models.CharField(max_length=300, default="درباره ما", verbose_name="عنوان صفحه")
    text = SummernoteTextField(verbose_name="متن درباره ما")
    image = models.ImageField(upload_to='about/', verbose_name="تصویر درباره ما", blank=True, null=True)

    class Meta:
        verbose_name = "محتوای درباره ما"
        verbose_name_plural = "محتواهای درباره ما"

    def __str__(self):
        return self.title