from django import forms
from PharmaQ.consultation.models import Question


class QuestionBaseForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'category_id']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заглавие',
            'content': 'Съдържание',
            'category_id': 'Категория',
        }


class QuestionCreateForm(QuestionBaseForm):
    pass


class QuestionEditForm(QuestionBaseForm):
    pass

