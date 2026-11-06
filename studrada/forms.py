from django import forms
from . models import Course


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    description = forms.CharField(required=False, widget=forms.Textarea)
    is_done = forms.BooleanField(required=False, widget=forms.CheckboxInput)


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, label="Назва")
    slug = forms.SlugField(label="Slug (адреса)")
    level = forms.ChoiceField(choices=Course.Level.choices, label="Рівень")
    teacher = forms.CharField(max_length=100, label="Викладач")
    hours = forms.IntegerField(min_value=1, label="Годин")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Опис")
