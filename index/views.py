import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Article, Course, Category, Announcement, Testimonial, ContactMessage, AboutStat, AboutContent


def article_detail(request: HttpRequest, slug):
    article = get_object_or_404(Article, slug=slug)
    article.increase_views()
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)[:3]
    return render(request, 'index/detail.html', {
        'article': article,
        'related_articles': related_articles,
    })


def list_view(request: HttpRequest):
    articles = []
    for a in Article.objects.all():
        articles.append({
            'title': a.title,
            'slug': a.slug,
            'excerpt': a.content[:150] + '...' if len(a.content) > 150 else a.content,
            'featured_image': request.build_absolute_uri(a.featured_image.url) if a.featured_image else '',
            'created_at': a.created_at.isoformat(),
            'reading_time': a.reading_time,
            'views': a.views,
            'category_name': a.category.name if a.category else 'نامشخص',
            'category_slug': a.category.slug if a.category else 'other',
        })

    courses = []
    for c in Course.objects.all():
        courses.append({
            'title': c.title,
            'slug': c.slug,
            'description': c.description,
            'image': request.build_absolute_uri(c.image.url) if c.image else '',
            'start_date': c.start_date.isoformat(),
            'duration': c.duration,
            'features': c.features,
            'views': c.views,
            'category_name': c.category.name if c.category else 'نامشخص',
            'category_slug': c.category.slug if c.category else 'other',
        })

    categories = [{'name': c.name, 'slug': c.slug} for c in Category.objects.all()]

    context = {
        'articles_data': json.dumps(articles, cls=DjangoJSONEncoder, ensure_ascii=False),
        'courses_data': json.dumps(courses, cls=DjangoJSONEncoder, ensure_ascii=False),
        'categories_data': json.dumps(categories, cls=DjangoJSONEncoder, ensure_ascii=False),
    }
    return render(request, 'index/list.html', context)


def home_view(request: HttpRequest):
    latest_articles = Article.objects.order_by('-created_at')[:4]
    announcements = Announcement.objects.filter(is_active=True).order_by('-start_date')[:3]
    testimonials = Testimonial.objects.order_by('-date')[:3]
    categories = Category.objects.all()

    return render(request, 'index/index.html', {
        'latest_articles': latest_articles,
        'announcements': announcements,
        'testimonials': testimonials,
        'categories': categories,
    })


def about_view(request: HttpRequest):
    about_content = AboutContent.objects.first()  # فرض بر این که فقط یک رکورد وجود دارد
    stats = AboutStat.objects.first()  # فرض بر این که فقط یک رکورد وجود دارد

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'پیام شما با موفقیت ارسال شد. همکاران ما در اسرع وقت با شما تماس خواهند گرفت.')
        else:
            messages.error(request, 'لطفاً تمام فیلدهای الزامی را پر کنید.')

    return render(request, 'index/about.html', {
        'about_content': about_content,
        'stats': stats,
    })