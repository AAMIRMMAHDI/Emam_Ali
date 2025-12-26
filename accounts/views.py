# accounts/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
import json

from .models import Question, ExamResult


# ویوی لاگین سفارشی
class CustomLoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:exam_page')


# ویوی اصلی صفحه آزمون (MVT کامل)
class ExamView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/exam-results.html'

    def dispatch(self, request, *args, **kwargs):
        # ادمین و staff اجازه ورود ندارن
        if request.user.is_staff or request.user.is_superuser:
            return HttpResponseForbidden("دسترسی برای مدیران مجاز نیست.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # اگر قبلاً آزمون داده باشه
        if user.has_taken_exam:
            context['exam_already_taken'] = True
            if hasattr(user, 'examresult'):
                context['score_200'] = user.examresult.score_200
                context['percentage'] = user.examresult.percentage
                context['correct_answers'] = user.examresult.correct_answers
                context['total_questions'] = user.examresult.total_questions
            return context

        # اگر دسته‌بندی نداشته باشه
        if not user.category:
            context['no_category'] = True
            return context

        # ارسال سوالات به تمپلیت
        questions = Question.objects.filter(category=user.category).order_by('id')
        context['questions_json'] = [
            {
                'id': q.id,
                'text': q.text,
                'options': [q.option_a, q.option_b, q.option_c, q.option_d],
                # ایندکس گزینه صحیح (0=الف، 1=ب، 2=ج، 3=د)
                'correct_index': {'A': 0, 'B': 1, 'C': 2, 'D': 3}[q.correct_option]
            } for q in questions
        ]
        context['total_questions'] = questions.count()
        return context


# ویوی ثبت پاسخ‌های آزمون (API JSON)
@method_decorator(csrf_exempt, name='dispatch')
class SubmitExamView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user

        # جلوگیری از آزمون مجدد
        if user.has_taken_exam:
            return JsonResponse({
                "error": "شما قبلاً آزمون را انجام داده‌اید و نمی‌توانید دوباره شرکت کنید."
            }, status=403)

        # خواندن داده‌های ارسالی از فرانت (JSON)
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})  # فرمت: {"1": 0, "2": 2, "3": 1, ...}
        except json.JSONDecodeError:
            return JsonResponse({"error": "فرمت داده نامعتبر است."}, status=400)

        if not user.category:
            return JsonResponse({"error": "دسته‌بندی آزمون برای شما تعیین نشده است."}, status=400)

        questions = Question.objects.filter(category=user.category)
        total = questions.count()
        correct = 0

        # محاسبه تعداد پاسخ‌های صحیح
        correct_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        for q in questions:
            user_answer = answers.get(str(q.id))
            if user_answer is not None:
                if int(user_answer) == correct_map[q.correct_option]:
                    correct += 1

        answered_count = len(answers)
        unanswered_count = total - answered_count
        incorrect_count = answered_count - correct

        percentage = round((correct / total) * 100, 1) if total > 0 else 0
        score_200 = int(percentage * 2)

        # ثبت وضعیت و نتیجه
        user.has_taken_exam = True
        user.score = score_200
        user.save()

        ExamResult.objects.create(
            user=user,
            correct_answers=correct,
            total_questions=total,
            percentage=percentage,
            score_200=score_200
        )

        # پاسخ نهایی به فرانت‌اند
        return JsonResponse({
            "correct": correct,
            "incorrect": incorrect_count,
            "unanswered": unanswered_count,
            "total": total,
            "percentage": percentage,
            "score_200": score_200
        })