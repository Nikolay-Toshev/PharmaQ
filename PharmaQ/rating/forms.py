from django import forms

from PharmaQ.rating.models import Rating


class LikeForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['like']
        widgets = {
            'like': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_type'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial='like_form'
        )

class DislikeForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['dislike']
        widgets = {
            'dislike': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_type'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial='dislike_form'
        )
