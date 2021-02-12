from django import forms
from .models import Objective, KR, Entry


class ObjectiveCreationForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['objective']
        labels = {
            "objective": "Objective"
        }


class KRCreationForm(forms.ModelForm):
    class Meta:
        model = KR
        fields = ['objective', 'key_result']
        labels = {
            "objective": "Objective",
            "key_result": "Key Result"
        }


class EntryCreationForm(forms.ModelForm):
    update = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,
        'minlength': 20,
        'title': "Brief update",

    }))
    class Meta:
        model = Entry
        fields = ['date_time','key_result', 'percentage', 'update', 'time_spent']
        labels = {
            "date_time": "Date",
            "key_result": "Key Result",
            "percentage": "Percentage",
            "update": "Brief update",
            "time_spent": "Productive time spent"
        }
