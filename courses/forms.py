from django import forms
from django.utils.text import slugify

from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "description", "thumbnail", "status")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Course title", "class": "form-input"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Describe your course…", "rows": 4, "class": "form-input"}
            ),
            "status": forms.Select(attrs={"class": "form-input"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            base_slug = slugify(instance.title)
            slug = base_slug
            n = 1
            while Course.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "content", "order", "video_url")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Lesson title", "class": "form-input"}),
            "content": forms.Textarea(
                attrs={"placeholder": "Write your lesson content…", "rows": 8, "class": "form-input"}
            ),
            "order": forms.NumberInput(attrs={"class": "form-input", "min": 0}),
            "video_url": forms.URLInput(attrs={"placeholder": "https://youtube.com/...", "class": "form-input"}),
        }
