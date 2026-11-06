from django import forms
from . models import Course


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    description = forms.CharField(required=False, widget=forms.Textarea)
    is_done = forms.BooleanField(required=False, widget=forms.CheckboxInput)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "level", "teacher", "hours", "is_new", "description"]
