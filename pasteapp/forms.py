from datetime import datetime, timedelta

from django import forms
from django.utils import html

from .models import *


class CreatePasteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePasteForm, self).__init__(*args, **kwargs)
        # self.fields["slug"].initial = "Initial"

    class Meta:
        model = Paste
        exclude = ('user', 'created_at')
        error_messages = {
            'content': {
                'required': 'Content is required',
                'max_length': 'Content is too long'
            },
            'slug': {
                'required': 'Slug is required',
                'max_length': 'Slug is too long'
            }
        }

    def save(self, commit=True):
        paste = super(CreatePasteForm, self).save(commit=False)
        if len(self.cleaned_data['title']) == 0:
            paste.title = 'Untitled'
        paste.content = html.escape(self.cleaned_data['content'])
        if self.cleaned_data['expire'] == '10M':
            expire = '10 minutes'
            timed = timedelta(minutes=10)
        elif self.cleaned_data['expire'] == '1H':
            expire = '1 hour'
            timed = timedelta(hours=1)
        elif self.cleaned_data['expire'] == '1D':
            expire = '1 day'
            timed = timedelta(days=1)
        elif self.cleaned_data['expire'] == '1W':
            expire = '1 week'
            timed = timedelta(weeks=1)
        elif self.cleaned_data['expire'] == '1M':
            expire = '1 month'
            timed = timedelta(days=30)
        elif self.cleaned_data['expire'] == '6M':
            expire = '6 months'
            timed = timedelta(days=30 * 6)
        elif self.cleaned_data['expire'] == '1Y':
            expire = '1 year'
            timed = timedelta(days=365)
        elif self.cleaned_data['expire'] == 'SD':
            expire = 'SD'
            timed = timedelta(minutes=1)
        else:
            expire = 'N'
        if expire != 'N':
            if expire == 'SD':
                paste.self_destroy = True
            else:
                paste.expire_time = datetime.now() + timed
        else:
            paste.expire_time = timezone.now() + timedelta(days=1200)
        if commit:
            paste.save()
        return paste
