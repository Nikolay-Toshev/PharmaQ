from django import forms
from PharmaQ.consultation.models import Category


class CategoryBaseForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['slug']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Описание',
            'title': 'Заглавие',
        }


class CategoryCreateForm(CategoryBaseForm):
    pass


class CategoryEditForm(CategoryBaseForm):
    pass



