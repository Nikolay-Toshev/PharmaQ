from django import forms

from PharmaQ.comments.models import Comment


class CommentBaseForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'comment-form',
                'placeholder': 'Enter your comment...',
            }),
        }
        labels = {
            'content': "",
        }

class CommentCreateForm(CommentBaseForm):
    pass


class CommentEditForm(CommentBaseForm):
    class Meta(CommentBaseForm.Meta):
        widgets = {
            'content': forms.Textarea(attrs={})
        }




