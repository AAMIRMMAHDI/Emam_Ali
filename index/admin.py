from django.contrib import admin
from .models import Category, Author, Article, Course, Announcement, Testimonial, ContactMessage, AboutStat, AboutContent

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'created_at', 'views')
    list_filter = ('category',)
    search_fields = ('title', 'content')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'start_date', 'duration')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'is_active')
    list_filter = ('is_active',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'date')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)

@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ('years_experience', 'graduates', 'courses', 'teachers')

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'text', 'image')