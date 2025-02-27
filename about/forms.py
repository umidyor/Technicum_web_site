from django import forms
from .models import Achievement,News
import os

def validate_file_type(file):
    allowed_extensions = ['.mp4','.jpg', '.jpeg', '.png']  # Add any allowed extensions
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise forms.ValidationError(f'File type {ext} is not allowed.')


from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]

        # Validate file type for each file
        for file in result:
            validate_file_type(file)
        return result


class AchievementForm(forms.ModelForm):
    achievement_files = MultipleFileField()
    news_name = forms.CharField(max_length=300)
    news_description = forms.CharField(widget=forms.Textarea)
    news_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Achievement
        fields = ['achievement_files', 'news_name', 'news_description', 'news_date']

