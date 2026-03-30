from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib import messages

from .models import Course, Lesson, Enrollment
from .forms import CourseForm, LessonForm
from .mixins import InstructorRequiredMixin, StudentRequiredMixin
from .ai import generate_summary


# ══════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "courses/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_instructor:
            ctx["my_courses"] = Course.objects.filter(instructor=user)
            ctx["total_students"] = Enrollment.objects.filter(
                course__instructor=user
            ).count()
        else:
            ctx["enrollments"] = Enrollment.objects.filter(student=user).select_related(
                "course", "course__instructor"
            )
            ctx["available_courses"] = (
                Course.objects.filter(status=Course.Status.PUBLISHED)
                .exclude(enrollments__student=user)
                .select_related("instructor")
            )
        return ctx


# ══════════════════════════════════════════════════════════════
#  COURSE VIEWS
# ══════════════════════════════════════════════════════════════
class CourseListView(ListView):
    """Public catalogue of published courses."""

    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        return (
            Course.objects.filter(status=Course.Status.PUBLISHED)
            .select_related("instructor")
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["lessons"] = self.object.lessons.all()
        if self.request.user.is_authenticated:
            ctx["is_enrolled"] = Enrollment.objects.filter(
                student=self.request.user, course=self.object
            ).exists()
        return ctx


class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        messages.success(self.request, "Course created successfully!")
        return super().form_valid(form)


class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Course updated.")
        return super().form_valid(form)


class CourseDeleteView(InstructorRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy("courses:dashboard")

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Course deleted.")
        return super().form_valid(form)


# ══════════════════════════════════════════════════════════════
#  LESSON VIEWS  (with AI Integration Placeholder)
# ══════════════════════════════════════════════════════════════
class LessonCreateView(InstructorRequiredMixin, CreateView):
    """
    Create a Lesson under a Course.
    ───────────────────────────────────────────────────────
    AI INTEGRATION:  On form_valid() we call `generate_summary()`
    from courses/ai.py.  Replace that function's body to plug in
    any Python text-summarization pipeline.
    ───────────────────────────────────────────────────────
    """

    model = Lesson
    form_class = LessonForm
    template_name = "courses/lesson_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(
            Course, slug=kwargs["course_slug"], instructor=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["course"] = self.course
        return ctx

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.course = self.course

        # ── AI integration hook ────────────────────────────
        lesson.ai_summary = generate_summary(lesson.content)
        # ───────────────────────────────────────────────────

        lesson.save()
        messages.success(self.request, "Lesson added!")
        return redirect(self.course.get_absolute_url())


class LessonUpdateView(InstructorRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "courses/lesson_form.html"

    def get_queryset(self):
        return Lesson.objects.filter(course__instructor=self.request.user)

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.ai_summary = generate_summary(lesson.content)
        lesson.save()
        messages.success(self.request, "Lesson updated!")
        return redirect(lesson.get_absolute_url())


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "courses/lesson_detail.html"
    context_object_name = "lesson"

    def get_queryset(self):
        return Lesson.objects.filter(
            course__slug=self.kwargs["course_slug"]
        ).select_related("course")


# ══════════════════════════════════════════════════════════════
#  ENROLLMENT
# ══════════════════════════════════════════════════════════════
class EnrollView(StudentRequiredMixin, View):
    """Enroll the current student in a course."""

    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, status=Course.Status.PUBLISHED)
        _, created = Enrollment.objects.get_or_create(student=request.user, course=course)
        if created:
            messages.success(request, f"Enrolled in '{course.title}'!")
        else:
            messages.info(request, "You are already enrolled.")
        return redirect(course.get_absolute_url())


class UnenrollView(StudentRequiredMixin, View):
    """Unenroll the current student from a course."""

    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        Enrollment.objects.filter(student=request.user, course=course).delete()
        messages.success(request, f"Unenrolled from '{course.title}'.")
        return redirect("courses:dashboard")
