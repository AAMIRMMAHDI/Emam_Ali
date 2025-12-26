# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی آزمون")
    has_taken_exam = models.BooleanField(default=False, verbose_name="آزمون داده شده؟")
    score = models.IntegerField(default=0, verbose_name="نمره از ۲۰۰")

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="نام دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions', verbose_name="دسته‌بندی")
    text = models.TextField(verbose_name="متن سوال")
    option_a = models.CharField(max_length=300, verbose_name="گزینه الف")
    option_b = models.CharField(max_length=300, verbose_name="گزینه ب")
    option_c = models.CharField(max_length=300, verbose_name="گزینه ج")
    option_d = models.CharField(max_length=300, verbose_name="گزینه د")
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'الف'), ('B', 'ب'), ('C', 'ج'), ('D', 'د')],
        verbose_name="گزینه صحیح"
    )

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"

    def __str__(self):
        return f"{self.category} - {self.text[:50]}"


class ExamResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    correct_answers = models.IntegerField(verbose_name="پاسخ‌های صحیح")
    total_questions = models.IntegerField(verbose_name="تعداد کل سوالات")
    percentage = models.FloatField(verbose_name="درصد")
    score_200 = models.IntegerField(verbose_name="نمره از ۲۰۰")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        verbose_name = "نتیجه آزمون"
        verbose_name_plural = "نتایج آزمون"

    def __str__(self):
        return f"نتیجه {self.user} - نمره: {self.score_200}"