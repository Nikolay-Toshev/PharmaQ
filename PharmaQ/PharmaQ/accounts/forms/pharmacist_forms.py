from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PharmacistEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_img', 'personal_info']
        widgets = {
            'profile_img': forms.FileInput(attrs={
                'class': 'add-image-btn',
            }),
        }
