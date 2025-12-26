# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Question, ExamResult


class ExamResultInline(admin.StackedInline):
    model = ExamResult
    can_delete = False
    readonly_fields = ('correct_answers', 'total_questions', 'percentage', 'score_200', 'submitted_at')
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'category', 'has_taken_exam', 'user_score_200', 'date_joined')
    list_filter = ('has_taken_exam', 'category')
    search_fields = ('username',)
    inlines = [ExamResultInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email')}),
        ('آزمون', {'fields': ('category', 'has_taken_exam', 'score')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'category'),
        }),
    )

    def user_score_200(self, obj):
        return obj.examresult.score_200 if hasattr(obj, 'examresult') else "-"
    user_score_200.short_description = "نمره (از ۲۰۰)"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count')
    search_fields = ('name',)

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "تعداد سوالات"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'category', 'correct_option')
    list_filter = ('category', 'correct_option')
    search_fields = ('text', 'category__name')

    def text_preview(self, obj):
        return obj.text[:70] + "..." if len(obj.text) > 70 else obj.text
    text_preview.short_description = "متن سوال"


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'score_200', 'percentage', 'submitted_at')
    list_filter = ('submitted_at',)
    readonly_fields = ('user', 'correct_answers', 'total_questions', 'percentage', 'score_200', 'submitted_at')
    search_fields = ('user__username',)

    def has_add_permission(self, request):
        return False