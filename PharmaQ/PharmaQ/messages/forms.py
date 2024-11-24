from django import forms

from PharmaQ.messages.models import Message


class MessageBaseForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your messages',
            }),
        }
        labels = {
            'content': '',
        }


class MessageCreateForm(MessageBaseForm):
    pass


class MessageEditForm(MessageBaseForm):
    pass
