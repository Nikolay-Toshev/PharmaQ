from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_img']
        widgets = {
            'profile_img': forms.FileInput(attrs={
                'class': 'add-image-btn',
            }),
        }
        labels = {
            'username': 'Потребителско име',
            'email': 'Имейл',
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'profile_img': 'Профилна снимка',

        }
