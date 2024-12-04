from django import forms

from PharmaQ.message.models import Message


class MessageBaseForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-textarea',
                'placeholder': 'Въведете съобщението си',
            }),
        }
        labels = {
            'content': '',
        }


class MessageCreateForm(MessageBaseForm):
    pass


class MessageEditForm(MessageBaseForm):
    pass
