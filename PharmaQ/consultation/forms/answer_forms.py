from django import forms

from PharmaQ.consultation.models import Answer


class AnswerBaseForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Отговор...'}),
        }
        labels = {
            'content': 'Съдържание',
        }


class AnswerCreateForm(AnswerBaseForm):
    pass


class AnswerEditForm(AnswerBaseForm):
    pass