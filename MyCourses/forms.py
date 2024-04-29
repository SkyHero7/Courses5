from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['send_datetime', 'frequency', 'status']
