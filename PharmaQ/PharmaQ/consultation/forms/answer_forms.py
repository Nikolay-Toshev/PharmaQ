from django import forms

from PharmaQ.consultation.models import Answer


class AnswerBaseForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AnswerCreateForm(AnswerBaseForm):
    pass
