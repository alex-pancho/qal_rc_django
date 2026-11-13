from django import forms
from . models import Course, CourseReview


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    description = forms.CharField(required=False, widget=forms.Textarea)
    is_done = forms.BooleanField(required=False, widget=forms.CheckboxInput)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "level", "teacher", "hours", "is_new", "description"]
        labels = {
            "title": "Назва",
            "slug": "Адреса (slug)",
            "level": "Рівень",
            "teacher": "Викладач",
            "hours": "Тривалість, годин",
            "is_new": "Позначити як новий",
            "description": "Опис",
        }
        help_texts = {"slug": "Латиниця, цифри та дефіси. Це частина URL."}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Наприклад: Python для QA"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Назва має містити щонайменше 5 символів.")
        return title

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("level") == Course.Level.ADVANCED and (cleaned.get("hours") or 0) < 20:
            self.add_error("hours", "Просунутий курс має тривати щонайменше 20 годин.")
        return cleaned


class CourseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(value, str(value)) for value in range(1, 6)],
        widget=forms.RadioSelect,
        label="Оцінка",
    )

    class Meta:
        model = CourseReview
        fields = ["rating", "comment"]
        labels = {"comment": "Коментар"}
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Поділіться враженнями про курс"}),
        }
